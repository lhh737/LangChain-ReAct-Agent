"""
检索增强生成服务：混合检索 → Reranker 精排 → Query Rewrite → 引用绑定 → LLM 低温生成 → 引用校验
"""
import re
import json
import hashlib
import os
from datetime import datetime
import numpy as np
import jieba
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from rag.vector_store import VectorStoreService
from rag.bm25_store import BM25Store
from rag.retrieval_strategy import HybridRetriever, Reranker, PAPER_NAME_KEYWORDS
from utils.prompt_loader import load_rag_prompts
from utils.config_handler import rag_conf, chroma_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model, embed_model


class RagSummarizeService:
    # 中译英 Prompt（用于检索前将中文查询翻译为英文）
    DETECT_TRANSLATE_PROMPT = PromptTemplate.from_template(
        "You are a query language detector and translator for an English-only academic paper retrieval system.\n"
        "\n"
        "If the query is already in English, output it EXACTLY unchanged — do NOT modify, improve, or rewrite a single character.\n"
        "If the query is in Chinese (or any non-English language), translate it into English following these rules:\n"
        "\n"
        "1. NEVER translate proper nouns — paper names, method names, system names, model names MUST stay in their original English form (e.g., \"transformer\", \"CNN\", \"BERT\", \"BTD\", \"PoisonedRAG\", \"FlippedRAG\", \"AgentSentinel\")\n"
        "2. Keep abbreviations in English (DNN, RAG, LLM, NLP, etc.), optionally append their English full names\n"
        "3. Preserve the original meaning exactly\n"
        "\n"
        "Output ONLY the resulting query. No explanation, no quotes, no markdown.\n"
        "\n"
        "Query: {query}\n"
        "Output:"
    )

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.vector_retriever = self.vector_store.get_retriever()

        self.bm25_store = BM25Store()
        self.bm25_store.load()

        self.hybrid_retriever = HybridRetriever(
            vector_store=self.vector_store.vector_store,
            bm25_store=self.bm25_store,
        )
        self.reranker = Reranker(passage_mode=True, fusion_enabled=True)

        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()

        # 加载已验证的缩写表（优先缓存 JSON → YAML 全量）
        self._active_abbreviations: dict[str, str] = self._load_abbreviation_index()

        # 中译英缓存
        self._translate_cache: dict[str, str] = {}

        # 索引一致性检查
        self._check_index_manifest()

    def _init_chain(self):
        return self.prompt_template | self.model | StrOutputParser()

    # ---------- 缩写索引 ----------

    def _abbreviation_index_path(self) -> str:
        return get_abs_path("data/abbreviation_index.json")

    def _load_abbreviation_index(self) -> dict[str, str]:
        """加载已验证的缩写索引：优先缓存 JSON，不存在则退回 YAML 全量"""
        cache_path = self._abbreviation_index_path()
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"[AbbrIndex]从缓存加载：{len(data)} 条已验证缩写")
            return data
        # 退化：使用 YAML 全量
        raw = rag_conf.get("abbreviation_map", {})
        logger.info(f"[AbbrIndex]缓存不存在，使用 YAML 全量：{len(raw)} 条")
        return raw

    def _build_abbreviation_index(self, documents: list[Document]):
        """入库时构建术语索引：扫描语料，只保留全称在语料中出现的缩写"""
        raw_map = rag_conf.get("abbreviation_map", {})
        if not raw_map:
            return

        corpus = " ".join(d.page_content for d in documents).lower()
        active: dict[str, str] = {}
        for abbr, full in raw_map.items():
            if full.lower() in corpus:
                active[abbr] = full
            else:
                logger.debug(f"[AbbrIndex]禁用「{abbr} → {full}」（语料中未出现全称）")

        cache_path = self._abbreviation_index_path()
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(active, f, ensure_ascii=False, indent=2)
        self._active_abbreviations = active
        logger.info(f"[AbbrIndex]构建完成：{len(active)}/{len(raw_map)} 条已验证，缓存至 {cache_path}")

    # ---------- 索引清单 ----------

    def _manifest_path(self) -> str:
        return get_abs_path("data/index_manifest.json")

    def _check_index_manifest(self):
        """检查 Chroma / BM25 / Abbreviation 索引是否同步"""
        manifest_path = self._manifest_path()
        if not os.path.exists(manifest_path):
            logger.warning("[Manifest]index_manifest.json 不存在，请执行 rebuild_bm25_index()")
            return

        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)

        chroma_count = self._count_chroma_docs()
        bm25_count = len(self.bm25_store._documents) if self.bm25_store.is_built() else 0
        abbr_count = len(self._active_abbreviations)

        ok = True
        if chroma_count != m.get("chroma_doc_count", -1):
            logger.warning(f"[Manifest]Chroma 文档数不一致：当前 {chroma_count} vs 清单 {m.get('chroma_doc_count')}")
            ok = False
        if bm25_count != m.get("bm25_doc_count", -1):
            logger.warning(f"[Manifest]BM25 文档数不一致：当前 {bm25_count} vs 清单 {m.get('bm25_doc_count')}")
            ok = False

        if ok and chroma_count > 0:
            logger.info(f"[Manifest]索引一致：Chroma={chroma_count} BM25={bm25_count} Abbr={abbr_count}")

    def _count_chroma_docs(self) -> int:
        try:
            collection = self.vector_store.vector_store._collection
            return collection.count()
        except Exception:
            return -1

    def _write_manifest(self, documents: list[Document]):
        """入库后更新索引清单"""
        source_md5 = {}
        for d in documents:
            src = d.metadata.get("source_file", "unknown")
            if src not in source_md5:
                source_md5[src] = hashlib.md5(d.page_content.encode()).hexdigest()[:8]

        manifest = {
            "chroma_doc_count": self._count_chroma_docs(),
            "bm25_doc_count": len(documents),
            "abbreviation_index_size": len(self._active_abbreviations),
            "source_files": source_md5,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self._manifest_path(), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        logger.info(f"[Manifest]已更新：{manifest['chroma_doc_count']} docs")

    # ---------- 查询改写 ----------

    def _rewrite_query(self, query: str) -> str:
        """仅展开语料库已验证的缩写"""
        extra_terms = []
        for abbr, full in self._active_abbreviations.items():
            if re.search(r"\b" + re.escape(abbr) + r"\b", query):
                extra_terms.append(full)
        if extra_terms:
            return query + " " + " ".join(extra_terms)
        return query

    def _translate_query(self, query: str) -> str:
        """中→英翻译：英文原样返回，中文经 LLM 翻译为英文学术检索词（带缓存）"""
        if query in self._translate_cache:
            return self._translate_cache[query]
        try:
            chain = self.DETECT_TRANSLATE_PROMPT | self.model | StrOutputParser()
            result = chain.invoke({"query": query}).strip()
            result = result.strip('"').strip("'").strip()
        except Exception:
            logger.warning(f"[Translate] LLM 翻译失败，回退原文")
            result = query
        self._translate_cache[query] = result
        return result

    # ---------- 检索 + 生成 ----------

    def rebuild_bm25_index(self):
        """从 Chroma 重建 BM25 索引 + 术语索引 + 清单（文档加载后调用）"""
        if not self.vector_store.vector_store:
            return
        collection = self.vector_store.vector_store._collection
        result = collection.get()
        documents = []
        for i, content in enumerate(result.get("documents", [])):
            meta = result.get("metadatas", [{}])[i] if result.get("metadatas") else {}
            documents.append(Document(page_content=content, metadata=meta))
        if documents:
            self.bm25_store.build_index(documents)
            self.bm25_store.save()
            self._build_abbreviation_index(documents)
            self._write_manifest(documents)

    def retriever_docs(self, query: str, section_filter: str | None = None) -> list[Document]:
        """混合检索 → RRF 融合(50) → Reranker 精排(8)"""
        logger.info(f"[Retrieve] 原始query: {query[:200]}")
        rewritten = self._rewrite_query(query)
        rewritten = self._translate_query(rewritten)
        if rewritten != query:
            logger.info(f"[Retrieve] 改写后query: {rewritten[:200]}")
        docs = self.hybrid_retriever.retrieve(rewritten, section_filter=section_filter)
        docs = self.reranker.rerank(rewritten, docs)
        for i, doc in enumerate(docs, 1):
            meta = doc.metadata
            title = meta.get("paper_title", "?")
            section = meta.get("section", "?")
            ps = meta.get("page_start") or meta.get("page", "?")
            pe = meta.get("page_end") or meta.get("page", "?")
            page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}"
            preview = doc.page_content[:80].replace("\n", " ")
            logger.info(f"[Retrieve] chunk[{i}] 《{title}》| {section} | {page} | {preview}...")
        return docs

    def retrieve_with_quality(self, query: str) -> dict:
        """一次检索，返回结构化结果：text + docs + quality_report"""
        docs = self.retriever_docs(query)
        # 用同一批 docs 构建 context 并生成回答（避免二次检索）
        context = ""
        for i, doc in enumerate(docs, 1):
            meta = doc.metadata
            parts = []
            if meta.get("paper_title"):
                parts.append(f"《{meta['paper_title']}》")
            if meta.get("section"):
                parts.append(f"{meta['section']}")
            ps = meta.get("page_start") or meta.get("page")
            pe = meta.get("page_end") or meta.get("page")
            if ps and pe:
                parts.append(f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}")
            citation = " · ".join(parts) if parts else "未知来源"
            context += f"[{i}] {citation}\n{doc.page_content}\n\n"
        text = self.chain.invoke({"input": query, "context": context})
        text = self._verify_citations(text, len(docs))
        quality = self._check_retrieval_quality(query, docs)
        return {"text": text, "docs": docs, "quality": quality}

    def _check_retrieval_quality(self, query: str, docs: list[Document]) -> dict:
        """四信号质量评估，返回完整报告"""
        top5 = docs[:5]
        scores = self.reranker.last_fusion_scores or []
        max_score = float(max(scores)) if scores else 0.0

        # S1: Reranker 最高分过低
        min_score = chroma_conf.get("quality_reranker_min_score", 0.35)
        s1 = max_score > 0 and max_score < min_score

        # S2: 论文名不匹配
        query_lower = query.lower()
        papers_in_query = {kw for kw in PAPER_NAME_KEYWORDS if kw.lower() in query_lower}
        papers_in_chunks: set[str] = set()
        for doc in top5:
            title = (doc.metadata.get("paper_title", "") or "").lower()
            for kw in PAPER_NAME_KEYWORDS:
                if kw.lower() in title:
                    papers_in_chunks.add(kw)
        s2 = bool(papers_in_query) and not bool(papers_in_query & papers_in_chunks)

        # S3: 关键词覆盖率低
        query_tokens = self._tokenize(query)
        chunk_tokens: set[str] = set()
        for doc in top5:
            chunk_tokens.update(self._tokenize(doc.page_content))
        coverage = len(query_tokens & chunk_tokens) / len(query_tokens) if query_tokens else 0
        min_cov = chroma_conf.get("quality_keyword_coverage_min", 0.3)
        s3 = coverage < min_cov

        # S4: 领域相似度低
        s4 = False
        domain_max_sim = 0.0
        try:
            titles = list(dict.fromkeys(
                doc.metadata.get("paper_title", "") for doc in top5 if doc.metadata.get("paper_title")
            ))
            if titles:
                query_emb = np.array(embed_model.embed_query(query))
                title_embs = np.array(embed_model.embed_documents(titles))
                sims = np.dot(title_embs, query_emb) / (
                    np.linalg.norm(title_embs, axis=1) * np.linalg.norm(query_emb) + 1e-8
                )
                domain_max_sim = float(np.max(sims))
                domain_min = chroma_conf.get("quality_domain_similarity_min", 0.45)
                s4 = domain_max_sim < domain_min
            else:
                s4 = True
        except Exception:
            s4 = False

        signals = [s1, s2, s3, s4]
        return {
            "is_soft_miss": sum(signals) >= 2,
            "signal_count": sum(signals),
            "signals": {
                "low_reranker_score": s1,
                "paper_mismatch": s2,
                "low_keyword_coverage": s3,
                "domain_mismatch": s4,
            },
            "max_score": max_score,
            "coverage": coverage,
            "domain_max_sim": domain_max_sim,
        }

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        tokens = list(jieba.cut(text))
        return {t.strip().lower() for t in tokens if len(t.strip()) > 1}

    def _verify_citations(self, answer: str, num_docs: int) -> str:
        """校验回答中的 [N] 引用编号，非法编号追加警告"""
        cited = set(int(m) for m in re.findall(r"\[(\d+)\]", answer))
        invalid = sorted(n for n in cited if n < 1 or n > num_docs)
        if invalid:
            answer += (
                f"\n\n> ⚠ 引用校验警告：发现无效引用编号 {invalid}，"
                f"有效范围为 [1-{num_docs}]，请忽略无效引用。"
            )
        return answer

    def rag_summarize(self, query: str, section_filter: str | None = None) -> str:
        """检索 + 编号引用绑定 + 低温生成 + 引用校验"""
        context_docs = self.retriever_docs(query, section_filter=section_filter)

        context = ""
        for i, doc in enumerate(context_docs, 1):
            meta = doc.metadata
            parts = []
            if meta.get("paper_title"):
                parts.append(f"《{meta['paper_title']}》")
            if meta.get("section"):
                parts.append(f"{meta['section']}")

            # 页码：优先 page_start-page_end → 兼容旧 page 字段
            ps = meta.get("page_start") or meta.get("page")
            pe = meta.get("page_end") or meta.get("page")
            if ps and pe:
                if ps == pe:
                    parts.append(f"p.{ps}")
                else:
                    parts.append(f"pp.{ps}-{pe}")

            citation = " · ".join(parts) if parts else "未知来源"
            context += f"[{i}] {citation}\n{doc.page_content}\n\n"

        answer = self.chain.invoke({"input": query, "context": context})
        answer = self._verify_citations(answer, len(context_docs))
        return answer


if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize("深度学习图像分割有哪些主流方法？"))

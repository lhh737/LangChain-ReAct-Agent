import json
import hashlib
import re
import urllib.request
import os
import jieba
from langchain_core.documents import Document
from langchain_chroma import Chroma
from rag.bm25_store import BM25Store
from rag.paper_metadata import PaperSection, SECTION_HEADER_PATTERNS
from utils.config_handler import chroma_conf
from utils.logger_handler import logger

# 章节别名→规范名映射（中文→英文）
SECTION_ALIAS_MAP: dict[str, str] = {}
for _section, _headers in SECTION_HEADER_PATTERNS.items():
    for _h in _headers:
        SECTION_ALIAS_MAP[_h.lower()] = _section

# 硅基流动 rerank API 地址
SILICONFLOW_RERANK_URL = "https://api.siliconflow.cn/v1/rerank"
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")

# ────────── Metadata-aware boost ──────────
# 论文缩写/关键词 → 用于匹配 paper_title / paper_id
PAPER_NAME_KEYWORDS = [
    "PoisonedRAG", "FlippedRAG", "AgentSentinel", "Appatch",
    "FlatD", "MACO", "PatchAgent", "Codellm", "Devkit",
    "BTD", "Bin-to-DNN", "BGE-M3", "BGE-Reranker",
    "Achieving Zen", "Machine Against the RAG",
    "Give LLMs a Security Course", "Hardening Deep Neural Network",
    "LLMs Understanding Code Syntax", "Pitfalls in Language Models",
]

# Query 章节意图词 → section 值映射
SECTION_INTENT_MAP: dict[str, str] = {}
for _sec, _headers in SECTION_HEADER_PATTERNS.items():
    for _h in _headers:


        SECTION_INTENT_MAP[_h] = _sec

# 额外章节别名（查询意图词 → PaperSection 值，中英双语）
_EXTRA_SECTION_ALIASES = {
    # 中文
    "方法论": "method", "技术方案": "method", "模型设计": "method", "系统设计": "method",
    "实验评估": "experiment", "消融实验": "experiment", "基准测试": "experiment",
    "实验结果": "results", "性能分析": "results",
    "威胁模型": "method", "攻击方法": "method", "安全防御": "method",
    "逆向工程": "method", "代码智能": "method", "程序修复": "method",
    "漏洞检测": "method", "问题定义": "method",
    "相关工作": "related_work", "文献综述": "related_work",
    "未来工作": "conclusion", "研究背景": "introduction",
    # 英文
    "methodology": "method", "approach": "method", "architecture": "method",
    "design": "method", "implementation": "method", "framework": "method",
    "threat model": "method", "attack method": "method", "defense": "method",
    "reverse engineering": "method", "program repair": "method",
    "vulnerability detection": "method", "code intelligence": "method",
    "experiment evaluation": "experiment", "ablation": "experiment",
    "benchmark": "experiment", "evaluation": "experiment",
    "results": "results", "performance": "results",
    "related work": "related_work", "literature review": "related_work",
    "future work": "conclusion", "background": "introduction",
    "experimental results": "results",
}
SECTION_INTENT_MAP.update(_EXTRA_SECTION_ALIASES)


class HybridRetriever:
    """BM25 + 向量 RRF 融合检索器（支持 metadata-aware boost + rrf_k 覆写）"""

    def __init__(
        self,
        vector_store: Chroma,
        bm25_store: BM25Store,
        rrf_k_override: int | None = None,
        hybrid_k_override: int | None = None,
        rrf_fusion_k_override: int | None = None,
    ):
        self.vector_store = vector_store
        self.bm25_store = bm25_store
        self.rrf_k = rrf_k_override if rrf_k_override is not None else chroma_conf.get("rrf_k", 60)
        self.hybrid_k = hybrid_k_override if hybrid_k_override is not None else chroma_conf.get("hybrid_retrieval_k", 30)
        self.rrf_fusion_k = rrf_fusion_k_override if rrf_fusion_k_override is not None else chroma_conf.get("rrf_fusion_k", 20)
        self.section_filter_mode = chroma_conf.get("section_filter_mode", "soft")
        self.section_soft_boost = chroma_conf.get("section_soft_boost", 0.01)
        # Metadata boost 权重
        self.boost_program_name = chroma_conf.get("boost_program_name", 0.03)
        self.boost_program_code = chroma_conf.get("boost_program_code", 0.04)
        self.boost_section_match = chroma_conf.get("boost_section_match", 0.01)

    def _normalize_section(self, section: str) -> str:
        """将中文章节名归一化为英文 PaperSection 值，用于 metadata 过滤"""
        section_lower = section.lower()
        if section_lower in SECTION_ALIAS_MAP:
            return SECTION_ALIAS_MAP[section_lower]
        valid = {s.value for s in PaperSection}
        if section_lower in valid:
            return section_lower
        return section

    @staticmethod
    def _extract_query_entities(query: str) -> dict:
        """从 query 中提取论文名、章节意图（用于 metadata boost）"""
        entities: dict[str, list[str]] = {
            "paper_names": [],
            "section_types": [],
        }
        # 论文名：从预定义关键词中匹配
        for kw in PAPER_NAME_KEYWORDS:
            if kw.lower() in query.lower():
                entities["paper_names"].append(kw)

        # 章节意图：从 query 关键词映射到 section 值（大小写不敏感）
        query_lower = query.lower()
        for kw, sec in SECTION_INTENT_MAP.items():
            if kw.lower() in query_lower:
                entities["section_types"].append(sec)

        return entities

    def _apply_metadata_boost(
        self,
        doc: Document,
        entities: dict,
    ) -> float:
        """根据 query 实体匹配程度计算额外加分"""
        boost = 0.0
        meta = doc.metadata

        # 论文名匹配（paper_title 或 source_file 包含 query 中的论文名）
        for pn in entities.get("paper_names", []):
            title = meta.get("paper_title", "") or ""
            source = meta.get("source_file", "") or ""
            if pn in title or pn in source:
                boost += self.boost_program_name
                break

        # 章节意图匹配
        doc_section = meta.get("section", "")
        for st in entities.get("section_types", []):
            if st == doc_section:
                boost += self.boost_section_match
                break

        return boost

    def retrieve(
        self, query: str, k: int | None = None, section_filter: str | None = None
    ) -> list[Document]:
        """混合检索：BM25 + 向量 RRF 融合，支持章节过滤（soft/hard）+ metadata boost"""
        k = k or self.rrf_fusion_k
        normalized_section = self._normalize_section(section_filter) if section_filter else None
        entities = self._extract_query_entities(query)

        # 确定是否硬过滤
        hard_filter = (
            normalized_section
            and chroma_conf.get("section_filter_enabled", False)
            and self.section_filter_mode == "hard"
        )

        # 1. 向量检索 — soft 模式全局检索，hard 模式按 section 过滤
        if hard_filter:
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": self.hybrid_k, "filter": {"section": normalized_section}}
            )
        else:
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": self.hybrid_k}
            )
        vector_docs = retriever.invoke(query)

        # 2. BM25 关键词检索 — hard 模式才过滤
        if self.bm25_store.is_built():
            bm25_results = self.bm25_store.search(query, self.hybrid_k)
            if hard_filter:
                bm25_results = [
                    (d, s) for d, s in bm25_results
                    if d.metadata.get("section") == normalized_section
                ]
            bm25_docs = [d for d, _ in bm25_results]
        else:
            bm25_docs = []

        # 3. RRF 融合（内部应用 soft section boost + metadata boost）
        if bm25_docs:
            merged = self._rrf_fusion(vector_docs, bm25_docs, k, entities, normalized_section)
        else:
            merged = vector_docs[:k]

        return merged

    def _rrf_fusion(
        self,
        vector_docs: list[Document],
        bm25_docs: list[Document],
        top_k: int,
        entities: dict | None = None,
        section_boost_for: str | None = None,
    ) -> list[Document]:
        """RRF (Reciprocal Rank Fusion) + section soft boost + metadata-aware boost"""
        scores: dict[str, float] = {}
        doc_map: dict[str, Document] = {}

        for rank, doc in enumerate(vector_docs, 1):
            key = hashlib.md5(doc.page_content.encode()).hexdigest()
            scores[key] = scores.get(key, 0) + 1.0 / (self.rrf_k + rank)
            doc_map[key] = doc

        for rank, doc in enumerate(bm25_docs, 1):
            key = hashlib.md5(doc.page_content.encode()).hexdigest()
            scores[key] = scores.get(key, 0) + 1.0 / (self.rrf_k + rank)
            doc_map[key] = doc

        # Soft section boost: 匹配章节的文档加小幅加分（不改变 rank 公式）
        if section_boost_for and self.section_filter_mode == "soft":
            for key in scores:
                if doc_map[key].metadata.get("section") == section_boost_for:
                    scores[key] += self.section_soft_boost

        # Metadata-aware boost：论文名 + 章节意图（在 RRF 分数基础上叠加）
        if entities:
            has_entities = any(entities.get(k) for k in entities)
            if has_entities:
                for key in scores:
                    scores[key] += self._apply_metadata_boost(doc_map[key], entities)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [doc_map[key] for key, _ in ranked if key in doc_map]


class Reranker:
    """使用硅基流动 rerank API + metadata-aware score fusion 重排序"""

    def __init__(self, passage_mode: bool = False, fusion_enabled: bool | None = None, alpha: float | None = None):
        self.url = SILICONFLOW_RERANK_URL
        self.api_key = SILICONFLOW_API_KEY
        self.model = chroma_conf.get("reranker_model", "BAAI/bge-reranker-v2-m3")
        self.enabled = chroma_conf.get("enable_reranker", False) and bool(self.api_key)
        self.min_score = chroma_conf.get("reranker_min_score", 0.01)
        self.fallback_enabled = chroma_conf.get("reranker_fallback_enabled", True)
        self.passage_mode = passage_mode

        # Score fusion 参数
        self.fusion_enabled = fusion_enabled if fusion_enabled is not None else chroma_conf.get("score_fusion_enabled", False)
        self.alpha = alpha if alpha is not None else chroma_conf.get("score_fusion_alpha", 0.7)
        self.meta_score_program = chroma_conf.get("meta_score_program", 0.08)
        self.meta_score_degree = chroma_conf.get("meta_score_degree", 0.04)
        self.meta_score_section = chroma_conf.get("meta_score_section", 0.02)
        self.meta_score_keyword = chroma_conf.get("meta_score_keyword", 0.02)

        # 调试：记录最近一次 rerank 的分数
        self.last_reranker_scores: list[float] = []
        self.last_metadata_scores: list[float] = []
        self.last_fusion_scores: list[float] = []

    @staticmethod
    def _extract_paper_short_name(paper_id: str) -> str:
        """从 paper_id 中提取论文缩写简称"""
        mapping = {
            "PoisonedRAG": ["PoisonedRAG", "Knowledge Corruption Attacks"],
            "FlippedRAG": ["FlippedRAG", "Black-Box Opinion Manipulation"],
            "AgentSentinel": ["AgentSentinel", "Real-Time Security Defense"],
            "Appatch": ["Appatch", "Adaptive Prompting"],
            "FlatD": ["FlatD", "Protecting Deep Neural Network"],
            "MACO": ["MACO", "Model Anti-Extraction"],
            "PatchAgent": ["PatchAgent", "Program Repair Agent"],
            "BTD": ["BTD", "Bin-to-DNN", "Decompiling x86"],
            "Codellm-Devkit": ["Codellm-Devkit", "Contextualizing"],
            "Achieving Zen": ["Achieving Zen", "Combining Mathematical"],
            "Machine Against the RAG": ["Machine Against the RAG", "Jamming Retrieval"],
            "Give LLMs a Security Course": ["Give LLMs a Security Course", "Securing Retrieval-Augmented"],
            "Hardening DNN": ["Hardening Deep Neural Network", "Reverse Engineering Attacks"],
            "LLMs Code": ["Understanding Code Syntax and Semantics", "Code Intelligence"],
            "Pitfalls": ["Pitfalls in Language Models", "Code Intelligence"],
        }
        for short_name, patterns in mapping.items():
            for pat in patterns:
                if pat in paper_id:
                    return short_name
        return paper_id[:30]

    def _build_passage(self, doc: Document) -> str:
        """构造增强 passage：来源 + 文档标题 + 章节 + 页码 + 正文"""
        meta = doc.metadata
        parts = []
        src = meta.get("source_file", "")
        if src:
            parts.append(f"[来源: {src}]")
        title = meta.get("paper_title", "") or meta.get("paper_id", "")
        if title:
            parts.append(f"[文档: {title}]")
        if meta.get("section"):
            parts.append(f"[章节: {meta['section']}]")
        ps = meta.get("page_start")
        pe = meta.get("page_end")
        if ps is not None and pe is not None:
            parts.append(f"[页码: p.{ps}-{pe}]")
        parts.append(meta.get("section_title", "") or doc.page_content)
        return "\n".join(parts)

    def _compute_metadata_score(self, query: str, doc: Document) -> float:
        """计算 query 与 document metadata 的结构化匹配分（0-1）"""
        score = 0.0
        meta = doc.metadata
        content = doc.page_content
        pid = meta.get("paper_id", "")
        title = meta.get("paper_title", "") or ""

        # 论文名匹配（权重最高）
        for kw in PAPER_NAME_KEYWORDS:
            if kw in query and (kw in title or kw in pid):
                score += self.meta_score_program
                break

        # 章节匹配
        doc_section = meta.get("section", "")
        for kw, sec in SECTION_INTENT_MAP.items():
            if kw in query and sec == doc_section:
                score += self.meta_score_section
                break

        # 关键词覆盖率（query 中的关键词在 chunk 中的覆盖比例）
        query_tokens = re.findall(r"[一-鿿]{2,}|\w{2,}", query)
        if query_tokens:
            hit = sum(1 for t in query_tokens if t in content)
            coverage = hit / len(query_tokens)
            score += self.meta_score_keyword * coverage

        return min(score, 1.0)

    def rerank(self, query: str, documents: list[Document], top_k: int | None = None) -> list[Document]:
        """对候选文档重排序 + metadata-aware score fusion"""
        if not self.enabled or not documents:
            return documents

        top_k = top_k or chroma_conf.get("rerank_top_k", 8)

        # 增强 passage 模式
        passages = [self._build_passage(d) for d in documents] if self.passage_mode else [d.page_content for d in documents]

        try:
            payload = json.dumps({
                "model": self.model,
                "query": query,
                "documents": passages,
                "top_n": min(top_k * 3, len(documents)),
            }).encode("utf-8")

            req = urllib.request.Request(
                self.url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())

            # 构建 reranker_score 映射（归一到 0-1）
            api_results = result.get("results", [])
            reranker_scores: dict[int, float] = {}
            max_api_score = max((item.get("relevance_score", 0) for item in api_results), default=1.0)
            for item in api_results:
                idx = item["index"]
                if idx < len(documents):
                    reranker_scores[idx] = item.get("relevance_score", 0) / max(max_api_score, 0.001)

            # Metadata-aware score fusion
            self.last_reranker_scores = []
            self.last_metadata_scores = []
            self.last_fusion_scores = []

            fusion_scores: dict[int, float] = {}
            for i in range(len(documents)):
                rs = reranker_scores.get(i, 0.0)
                ms = self._compute_metadata_score(query, documents[i]) if self.fusion_enabled else 0.0
                fs = self.alpha * rs + (1 - self.alpha) * ms if self.fusion_enabled else rs
                fusion_scores[i] = fs
                self.last_reranker_scores.append(rs)
                self.last_metadata_scores.append(ms)
                self.last_fusion_scores.append(fs)

            # 有效分过滤 + 排序
            valid = [(i, fusion_scores[i]) for i in fusion_scores
                     if reranker_scores.get(i, 0) > self.min_score]
            valid.sort(key=lambda x: x[1], reverse=True)

            if len(valid) >= top_k:
                selected = [documents[i] for i, _ in valid[:top_k]]
            elif len(valid) > 0:
                selected = [documents[i] for i, _ in valid]
                valid_set = {i for i, _ in valid}
                for i in range(len(documents)):
                    if len(selected) >= top_k:
                        break
                    if i not in valid_set:
                        selected.append(documents[i])
            elif self.fallback_enabled:
                selected = list(documents[:top_k])
            else:
                selected = []

            logger.debug(f"[Reranker]重排序：{len(documents)} → {len(selected)} 篇"
                         f"（fusion={self.fusion_enabled} alpha={self.alpha}）")
            return selected

        except Exception as e:
            logger.warning(f"[Reranker]API 异常，回退 RRF 排序：{e}")
            return documents[:top_k]

    def score_batch(self, query: str, documents: list[Document]) -> dict[int, float]:
        """返回所有文档的归一化 reranker 分数 {index: score}，不做过滤/截断"""
        if not documents or not self.api_key:
            return {}
        passages = [self._build_passage(d) for d in documents] if self.passage_mode else [d.page_content for d in documents]
        try:
            payload = json.dumps({
                "model": self.model,
                "query": query,
                "documents": passages,
                "top_n": len(documents),
            }).encode("utf-8")
            req = urllib.request.Request(
                self.url, data=payload,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
            api_results = result.get("results", [])
            max_s = max((item.get("relevance_score", 0) for item in api_results), default=1.0)
            return {item["index"]: item.get("relevance_score", 0) / max(max_s, 0.001) for item in api_results}
        except Exception as e:
            logger.warning(f"[Reranker.score_batch] API error: {e}")
            return {}


class HybridScorer:
    """混合保底打分器：BM25(45%) + Reranker(25%) + Keyword(20%) + Metadata(10%)
    Reranker 不作为硬截断器，BM25 高分 chunk 受保护不被洗掉。

    生产路径使用 HybridRetriever → Reranker.rerank()；
    本类保留用于 evaluation/ 下的检索消融实验对比，非生产检索链路。"""

    def __init__(self, bm25_store: "BM25Store", reranker: Reranker):
        self.bm25 = bm25_store
        self.reranker = reranker
        self.w_bm25 = 0.45
        self.w_rerank = 0.25
        self.w_keyword = 0.20
        self.w_metadata = 0.10
        self.bm25_safeguard_n = 5  # BM25 top-N 保证进入最终结果

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        tokens = list(jieba.cut(text))
        return [t.strip().lower() for t in tokens if len(t.strip()) > 1]

    @staticmethod
    def _keyword_overlap(query: str, content: str) -> float:
        """query 中的实词在 chunk 中的覆盖率"""
        qt = set(HybridScorer._tokenize(query))
        if not qt:
            return 0.0
        ct = set(HybridScorer._tokenize(content))
        return len(qt & ct) / len(qt)

    @staticmethod
    def _metadata_boost(query: str, doc: Document) -> float:
        """学术论文章节意图匹配加分（0-0.1）"""
        boost = 0.0
        meta = doc.metadata
        query_lower = query.lower()

        # 章节匹配：method / experiment / results 意图 → 同 section chunk 加分
        section_intent = {
            "method": ["method", "methodology", "approach", "design", "implementation",
                       "方法", "技术方案", "模型设计", "workflow", "步骤", "流程"],
            "experiment": ["experiment", "evaluation", "实验", "评估", "benchmark", "accuracy"],
            "results": ["results", "结果", "performance", "accuracy", "achieve"],
        }
        doc_sec = meta.get("section", "")
        for intent_sec, keywords in section_intent.items():
            if any(kw in query_lower for kw in keywords) and doc_sec == intent_sec:
                boost += 0.06
                break

        # 标题/摘要匹配加分
        title = (meta.get("paper_title", "") or meta.get("source_file", "")).lower()
        qt = set(HybridScorer._tokenize(query_lower))
        title_tokens = set(HybridScorer._tokenize(title))
        if qt and title_tokens:
            boost += 0.04 * len(qt & title_tokens) / len(qt)

        return min(boost, 0.10)

    def retrieve(self, query: str, bm25_k: int = 50, top_k: int = 20) -> list[Document]:
        """Stage 1: BM25 → Stage 2+3+4: 混合打分 → 排序 + BM25 保底"""
        bm25_results = self.bm25.search(query, bm25_k)
        if not bm25_results:
            return []

        documents = [d for d, _ in bm25_results]
        bm25_scores = {i: s for i, (_, s) in enumerate(bm25_results)}

        # Reranker scores（全量不截断）
        rerank_scores = self.reranker.score_batch(query, documents)

        # 逐文档混合打分
        final_scores: dict[int, float] = {}
        for i, d in enumerate(documents):
            kw = self._keyword_overlap(query, d.page_content)
            meta = self._metadata_boost(query, d)
            final_scores[i] = (
                self.w_bm25 * bm25_scores.get(i, 0)
                + self.w_rerank * rerank_scores.get(i, 0)
                + self.w_keyword * kw
                + self.w_metadata * meta
            )

        # 按混合分排序
        ranking = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

        # BM25 保底：top-N 必须进入最终 top_k
        bm25_top = {i for i, _ in sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)[:self.bm25_safeguard_n]}

        selected: list[Document] = []
        selected_idx: set[int] = set()
        for i, _ in ranking:
            if len(selected) >= top_k:
                break
            if i not in selected_idx:
                selected.append(documents[i])
                selected_idx.add(i)

        for i in sorted(bm25_top):
            if i not in selected_idx and len(selected) < top_k:
                selected.append(documents[i])
                selected_idx.add(i)

        return selected[:top_k]

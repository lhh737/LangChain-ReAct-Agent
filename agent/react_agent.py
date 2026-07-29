"""ReAct Agent — 多意图、状态感知、7 工具、流式输出、三层记忆"""
import json
import os
import re
import time
import jieba
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Generator

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

from model.factory import chat_model
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

from agent.intent_router import IntentRouter, Intent
from agent.retrieval_state import AgentRetrievalState
from agent.execution_policy import AgentExecutionPolicy
from agent.memory_manager import ShortTermMemory, CumulativeSummary, FactStore
from agent.tools.agent_tools import (
    academic_search, search_academic_papers, fetch_paper_metadata,
    fetch_citation_info, compare_papers, mark_paper_not_in_kb,
    start_literature_review, _search_academic_papers_internal,

)
from agent.retrieval.retrieval_pipeline import search_academic_papers_core
from agent.evidence_budgeter import (
    EvidenceBudgeter, TokenCounter, build_local_blocks, build_online_blocks,
)
from agent.tools.middleware import AgentCallback


@dataclass
class EvidenceItem:
    """单条证据项：逐 subject 的证据收集结果"""
    subject: str
    content: str
    source: str  # "local" / "local_retry" / "online" / "online_fallback" / "duplicate"
    is_missing: bool = False
    is_soft_miss: bool = False
    quality: dict = field(default_factory=dict)
    chunks: list = field(default_factory=list)  # raw Document chunks from local retrieval


class ReactAgent:
    def __init__(self):
        self.callback = AgentCallback()

        # 记忆系统
        self.memory = ShortTermMemory()
        self.summary = CumulativeSummary()
        self.fact_store = FactStore()

        # 意图路由
        self.intent_router = IntentRouter()

        # per-execution 状态（在 execute_stream 中重置）
        self._retrieval_state: AgentRetrievalState | None = None
        self._execution_policy: AgentExecutionPolicy | None = None
        self._current_intent: Intent = Intent.QA


    def _load_prompt(self, intent: Intent) -> str:
        file_map = {
            Intent.QA: "prompts/academic_main.txt",
            Intent.COMPARE: "prompts/paper_comparison.txt",
            Intent.REVIEW: "prompts/review.txt",
        }
        path = get_abs_path(file_map.get(intent, file_map[Intent.QA]))
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # ── KB Missing 索引 ──

    _kb_missing_cache: dict | None = None

    def _load_kb_missing_papers(self) -> dict:
        if self._kb_missing_cache is not None:
            return self._kb_missing_cache
        path = get_abs_path("data/kb_missing_papers.json")
        if not os.path.exists(path):
            self._kb_missing_cache = {}
            return {}
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._kb_missing_cache = data.get("papers", {})
        return self._kb_missing_cache

    def _match_kb_missing(self, subject: str) -> dict | None:
        papers = self._load_kb_missing_papers()
        if not papers:
            return None
        subj_lower = subject.strip().lower()
        for key, paper in papers.items():
            display = (paper.get("display_name") or "").lower()
            if subj_lower in key or key in subj_lower or subj_lower in display:
                logger.info(f"[KBMissing] 命中: {subject} → {paper.get('display_name', key)}")
                return paper
            for alias in paper.get("aliases", []):
                if subj_lower in alias.lower() or alias.lower() in subj_lower:
                    logger.info(f"[KBMissing] 命中(alias): {subject} → {paper.get('display_name', key)}")
                    return paper
        logger.info(f"[KBMissing] 未命中: {subject}")
        return None

    # ── Candidate Extraction ──

    def _extract_candidates(self, query: str) -> list[str]:
        prompt = (
            "从以下用户问题中提取所有论文名、方法名、系统名，每行一个。"
            "如果没有明确名称，输出 NONE。\n"
            f"问题：{query}\n输出："
        )
        raw = ""
        for chunk in chat_model.stream(prompt, config={"callbacks": [self.callback]}):
            if chunk.content and isinstance(chunk.content, str):
                raw += chunk.content
        candidates = [t.strip() for t in raw.strip().split("\n") if t.strip() and t.strip().upper() != "NONE"]
        logger.info(f"[Candidates] {candidates}")
        return candidates

    def _llm_rewrite_query(self, query: str) -> str:
        prompt = (
            "以下问题在英文学术论文库中检索不到相关内容，请将问题改写为不同的英文学术检索关键词。"
            "只输出改写后的检索词，不要解释。\n"
            f"原问题：{query}\n改写："
        )
        rewritten = ""
        for chunk in chat_model.stream(prompt):
            if chunk.content and isinstance(chunk.content, str):
                rewritten += chunk.content
        return rewritten.strip()

    def _build_online_query(self, query: str, subject: str) -> str:
        """从自然语言问句中提取领域关键词，拼成 '论文名 关键词' 格式用于学术检索"""
        if not subject:
            from rag.rag_service import RagSummarizeService
            return RagSummarizeService()._translate_query(query)
        prompt = (
            "从以下研究问题中提取2-3个最核心的英文学术领域关键词（不含论文名/方法名本身），"
            "用空格分隔。只输出关键词，不要解释。\n"
            f"问题：{query}\n关键词："
        )
        keywords = ""
        for chunk in chat_model.stream(prompt):
            if chunk.content and isinstance(chunk.content, str):
                keywords += chunk.content
        keywords = keywords.strip()
        if keywords:
            return f"{subject} {keywords}"
        return subject

    @staticmethod
    def _strip_pipeline_numbering(text: str) -> str:
        """清除在线检索输出中的 [N] 编号前缀，避免与统一引用编号冲突"""
        return re.sub(r'^\[\d+\]\s*', '', text, flags=re.MULTILINE)

    @staticmethod
    def _build_review_online_blocks(
        scored_results,
        max_papers: int = 30,
    ) -> list[dict]:
        """从 scored_results 构建独立 EvidenceBlock 输入列表。

        每篇论文一个独立 block，包含完整引用元数据。
        去重、过滤无摘要论文、保留质量分、上限截断。
        """
        from agent.retrieval.paper_validator import PaperIdentityValidator

        blocks = []
        seen: set[str] = set()

        ranked = sorted(
            scored_results,
            key=lambda item: item[1],
            reverse=True,
        )

        for paper, score in ranked:
            title = (paper.title or "").strip()
            abstract = (paper.abstract or "").strip()
            doi = (paper.doi or "").strip()
            url = (paper.url or "").strip()

            # Dedup key: prefer DOI, fallback to normalized title
            dedup_key = (
                PaperIdentityValidator._normalize_doi(doi)
                if doi
                else PaperIdentityValidator._normalize_title(title)
            )
            if not dedup_key or dedup_key in seen:
                continue
            seen.add(dedup_key)

            # Skip papers without evidence text
            if not abstract:
                logger.info(
                    "[ReviewEvidence] skip paper without evidence text: %s",
                    title,
                )
                continue

            blocks.append({
                "title": title or "未命名论文",
                "source": paper.source or "在线学术检索",
                "content": abstract,
                "quality_score": float(score),
                "authors": list(paper.authors or []),
                "year": paper.year or "",
                "doi": doi,
                "url": url,
                "evidence_type": "abstract",
            })

            if len(blocks) >= max_papers:
                break

        logger.info(
            "[ReviewEvidence] scored=%d candidates=%d max=%d",
            len(scored_results), len(blocks), max_papers,
        )
        return blocks


    # ── COMPARE: 对比维度提取 + 逐 subject 证据判断 ──

    def _extract_compare_aspects(self, query: str) -> str:
        """从用户对比问题中提取核心对比维度（英文关键词），仅 COMPARE 调用一次"""
        prompt = (
            "从以下用户问题中提取所有对比维度，输出对应的英文学术关键词（空格分隔，不超过 8 个词）。\n"
            "如：攻击目标→attack goal target；攻击手段→attack method technique；威胁模型→threat model\n"
            f"问题：{query}\n关键词："
        )
        aspects = ""
        for chunk in chat_model.stream(prompt, config={"callbacks": [self.callback]}):
            if chunk.content and isinstance(chunk.content, str):
                aspects += chunk.content
        result = aspects.strip()
        logger.info(f"[CompareAspects] {result}")
        return result

    def _judge_subject_evidence(self, docs: list, subject: str, aspects: str) -> dict:
        """逐 subject 判断：是否命中目标论文 + 证据是否覆盖对比维度 + 缺失信息 + 改写建议"""
        if not docs:
            return {"sufficient": False, "paper_hit": False, "missing_dimensions": "",
                    "refine_query": f"{subject} {aspects}"}

        chunks_text = ""
        for i, doc in enumerate(docs[:8], 1):
            meta = doc.metadata
            title = meta.get("paper_title", "?")
            section = meta.get("section", "?")
            ps = meta.get("page_start") or meta.get("page")
            pe = meta.get("page_end") or meta.get("page")
            page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}"
            chunks_text += f"[{i}] 《{title}》| {section} | {page}\n{doc.page_content[:500]}\n\n"

        prompt = (
            f"论文名：{subject}\n"
            f"对比维度：{aspects}\n\n"
            f"检索到的片段：\n{chunks_text}\n"
            "请判断：\n"
            f"1. 是否命中了目标论文「{subject}」的原文？（PAPER_HIT: YES/NO）\n"
            "2. 相关片段是否足够覆盖对比维度？逐一检查每个维度是否有证据。（SUFFICIENT 或 INSUFFICIENT: 缺少xxx维度）\n"
            "3. 如不足，给出英文改写检索词（REFINE_QUERY: xxx）\n"
        )

        judgment = ""
        for chunk in chat_model.stream(prompt, config={"callbacks": [self.callback]}):
            if chunk.content and isinstance(chunk.content, str):
                judgment += chunk.content

        judgment_clean = judgment.strip().rstrip("*").rstrip()

        paper_hit = "PAPER_HIT: YES" in judgment_clean.upper() or "PAPER_HIT:YES" in judgment_clean.upper()
        sufficient = "SUFFICIENT" in judgment_clean.upper() and "INSUFFICIENT" not in judgment_clean.upper()

        m_missing = re.search(r"INSUFFICIENT:\s*(.+?)(?:\n|$)", judgment_clean, re.IGNORECASE)
        missing_dimensions = m_missing.group(1).strip().rstrip("*").rstrip() if m_missing else ""

        # 用 _llm_rewrite_query 根据缺失维度生成改写检索词，而非从 LLM 输出正则提取
        if not sufficient and paper_hit and missing_dimensions:
            refine_query = self._llm_rewrite_query(
                f"论文「{subject}」的对比维度：{aspects}。当前检索缺失：{missing_dimensions}"
            )
        else:
            refine_query = f"{subject} {aspects}"

        return {
            "sufficient": sufficient,
            "paper_hit": paper_hit,
            "missing_dimensions": missing_dimensions,
            "refine_query": refine_query,
        }

    # ── LLM Chunk Judge ──

    def _llm_judge_chunks(self, chunks: list, query: str) -> Generator[dict, None, dict]:
        """LLM 逐 chunk 判断相关性 + 充分性 + 生成 refine_query"""
        yield {"type": "system", "content": "正在分析检索质量...", "name": "system"}
        if not chunks:
            yield {"type": "text", "content": "[系统] 未检索到任何 chunk", "name": "system"}
            return {"sufficient": False, "relevant_chunks": [], "refine_query": query, "judgment": ""}

        chunks_text = ""
        for i, doc in enumerate(chunks, 1):
            meta = doc.metadata
            title = meta.get("paper_title", "?")
            section = meta.get("section", "?")
            ps = meta.get("page_start") or meta.get("page")
            pe = meta.get("page_end") or meta.get("page")
            page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}"
            chunks_text += f"[{i}] 《{title}》| {section} | {page}\n{doc.page_content}\n\n"

        prompt = (
            "你是一个严格的检索质量评估器。请逐个检查以下检索到的论文片段是否与用户问题相关。\n\n"
            f"用户问题：{query}\n\n"
            "检索片段：\n"
            f"{chunks_text}\n"
            "请完成以下任务：\n"
            "1. 逐个判断每个片段是否与问题相关，输出格式：[N] [相关]/[不相关] — 一句话理由\n"
            "2. 综合判断：相关片段是否足够回答用户问题？输出：SUFFICIENT 或 INSUFFICIENT:<缺少什么信息>\n"
            "3. 如果 INSUFFICIENT，提供一个改写后的英文检索查询，输出：REFINE_QUERY: <english_query>\n"
        )

        judgment = ""
        for chunk in chat_model.stream(prompt, config={"callbacks": [self.callback]}):
            if chunk.content and isinstance(chunk.content, str):
                judgment += chunk.content

        sufficient = "SUFFICIENT" in judgment.upper() and "INSUFFICIENT" not in judgment.upper()

        # Multi-format parsing: relevant + irrelevant
        relevant_indices: set[int] = set()
        irrelevant_indices: set[int] = set()

        # Patterns ordered: try "不相关" before "相关" to avoid substring match
        irrelevant_patterns = [
            r"\[(\d+)\]\s*\[不相关\]",
            r"\[(\d+)\]\s*不相关",
            r"^\s*(\d+)[\.、:：]\s*\[?不相关\]?",
        ]
        for pat in irrelevant_patterns:
            for m in re.finditer(pat, judgment, re.MULTILINE | re.IGNORECASE):
                irrelevant_indices.add(int(m.group(1)))

        relevant_patterns = [
            r"\[(\d+)\]\s*\[相关\]",
            r"\[(\d+)\]\s*相关",
            r"^\s*(\d+)[\.、:：]\s*\[?相关\]?",
        ]
        # Only mark as relevant if not already marked irrelevant
        for pat in relevant_patterns:
            for m in re.finditer(pat, judgment, re.MULTILINE | re.IGNORECASE):
                idx = int(m.group(1))
                if idx not in irrelevant_indices:
                    relevant_indices.add(idx)

        relevant_chunks = [chunks[i - 1] for i in sorted(relevant_indices) if 1 <= i <= len(chunks)]
        irrelevant_chunks = [chunks[i - 1] for i in sorted(irrelevant_indices) if 1 <= i <= len(chunks)]

        # Coverage check
        expected = set(range(1, len(chunks) + 1))
        parsed = relevant_indices | irrelevant_indices
        unparsed_indices = expected - parsed
        unparsed_chunks = [chunks[i - 1] for i in sorted(unparsed_indices) if 1 <= i <= len(chunks)]
        parse_ok = len(unparsed_indices) == 0

        refine_query = query
        m_refine = re.search(r"REFINE_QUERY:\s*(.+?)(?:\n|$)", judgment, re.IGNORECASE)
        if m_refine:
            raw_rq = m_refine.group(1).strip()
            # Reject placeholder values
            if raw_rq and raw_rq not in ("<english_query>", "<query>", "english_query", "query"):
                refine_query = raw_rq
            else:
                logger.warning(
                    "[JudgeRefine] placeholder detected in refine_query: %r, using original query",
                    raw_rq,
                )

        # Invariant: sufficient=True + zero relevant_chunks is invalid
        judge_failed = False
        if sufficient and not relevant_chunks and chunks:
            logger.error(
                "[JudgeInvariant] sufficient=True but relevant_chunks is empty; "
                "forcing sufficient=False. raw_judgment=%r",
                judgment[:500],
            )
            sufficient = False
            parse_ok = False
            judge_failed = True

        # Also treat complete parse failure as judge_failed
        if not relevant_indices and not irrelevant_indices and chunks:
            judge_failed = True

        result = {
            "sufficient": sufficient,
            "relevant_chunks": relevant_chunks,
            "irrelevant_chunks": irrelevant_chunks,
            "unparsed_chunks": unparsed_chunks,
            "refine_query": refine_query,
            "judgment": judgment,
            "parse_ok": parse_ok,
            "judge_failed": judge_failed,
            "raw_response": judgment,
        }
        logger.info(
            "[QATrace][judge] sufficient=%s relevant=%d irrelevant=%d unparsed=%d "
            "parse_ok=%s judge_failed=%s refine_query=%r chunks_input=%d",
            sufficient, len(relevant_chunks), len(irrelevant_chunks), len(unparsed_chunks),
            parse_ok, judge_failed, (refine_query or "")[:200], len(chunks),
        )
        if relevant_chunks:
            logger.info("[QATrace][judge_relevant] %d chunks retained", len(relevant_chunks))
            for idx, chunk in enumerate(relevant_chunks[:5], 1):
                meta = chunk.metadata
                logger.info(
                    "[QATrace][judge_relevant:%d] title=%r section=%r page=%r",
                    idx,
                    meta.get("paper_title", ""),
                    meta.get("section", ""),
                    meta.get("page_start") or meta.get("page", ""),
                )
        if irrelevant_chunks:
            logger.info("[QATrace][judge_irrelevant] %d chunks dropped", len(irrelevant_chunks))
        if unparsed_chunks:
            logger.warning(
                "[QATrace][judge_unparsed] %d chunks could not be classified: %s",
                len(unparsed_chunks),
                sorted(unparsed_indices),
            )

        logger.info(
            "[QATrace][judge_raw] %r",
            judgment[:500],
        )
        return result

    # ── Generate Answer from Raw Chunks ──

    def _generate_answer_from_chunks(
        self, chunks: list, query: str, intent: Intent, extra_context: str = "",
        max_chunks: int = 0, max_tokens: int = 5000, memory_context: str = "",
        online_blocks: list | None = None,
    ) -> Generator[dict, None, None]:
        """从 raw chunks + online_blocks 构建统一编号引用上下文，生成答案。
        online_blocks: [{"title": str, "source": str, "content": str}, ...]
        max_tokens 控制上下文整体 token 上限。
        memory_context 为相关性过滤后的历史对话 + 长期事实。"""
        online_blocks = online_blocks or []
        for block in online_blocks:
            block["content"] = self._strip_pipeline_numbering(block.get("content", ""))

        logger.info("[QATrace][before_generate] local_chunks=%d online_blocks=%d extra_context_len=%d",
                    len(chunks), len(online_blocks), len(extra_context or ""))

        if not chunks and not extra_context and not online_blocks:
            logger.warning("[QATrace][branch] no_evidence all empty")
            yield {"type": "text", "content": "[系统] 无可用检索结果", "name": "system"}
            return

        # 条数上限
        ctx_chunks = chunks[:max_chunks] if max_chunks > 0 else chunks

        # ── EvidenceBudgeter: 分层 token 预算分配 ──
        token_counter = TokenCounter()
        local_evidence = build_local_blocks(ctx_chunks, token_counter)
        online_evidence = build_online_blocks(online_blocks, token_counter)

        # === CitationTrace: EvidenceBlock after build_online_blocks ===
        logger.info("[CitationTrace][evidence_blocks] count=%d", len(online_evidence))
        for idx, block in enumerate(online_evidence):
            logger.info(
                "[CitationTrace][evidence_block:%d] id=%s title=%r raw_len=%d newline_count=%d",
                idx, block.evidence_id, block.citation_meta.get("title", "未知"),
                len(block.raw_content or ""), (block.raw_content or "").count("\n"),
            )
        # === end CitationTrace ===

        online_available = bool(online_blocks)

        budgeter = EvidenceBudgeter()
        system_prompt = self._load_prompt(intent)
        allocation = budgeter.allocate(
            system_prompt=system_prompt,
            query=query,
            local_blocks=local_evidence,
            online_blocks=online_evidence,
            memory_context=memory_context,
            extra_context=extra_context,
            online_available=online_available,
        )

        # === CitationTrace: after EvidenceBudgeter.allocate() ===
        logger.info(
            "[CitationTrace][allocation] selected=%d references=%d context_len=%d context_newlines=%d",
            len(allocation.selected_blocks), len(allocation.references),
            len(allocation.context), allocation.context.count("\n"),
        )
        for idx, ref_text in enumerate(allocation.references):
            logger.info(
                "[CitationTrace][reference:%d] len=%d newline_count=%d",
                idx + 1, len(ref_text), ref_text.count("\n"),
            )
        logger.info(
            "[CitationTrace][allocation_context] len=%d",
            len(allocation.context),
        )
        # === end CitationTrace ===

        # ── 使用 budgeter 分配结果 ──
        context = allocation.context
        system_msg = SystemMessage(content=system_prompt)
        user_msg = HumanMessage(content=f"用户问题：{query}\n\n检索结果：\n{context}")

        collected_text: list[str] = []
        for chunk in chat_model.stream([system_msg, user_msg], config={"callbacks": [self.callback]}):
            if chunk.content and isinstance(chunk.content, str):
                collected_text.append(chunk.content)
                yield {"type": "text", "content": chunk.content, "name": "assistant"}

        final_text = "".join(collected_text)

        # 引用校验（统一编号：本地 N 个 + 在线 M 个）
        max_n = len(allocation.selected_blocks)
        cited = set(int(m) for m in re.findall(r"\[(\d+)\]", final_text))
        invalid = sorted(n for n in cited if n < 1 or n > max_n)
        if invalid:
            yield {"type": "text", "content": f"\n\n> 引用校验警告：无效引用 {invalid}，有效范围 [1-{max_n}]。", "name": "system"}

        # 有证据但零引用 → 警告
        if max_n > 0 and not cited:
            logger.warning("[Citation] 有 chunk 但回答零引用")
            yield {"type": "text", "content": "\n\n> 引用校验警告：回答未引用任何证据编号，请忽略以上回答并重新提问。", "name": "system"}
            return

        # 占位符检测
        if any(re.search(pat, final_text) for pat in [r"\[N\]", r"\[n\]", r"\[数字\]", r"\[编号\]", r"\[\?\]"]):
            logger.warning("[Placeholder] 检测到占位符引用")
            yield {"type": "text", "content": "\n[系统提示] 回答中包含无效引用占位符，已拦截。\n", "name": "system"}
            return

        # 输出引用来源（基于 allocation.selected_blocks 的完整渲染）
        if max_n > 0:
            ref_lines = []
            structured_refs = []
            for ref_num, block in enumerate(allocation.selected_blocks, 1):
                rendered = block.render(ref_num)
                ref_lines.append(rendered)
                meta = block.citation_meta
                structured_refs.append({
                    "index": ref_num,
                    "title": meta.get("title", "未知"),
                    "source_type": block.source_type,
                    "source": meta.get("source", "未知"),
                    "authors": meta.get("authors", []),
                    "year": meta.get("year", ""),
                    "doi": meta.get("doi", ""),
                    "url": meta.get("url", ""),
                    "evidence_type": meta.get("evidence_type", "abstract"),
                    "evidence_text": block.raw_content,
                })
            reference_content = "\n\n".join(ref_lines)
            logger.info(
                "[CitationTrace][yield_references] content_len=%d newline_count=%d structured_count=%d",
                len(reference_content), reference_content.count("\n"), len(structured_refs),
            )
            yield {
                "type": "references",
                "content": reference_content,
                "references": structured_refs,
                "name": "system",
            }

        # 记忆更新
        if final_text.strip():
            self.memory.add_turn(query, final_text)
            if self.memory.should_compress():
                recent = "\n".join(m["content"][:300] for m in self.memory.buffer[-8:])
                self.summary.update(recent, chat_model)
            total_turns = self.memory.turn_count()
            if total_turns > 0 and total_turns % FactStore.EXTRACT_INTERVAL == 0:
                new_facts = self.fact_store.extract_facts(self.memory.buffer)
                if new_facts:
                    self.fact_store.add_facts("research", new_facts)

    # ── Shared Evidence Layer ──

    def _collect_evidence_for_subject(
        self, subject: str, query: str, guards: dict
    ) -> Generator[dict, None, EvidenceItem]:
        from rag.rag_service import RagSummarizeService
        rag = RagSummarizeService()

        search_query = query  # 始终用原始 query 检索，不用 subject

        # Guard 3: 防重复
        if search_query in guards["queries_issued"]:
            logger.info(f"[Evidence] 重复 query，跳过: {search_query}")
            return EvidenceItem(subject=subject, content="", source="duplicate")
        guards["queries_issued"].add(search_query)

        # Step 0: 预检 KB 缺失索引
        missing = self._match_kb_missing(subject if subject else query)
        if missing:
            online_q = missing.get("online_query") or missing.get("display_name", search_query)
            online_result = search_academic_papers_core(online_q, candidate=subject if subject else "")
            self.callback.tool_invocation_log.append({
                "name": "search_academic_papers", "output": online_result.text,
                "elapsed": 0, "status": "success",
            })
            guards["online_done"] = True
            yield {
                "type": "tool", "content": online_result.text[:500], "name": "search_academic_papers",
                "query": online_q, "elapsed": 0,
                "meta": {"papers": online_result.papers_meta()},
            }
            display = missing.get("display_name", subject)
            context = f"[在线检索] 论文「{display}」不在本地 KB 中：\n{online_result.text}"
            if missing.get("abstract"):
                context += f"\n\n预存元数据：摘要={missing['abstract']}"
            return EvidenceItem(subject=subject, content=context, source="online", is_missing=True)

        # Guard 1: 本地 KB 已禁用 → 交给调用方决定是否在线
        if guards["local_kb_disabled"]:
            logger.info(f"[Evidence] 本地 KB 已禁用，跳过: {search_query}")
            return EvidenceItem(subject=subject, content="", source="local_disabled", is_soft_miss=True)

        # Step 1: 第一次本地检索 → 返回原始 chunks
        try:
            docs1 = rag.retriever_docs(search_query)
        except Exception as e:
            logger.warning(f"[Evidence] 本地检索失败: {e}")
            docs1 = []

        quality1 = rag._check_retrieval_quality(search_query, docs1)
        preview1 = docs1[0].page_content[:200] if docs1 else ""
        self.callback.tool_invocation_log.append({
            "name": "academic_search", "output": preview1,
            "elapsed": 0, "status": "success",
        })
        yield {
            "type": "tool", "content": preview1, "name": "academic_search",
            "query": search_query, "elapsed": 0,
            "meta": {
                "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                             "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                             "preview": d.page_content[:80]} for d in docs1[:8]],
                "count": len(docs1),
            },
        }
        logger.info(
            f"[Quality] subject={subject} soft_miss={quality1['is_soft_miss']} "
            f"signals={quality1.get('signals', {})}"
        )

        if not quality1["is_soft_miss"]:
            return EvidenceItem(subject=subject, content="", source="local",
                              quality=quality1, chunks=docs1)

        # 软 miss → 改写 query 再试一次
        guards["miss_count"] = guards.get("miss_count", 0) + 1
        rewritten = self._llm_rewrite_query(search_query)
        if rewritten and rewritten not in guards["queries_issued"]:
            guards["queries_issued"].add(rewritten)
            try:
                docs2 = rag.retriever_docs(rewritten)
            except Exception as e:
                logger.warning(f"[Evidence] 改写检索失败: {e}")
                docs2 = []

            quality2 = rag._check_retrieval_quality(rewritten, docs2)
            preview2 = docs2[0].page_content[:200] if docs2 else ""
            self.callback.tool_invocation_log.append({
                "name": "academic_search", "output": preview2,
                "elapsed": 0, "status": "success",
            })
            yield {
                "type": "tool", "content": preview2, "name": "academic_search",
                "query": rewritten, "elapsed": 0,
                "meta": {
                    "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                                 "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                                 "preview": d.page_content[:80]} for d in docs2[:8]],
                    "count": len(docs2),
                },
            }

            if not quality2["is_soft_miss"]:
                return EvidenceItem(subject=subject, content="", source="local_retry",
                                  quality=quality2, chunks=docs2)

        # 连续两次软 miss → 禁用本地 KB
        guards["miss_count"] = guards.get("miss_count", 0) + 1
        if guards["miss_count"] >= 2:
            guards["local_kb_disabled"] = True
            logger.warning(f"[Guard] 本地 KB 已禁用，miss_count={guards['miss_count']}")

        # 返回软 miss（chunks 仍保留，供调用方 LLM judge 二次判断）
        return EvidenceItem(subject=subject, content="", source="local",
                          is_soft_miss=True, quality=quality1, chunks=docs1)

    # ── QA Pipeline (三轮：本地检索 → LLM judge → refine → judge → 在线兜底) ──

    def _execute_qa_pipeline(self, query: str) -> Generator[dict, None, None]:
        from rag.rag_service import RagSummarizeService
        rag = RagSummarizeService()

        yield {"type": "system", "content": "正在提取论文名称...", "name": "system"}
        candidates = self._extract_candidates(query)
        subject = candidates[0] if candidates else ""

        all_chunks: list = []
        issued: set[str] = set()

        # Step 0: KB 缺失预检
        missing = self._match_kb_missing(subject if subject else query)
        if missing:
            logger.info(f"[QA] KB缺失命中 → 在线检索")
            yield {"type": "system", "content": "正在在线检索论文...", "name": "system"}
            online_q = missing.get("online_query") or missing.get("display_name", query)
            online_result = search_academic_papers_core(online_q, candidate=subject if subject else "")
            logger.info(f"[QA] 在线检索完成 ({len(online_result.text)} chars)")
            self.callback.tool_invocation_log.append({
                "name": "search_academic_papers", "output": online_result.text,
                "elapsed": 0, "status": "success",
            })
            yield {
                "type": "tool", "content": online_result.text[:500], "name": "search_academic_papers",
                "query": online_q, "elapsed": 0,
                "meta": {"papers": online_result.papers_meta()},
            }
            display = missing.get("display_name", subject)
            content = online_result.text
            if missing.get("abstract"):
                content = f"摘要：{missing['abstract']}\n\n{content}"
            yield from self._generate_answer_from_chunks(
                [], query, Intent.QA, max_chunks=15, max_tokens=5000,
                memory_context=self._build_memory_context(query),
                online_blocks=[{"title": display, "source": "在线检索（KB缺失）", "content": content}],
            )
            return

        # Round 1: 本地检索
        issued.add(query)
        logger.info(f"[QA] Round1 检索query: {query[:200]}")
        try:
            docs1 = rag.retriever_docs(query)
        except Exception:
            docs1 = []
        preview1 = docs1[0].page_content[:200] if docs1 else ""
        self.callback.tool_invocation_log.append({
            "name": "academic_search", "output": preview1, "elapsed": 0, "status": "success",
        })
        yield {
            "type": "tool", "content": preview1, "name": "academic_search",
            "query": query, "elapsed": 0,
            "meta": {
                "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                             "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                             "preview": d.page_content[:80]} for d in docs1[:8]],
                "count": len(docs1),
            },
        }

        all_chunks = list(docs1)
        quality1 = rag._check_retrieval_quality(query, docs1)
        logger.info(
            f"[Quality] Round1 soft_miss={quality1['is_soft_miss']} "
            f"signals={quality1['signals']} max_score={quality1['max_score']:.3f} coverage={quality1['coverage']:.2f}"
        )

        # Round 1: LLM judge
        judge1 = yield from self._llm_judge_chunks(all_chunks, query)
        if judge1["sufficient"] and judge1["relevant_chunks"]:
            logger.info("[QATrace][branch] answer_after_round1 sufficient=True relevant=%d",
                        len(judge1["relevant_chunks"]))
            yield from self._generate_answer_from_chunks(judge1["relevant_chunks"], query, Intent.QA, max_chunks=15, max_tokens=5000, memory_context=self._build_memory_context(query))
            self._log_session_end("qa")
            return
        elif judge1["sufficient"] and not judge1["relevant_chunks"]:
            logger.error("[QATrace][branch] invariant_violation sufficient=True relevant=0, forcing insufficient")
        logger.info("[QATrace][branch] round1_insufficient relevant=%d refine_query=%r",
                    len(judge1.get("relevant_chunks") or []),
                    (judge1.get("refine_query") or "")[:200])

        # Retain round1 relevant evidence
        retained_local = list(judge1.get("relevant_chunks") or [])

        # Round 2: refine query 再检索
        refine_query = judge1.get("refine_query", query)
        if refine_query and refine_query != query and refine_query not in issued:
            issued.add(refine_query)
            logger.info(f"[QA] Round2 检索query: {refine_query[:200]}")
            try:
                docs2 = rag.retriever_docs(refine_query)
            except Exception:
                docs2 = []
            preview2 = docs2[0].page_content[:200] if docs2 else ""
            self.callback.tool_invocation_log.append({
                "name": "academic_search", "output": preview2, "elapsed": 0, "status": "success",
            })
            yield {
                "type": "tool", "content": preview2, "name": "academic_search",
                "query": refine_query, "elapsed": 0,
                "meta": {
                    "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                                 "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                                 "preview": d.page_content[:80]} for d in docs2[:8]],
                    "count": len(docs2),
                },
            }

            # 去重合并
            seen = {d.page_content[:120] for d in all_chunks}
            for d in docs2:
                if d.page_content[:120] not in seen:
                    all_chunks.append(d)
                    seen.add(d.page_content[:120])

            quality2 = rag._check_retrieval_quality(refine_query, docs2)
            logger.info(
                f"[Quality] Round2 soft_miss={quality2['is_soft_miss']} "
                f"signals={quality2['signals']} max_score={quality2['max_score']:.3f} coverage={quality2['coverage']:.2f}"
            )
        else:
            logger.info("[QATrace][branch] skip_round2 invalid refine_query=%r in_issued=%s",
                        (refine_query or "<empty>")[:200],
                        str(refine_query in issued) if refine_query else "N/A")

        # Round 2: 再次 judge (with merged chunks if round2 executed)
        judge2 = yield from self._llm_judge_chunks(all_chunks, query)
        if judge2["sufficient"] and judge2["relevant_chunks"]:
            logger.info("[QATrace][branch] answer_after_round2 sufficient=True relevant=%d",
                        len(judge2["relevant_chunks"]))
            yield from self._generate_answer_from_chunks(judge2["relevant_chunks"], query, Intent.QA, max_chunks=15, max_tokens=5000, memory_context=self._build_memory_context(query))
            self._log_session_end("qa")
            return

        # Merge round2 relevant into retained
        if judge2.get("relevant_chunks"):
            seen_ids = {id(c) for c in retained_local}
            for c in judge2["relevant_chunks"]:
                if id(c) not in seen_ids:
                    retained_local.append(c)
                    seen_ids.add(id(c))
        logger.info("[QATrace][branch] round2_insufficient merged_relevant=%d round1_relevant=%d round2_relevant=%d",
                    len(retained_local),
                    len(judge1.get("relevant_chunks") or []),
                    len(judge2.get("relevant_chunks") or []))

        # Round 3: 在线兜底
        missing = self._match_kb_missing(subject if subject else query)
        if missing and missing.get("abstract"):
            display = missing.get("display_name", subject)
            logger.info(f"[QA] kb_missing有摘要，跳过在线检索: {display}")
            content = f"摘要：{missing['abstract']}"
            if missing.get("url"):
                content += f"\n链接：{missing['url']}"
            if missing.get("authors"):
                content += f"\n作者：{', '.join(missing['authors'][:5])}"
            if missing.get("year"):
                content += f"\n年份：{missing['year']}"
            online_block = {"title": display, "source": "kb_missing", "content": content}
            yield {
                "type": "tool", "content": content[:500], "name": "kb_missing_abstract",
                "query": display, "elapsed": 0,
                "meta": {
                    "authors": missing.get("authors", []),
                    "year": missing.get("year", ""),
                    "venue": missing.get("venue", ""),
                    "doi": missing.get("doi", ""),
                    "url": missing.get("url", ""),
                },
            }
        else:
            if missing:
                online_q = missing.get("online_query") or missing.get("display_name", subject)
                logger.info(f"[QA] kb_missing命中，在线检索query: {online_q}")
            else:
                online_q = self._build_online_query(query, subject)
                logger.info(f"[QA] 在线兜底（无kb_missing），关键词query: {online_q}")
            yield {"type": "system", "content": "正在在线检索论文...", "name": "system"}
            online_result = search_academic_papers_core(online_q, candidate=subject if subject else "")
            logger.info(f"[QA] 在线检索结果 ({len(online_result.text)} chars): {online_result.text[:300]}")
            self.callback.tool_invocation_log.append({
                "name": "search_academic_papers", "output": online_result.text, "elapsed": 0, "status": "success",
            })
            yield {
                "type": "tool", "content": online_result.text[:500], "name": "search_academic_papers",
                "query": online_q, "elapsed": 0,
                "meta": {"papers": online_result.papers_meta()},
            }
            display = missing.get("display_name", query) if missing else "在线检索结果"
            online_block = {"title": display, "source": "在线检索", "content": online_result.text}

        logger.info("[QATrace][branch] online_fallback local_chunks=%d online_blocks=1",
                    len(retained_local))
        yield from self._generate_answer_from_chunks(
            retained_local, query, Intent.QA, max_chunks=15, max_tokens=5000,
            memory_context=self._build_memory_context(query),
            online_blocks=[online_block],
        )
        self._log_session_end("qa")

    def _log_session_end(self, intent_name: str):
        tools_count = len(self.callback.tool_invocation_log)
        logger.warning(f"[SessionEnd] intent={intent_name} tools={tools_count}")

    # ── COMPARE Pipeline (逐 subject 检索 → 独立 judge → 两轮上限 → 15 chunk 均衡分配) ──

    def _process_compare_subject(self, subject: str, aspects: str) -> dict:
        """处理单个 subject 的检索+judge（线程安全，不 yield）"""
        from rag.rag_service import RagSummarizeService
        rag = RagSummarizeService()

        result: dict = {
            "subject": subject,
            "chunks": [],
            "online_block": None,
            "chunk_count": 0,
            "tool_logs": [],
            "tool_previews": [],
        }

        # Step 0: KB 缺失预检
        missing = self._match_kb_missing(subject)
        if missing:
            display = missing.get("display_name", subject)
            if missing.get("abstract"):
                logger.info(f"[Compare] {subject} kb_missing有摘要，跳过在线检索")
                content = f"摘要：{missing['abstract']}"
                if missing.get("url"):
                    content += f"\n链接：{missing['url']}"
                if missing.get("authors"):
                    content += f"\n作者：{', '.join(missing['authors'][:5])}"
                result["online_block"] = {"title": display, "source": "kb_missing", "content": content}
                return result

            online_q = missing.get("online_query") or missing.get("display_name", subject)
            logger.info(f"[Compare] {subject} KB缺失，在线检索query: {online_q}")
            online_result = search_academic_papers_core(online_q, candidate=subject)
            logger.info(f"[Compare] {subject} 在线检索完成 ({len(online_result.text)} chars)")
            result["tool_logs"].append({
                "name": "search_academic_papers", "output": online_result.text,
                "elapsed": 0, "status": "success",
            })
            result["tool_previews"].append({
                "type": "tool", "content": online_result.text[:500], "name": "search_academic_papers",
                "query": online_q, "elapsed": 0,
                "meta": {"papers": online_result.papers_meta()},
            })
            result["online_block"] = {"title": display, "source": "在线检索", "content": online_result.text}
            return result

        # Round 1: subject + aspects 检索
        search_query = f"{subject} {aspects}"
        try:
            docs1 = rag.retriever_docs(search_query)
        except Exception:
            docs1 = []
        preview1 = docs1[0].page_content[:200] if docs1 else ""
        result["tool_logs"].append({
            "name": "academic_search", "output": preview1, "elapsed": 0, "status": "success",
        })
        result["tool_previews"].append({
            "type": "tool", "content": preview1, "name": "academic_search",
            "query": search_query, "elapsed": 0,
            "meta": {
                "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                             "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                             "preview": d.page_content[:80]} for d in docs1[:8]],
                "count": len(docs1),
            },
        })

        # 逐 subject judge
        judge = self._judge_subject_evidence(docs1, subject, aspects)
        logger.info(
            f"[SubjectJudge] {subject} paper_hit={judge['paper_hit']} "
            f"sufficient={judge['sufficient']} missing={judge['missing_dimensions']}"
        )

        if judge["sufficient"]:
            result["chunks"] = list(docs1)
            result["chunk_count"] = len(docs1)
            return result

        # 未命中目标论文 → 在线检索
        if not judge["paper_hit"]:
            logger.info(f"[Compare] {subject} 本地未命中 → 在线检索query: {subject}")
            online_result = search_academic_papers_core(subject, candidate=subject)
            result["tool_logs"].append({
                "name": "search_academic_papers", "output": online_result.text,
                "elapsed": 0, "status": "success",
            })
            result["tool_previews"].append({
                "type": "tool", "content": online_result.text[:500], "name": "search_academic_papers",
                "query": subject, "elapsed": 0,
                "meta": {"papers": online_result.papers_meta()},
            })
            result["online_block"] = {"title": subject, "source": "在线检索（本地未命中）", "content": online_result.text}
            return result

        # 命中但证据不足 → Round 2: 改写重试
        refine_q = judge.get("refine_query", f"{subject} {aspects}")
        try:
            docs2 = rag.retriever_docs(refine_q)
        except Exception:
            docs2 = []
        preview2 = docs2[0].page_content[:200] if docs2 else ""
        result["tool_logs"].append({
            "name": "academic_search", "output": preview2, "elapsed": 0, "status": "success",
        })
        result["tool_previews"].append({
            "type": "tool", "content": preview2, "name": "academic_search",
            "query": refine_q, "elapsed": 0,
            "meta": {
                "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                             "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                             "preview": d.page_content[:80]} for d in docs2[:8]],
                "count": len(docs2),
            },
        })

        # 合并两轮 chunk（去重）
        merged = list(docs1)
        seen_contents = {d.page_content[:120] for d in docs1}
        for d in docs2:
            if d.page_content[:120] not in seen_contents:
                merged.append(d)
                seen_contents.add(d.page_content[:120])
        result["chunks"] = merged
        result["chunk_count"] = len(merged)
        return result

    def _execute_compare_pipeline(self, query: str) -> Generator[dict, None, None]:
        from rag.rag_service import RagSummarizeService
        rag = RagSummarizeService()

        yield {"type": "system", "content": "正在提取论文名称...", "name": "system"}
        candidates = self._extract_candidates(query)
        if not candidates:
            yield from self._execute_qa_pipeline(query)
            return

        # 提取对比维度（所有 subject 共用）
        yield {"type": "system", "content": "正在分析对比维度...", "name": "system"}
        aspects = self._extract_compare_aspects(query)

        all_chunks: list = []
        online_blocks: list[dict] = []
        subject_chunk_count: dict[str, int] = {}  # 记录每个 subject 已有 chunk 数

        # 并行处理所有 subject
        with ThreadPoolExecutor(max_workers=min(3, len(candidates[:4]))) as executor:
            futures = {
                executor.submit(self._process_compare_subject, subject, aspects): subject
                for subject in candidates[:4]
            }
            for future in as_completed(futures):
                subj_result = future.result()
                subject = subj_result["subject"]
                # yield tool previews
                for preview in subj_result["tool_previews"]:
                    yield preview
                # merge tool logs
                self.callback.tool_invocation_log.extend(subj_result["tool_logs"])
                # merge online block
                if subj_result["online_block"]:
                    online_blocks.append(subj_result["online_block"])
                # merge chunks (dedup)
                seen = {d.page_content[:120] for d in all_chunks}
                for d in subj_result["chunks"]:
                    if d.page_content[:120] not in seen:
                        all_chunks.append(d)
                        seen.add(d.page_content[:120])
                subject_chunk_count[subject] = subj_result["chunk_count"]

        if not all_chunks and not online_blocks:
            yield {"type": "text", "content": "[系统] 未检索到任何相关文献。", "name": "system"}
            return

        # 均衡分配：按 token 预算动态计算 chunk 上限（~400 tokens/chunk）
        n_subjects = len(subject_chunk_count)
        max_total = 5000 // 400
        min_per = max(2, max_total // n_subjects // 2)
        max_per = max_total // n_subjects + 1
        capped = self._balance_chunks_by_subject(all_chunks, subject_chunk_count,
                                                  max_total=max_total, min_per=min_per, max_per=max_per)
        logger.info(f"[Compare] chunk 分配: {subject_chunk_count} → capped={len(capped)} (max_total={max_total})")

        # 统一 LLM judge
        judge_result = yield from self._llm_judge_chunks(capped, query)

        # compare_papers 辅助结构化对比（仅当有本地 chunk 时调用，纯在线论文已在 online_blocks 中）
        compare_text = ""
        if len(candidates) >= 2 and len(all_chunks) > 0:
            try:
                compare_text = compare_papers("; ".join(candidates[:4]), ctx=ctx)
                self.callback.tool_invocation_log.append({
                    "name": "compare_papers", "output": compare_text,
                    "elapsed": 0, "status": "success",
                })
                yield {
                    "type": "tool", "content": compare_text[:500], "name": "compare_papers",
                    "query": "; ".join(candidates[:4]), "elapsed": 0,
                    "meta": {"titles": candidates[:4]},
                }
            except Exception as e:
                logger.warning(f"[Compare] compare_papers 失败: {e}")

        yield from self._generate_answer_from_chunks(
            judge_result["relevant_chunks"], query, Intent.COMPARE,
            extra_context=compare_text, max_chunks=15, max_tokens=5000,
            memory_context=self._build_memory_context(query),
            online_blocks=online_blocks,
        )
        self._log_session_end("compare")

    def _balance_chunks_by_subject(
        self, chunks: list, counts: dict[str, int], max_total: int, min_per: int, max_per: int
    ) -> list:
        """按 subject 均衡分配 chunk：每 subject 保留 min_per~max_per 条，总数不超过 max_total"""
        if len(chunks) <= max_total:
            return chunks

        # 按 subject 关键词匹配分组
        subject_keys = list(counts.keys())
        groups: dict[str, list] = {k: [] for k in subject_keys}
        unassigned: list = []

        for doc in chunks:
            title = (doc.metadata.get("paper_title", "") or "").lower()
            content = doc.page_content.lower()
            matched = None
            for subj in subject_keys:
                subj_lower = subj.lower()
                if subj_lower in title:
                    matched = subj
                    break
                # fallback: chunk 内容包含 subject 关键词（如 BTD 出现在正文中）
                if subj_lower in content:
                    matched = subj
                    break
            if matched:
                groups[matched].append(doc)
            else:
                unassigned.append(doc)

        result = []
        remaining = max_total

        # 第一轮：每个 subject 分配 min_per 条
        for subj in subject_keys:
            take = min(min_per, len(groups[subj]), remaining)
            result.extend(groups[subj][:take])
            remaining -= take

        # 第二轮：有余额则补充到 max_per
        for subj in subject_keys:
            if remaining <= 0:
                break
            already = min(min_per, len(groups[subj]))
            extra = min(max_per - already, len(groups[subj]) - already, remaining)
            if extra > 0:
                result.extend(groups[subj][already:already + extra])
                remaining -= extra

        # 仍有余额 → 补充未分配 chunk
        if remaining > 0 and unassigned:
            result.extend(unassigned[:remaining])

        return result

    @staticmethod
    def _tokenize_memory(text: str) -> set[str]:
        """jieba 分词，过滤短词"""
        tokens = jieba.cut(text)
        return {t.strip().lower() for t in tokens if len(t.strip()) > 1}

    def _filter_relevant(self, query: str, items: list[str], threshold: float = 0.15) -> list[str]:
        """Jaccard 相似度过滤：只保留与 query 相关的项"""
        q_tokens = self._tokenize_memory(query)
        if not q_tokens:
            return items
        relevant = []
        for item in items:
            item_tokens = self._tokenize_memory(item[:300])
            if not item_tokens:
                continue
            jaccard = len(q_tokens & item_tokens) / len(q_tokens | item_tokens)
            if jaccard >= threshold:
                relevant.append(item)
        return relevant

    def _build_memory_context(self, query: str) -> str:
        """从短期记忆和长期事实中提取与 query 相关的内容，拼接为上下文"""
        parts = []

        # 相关历史对话
        history_msgs = self.memory.get_recent_turns()
        if history_msgs:
            history_texts = [m["content"][:300] for m in history_msgs]
            relevant = self._filter_relevant(query, history_texts)
            if relevant:
                parts.append("[相关历史对话]\n" + "\n".join(relevant[-6:]))

        # 相关长期事实
        facts_text = self.fact_store.get_facts_text()
        if facts_text:
            facts_items = [l for l in facts_text.split("\n") if l.startswith("- ")]
            if facts_items:
                relevant = self._filter_relevant(query, facts_items)
                if relevant:
                    parts.append("[相关已知事实]\n" + "\n".join(relevant[-10:]))

        return "\n".join(parts) if parts else ""

    # ── REVIEW Pipeline (raw chunks → judge → 在线补充) ──

    def _execute_review_pipeline(self, query: str) -> Generator[dict, None, None]:
        from rag.rag_service import RagSummarizeService
        rag = RagSummarizeService()

        # 1. 本地检索 → 原始 chunks
        try:
            docs = rag.retriever_docs(query)
        except Exception:
            docs = []
        preview = docs[0].page_content[:200] if docs else ""
        self.callback.tool_invocation_log.append({
            "name": "academic_search", "output": preview, "elapsed": 0, "status": "success",
        })
        yield {
            "type": "tool", "content": preview, "name": "academic_search",
            "query": query, "elapsed": 0,
            "meta": {
                "sources": [{"title": d.metadata.get("paper_title", ""), "section": d.metadata.get("section", ""),
                             "page": d.metadata.get("page_start") or d.metadata.get("page", ""),
                             "preview": d.page_content[:80]} for d in docs[:8]],
                "count": len(docs),
            },
        }

        # 2. LLM judge chunks
        judge_result = yield from self._llm_judge_chunks(docs, query)

        # 3. 不足则在线补充 → 作为 online_blocks（享受 evidence budget 最低保障）
        online_blocks = []
        if not judge_result["sufficient"]:
            yield {"type": "system", "content": "正在在线检索补充文献...", "name": "system"}
            subject = self._extract_candidates(query)
            first = subject[0] if subject else ""
            online_q = self._build_online_query(query, first)
            logger.info(f"[Review] 在线检索query: {online_q}")
            online_result = search_academic_papers_core(online_q, candidate=first)

            # === CitationTrace: after online retrieval ===
            online_text = online_result.text or ""
            scored_count = len(online_result.scored_results) if hasattr(online_result, 'scored_results') else 0
            logger.info(
                "[CitationTrace][online_result] text_len=%d newline_count=%d",
                len(online_text), online_text.count("\n"),
            )
            logger.info(
                "[CitationTrace][online_result] scored_results_count=%d",
                scored_count,
            )
            for idx, (paper, score) in enumerate(online_result.scored_results[:10]):
                logger.info(
                    "[CitationTrace][online_result][paper:%d] title=%r score=%.3f abstract_len=%d doi=%r url=%r",
                    idx, paper.title, score, len(paper.abstract or ""), paper.doi, paper.url,
                )
            # === end CitationTrace ===

            self.callback.tool_invocation_log.append({
                "name": "search_academic_papers", "output": online_result.text, "elapsed": 0, "status": "success",
            })
            yield {
                "type": "tool", "content": online_result.text[:500], "name": "search_academic_papers",
                "query": online_q, "elapsed": 0,
                "meta": {"papers": online_result.papers_meta()},
            }

            # 使用 scored_results 逐篇构造独立 EvidenceBlock
            online_blocks = self._build_review_online_blocks(
                online_result.scored_results,
                max_papers=30,
            )

            # === CitationTrace: after online_blocks constructed ===
            logger.info("[CitationTrace][online_blocks] len=%d", len(online_blocks))
            for idx, block in enumerate(online_blocks):
                blk_content = block.get("content", "")
                logger.info(
                    "[CitationTrace][online_block:%d] title=%r source=%r content_len=%d newline_count=%d",
                    idx, block.get("title"), block.get("source"),
                    len(blk_content), blk_content.count("\n"),
                )
            # === end CitationTrace ===

        yield from self._generate_answer_from_chunks(
            judge_result["relevant_chunks"], query, Intent.REVIEW, max_chunks=30, max_tokens=8000,
            memory_context=self._build_memory_context(query),
            online_blocks=online_blocks,
        )
        self._log_session_end("review")

    def execute_stream(self, query: str) -> Generator[dict, None, None]:
        # === RESET per-execution state ===
        from agent.execution_context import ExecutionContext
        self._retrieval_state = AgentRetrievalState()
        self._execution_policy = AgentExecutionPolicy()
        ctx = ExecutionContext(
            policy=self._execution_policy,
            retrieval_state=self._retrieval_state,
        )
        self._current_intent = Intent.QA
        self.callback.tool_invocation_log.clear()


        # === CLASSIFY intent ===
        self._current_intent = self.intent_router.classify(query)
        yield {"type": "intent", "content": self._current_intent.value, "name": "system"}

        # === ROUTE by intent ===
        if self._current_intent == Intent.QA:
            yield from self._execute_qa_pipeline(query)
            return
        elif self._current_intent == Intent.COMPARE:
            yield from self._execute_compare_pipeline(query)
            return
        elif self._current_intent == Intent.REVIEW:
            yield from self._execute_review_pipeline(query)
            return

    def _verify_citations(self, answer: str, tool_results: list) -> str:
        """校验回答中的 [N] 引用编号"""
        acad_results = [r for r in tool_results if r["name"] == "academic_search" and r["is_valid"]]
        if not acad_results:
            return ""

        max_valid = 0
        for r in acad_results:
            content = r.get("content", "")
            cited = set(int(m) for m in re.findall(r"\[(\d+)\]", content) if m.isdigit())
            if cited:
                max_valid = max(max_valid, max(cited))

        if max_valid == 0:
            return ""

        cited_in_answer = set(int(m) for m in re.findall(r"\[(\d+)\]", answer) if m.isdigit())
        invalid = sorted(n for n in cited_in_answer if n > max_valid)
        if invalid:
            return f"\n\n> 引用校验警告：发现无效引用编号 {invalid}，有效范围为 [1-{max_valid}]。"
        return ""


if __name__ == "__main__":
    agent = ReactAgent()
    print("=== ReAct Agent 测试 ===\n")
    for chunk in agent.execute_stream("Transformer模型的核心机制是什么？"):
        if chunk["type"] == "text":
            print(chunk["content"], end="", flush=True)
        elif chunk["type"] == "tool":
            print(f"\n[工具: {chunk['name']}] {chunk['content'][:100]}...")
        elif chunk["type"] == "intent":
            print(f"[意图: {chunk['content']}]")
    print("\n\n=== Done ===")

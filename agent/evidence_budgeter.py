"""证据上下文分层 token 预算分配器。

将本地 chunks 和在线 blocks 转换为统一的 EvidenceBlock，
按分层策略分配 token 预算，返回 AllocationResult。
"""
import os
from dataclasses import dataclass, field
from typing import Callable


# ── Token 计数 ──

_MODEL_ENCODING: dict[str, str] = {
    "deepseek": "cl100k_base",
    "gpt-4":    "cl100k_base",
    "gpt-3.5":  "cl100k_base",
    "qwen":     "cl100k_base",
}
_FALLBACK_ENCODING = "cl100k_base"


def _get_encoding_name(model: str | None = None) -> str:
    model = model or os.getenv("LLM_MODEL", "")
    model_lower = model.lower()
    for key, enc in _MODEL_ENCODING.items():
        if key in model_lower:
            return enc
    return _FALLBACK_ENCODING


class TokenCounter:
    """延迟加载的 tiktoken 计数器，实例级 approximate 标记"""

    def __init__(self, model_name: str | None = None):
        import tiktoken
        self.model_name = model_name or os.getenv("LLM_MODEL", "")
        self.encoding = _get_encoding_name(self.model_name)
        self.backend = "tiktoken"
        self.approximate = True
        self._encoder = tiktoken.get_encoding(self.encoding)

    def count(self, text: str) -> int:
        return len(self._encoder.encode(text))


# ── 证据块 ──

@dataclass(frozen=True)
class EvidenceBlock:
    evidence_id: str            # 唯一标识 "local:0" | "online:0"
    source_type: str            # "local" | "online"
    subject_id: str             # 所属 subject（默认 ""）
    source_order: int           # 原始输入顺序
    quality_score: float        # 归一化质量分 0~1
    citation_meta: dict         # 标题/章节/页码等引用元数据
    raw_content: str            # 原始正文（未带引用编号）
    token_cost: int             # 预计算的渲染 token 成本

    def render(self, ref_number: int) -> str:
        """按最终引用编号渲染完整引用块"""
        from utils.logger_handler import logger
        meta = self.citation_meta
        title = meta.get("title", "未知")
        logger.info(
            "[CitationTrace][render:%d] id=%s title=%r raw_content_len=%d raw_newlines=%d",
            ref_number, self.evidence_id, title,
            len(self.raw_content or ""), (self.raw_content or "").count("\n"),
        )
        if self.source_type == "online":
            source = meta.get("source", "在线")
            authors = meta.get("authors", [])
            year = meta.get("year", "")
            doi = meta.get("doi", "")
            url = meta.get("url", "")
            evidence_type = meta.get("evidence_type", "abstract")
            author_str = ", ".join(authors[:3]) if authors else ""
            if len(authors) > 3:
                author_str += " 等"
            header = (
                f"[{ref_number}] [在线]《{title}》\n"
                f"    作者：{author_str or '未知'}\n"
                f"    年份：{year or '未知'}\n"
                f"    来源：{source}\n"
                f"    类型：{evidence_type}"
            )
            if doi:
                header += f"\n    DOI：{doi}"
            if url:
                header += f"\n    URL：{url}"
            header += f"\n\n{self.raw_content}"
            return header
        else:
            section = meta.get("section", "未知")
            ps = meta.get("page_start") or meta.get("page", "")
            pe = meta.get("page_end") or meta.get("page", "")
            page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}" if ps and pe else "未知"
            return (f"[{ref_number}] 来源：《{title}》；"
                    f"章节：{section}；页码：{page}；内容：{self.raw_content}")


# ── 预算配置 ──

@dataclass
class BudgetConfig:
    context_window: int = 8192
    output_reserve: int = 1024
    safety_margin_tokens: int = 200
    memory_ratio: float = 0.08
    extra_ratio: float = 0.08
    target_min_local: int = 2
    target_min_online: int = 1
    min_quality_score: float = 0.3
    target_min_per_subject: int = 1

    @property
    def input_budget(self) -> int:
        return self.context_window - self.output_reserve - self.safety_margin_tokens


# ── 分配结果 ──

@dataclass(frozen=True)
class AllocationResult:
    context: str
    selected_blocks: tuple       # tuple[EvidenceBlock, ...]  按最终引用顺序
    references: tuple            # tuple[str, ...]  渲染后的引用文本列表
    reference_map: tuple         # tuple[(int, str, dict), ...] (引用编号, evidence_id, citation_meta)
    token_usage: dict            # {"fixed": N, "memory": N, "extra": N, "evidence": N, "total": N}
    dropped_blocks: tuple        # tuple[EvidenceBlock, ...]
    drop_reasons: tuple          # tuple[str, ...]
    within_budget: bool
    approximate_token_count: bool


# ── 预算器 ──

class EvidenceBudgeter:
    """证据上下文分层 token 预算分配器"""

    def __init__(self, config: BudgetConfig | None = None,
                 counter: TokenCounter | None = None):
        self.config = config or BudgetConfig()
        self.counter = counter or TokenCounter()
        self._debug: list[str] = []

    # ── 公共入口 ──

    def allocate(
        self,
        system_prompt: str,
        query: str,
        local_blocks: list[EvidenceBlock],
        online_blocks: list[EvidenceBlock] | None = None,
        *,
        memory_context: str = "",
        extra_context: str = "",
        online_available: bool = False,
    ) -> AllocationResult:
        online_blocks = online_blocks or []
        budget = self.config.input_budget
        self._debug = [f"input_budget={budget}"]

        # 1. 固定开销
        template = "用户问题：{query}\n\n检索结果：\n{context}"
        fixed = (self.counter.count(system_prompt)
                 + self.counter.count(query)
                 + self.counter.count(template.format(query="", context="")))
        budget -= fixed
        self._debug.append(f"fixed={fixed}, remaining={budget}")

        # 2. memory_context
        mem_budget = int(min(self.config.input_budget * self.config.memory_ratio, budget))
        mem_text = self._truncate_text(memory_context, mem_budget) if memory_context else ""
        if mem_text:
            mem_block = f"[对话上下文]\n{mem_text}\n\n"
            mem_tokens = self.counter.count(mem_block)
            budget -= mem_tokens
            self._debug.append(f"memory={mem_tokens}, remaining={budget}")
        else:
            mem_block = ""

        # 3. extra_context
        extra_budget = int(min(self.config.input_budget * self.config.extra_ratio, budget))
        extra_text = self._truncate_text(extra_context, extra_budget) if extra_context else ""
        if extra_text:
            extra_block = f"\n\n---\n{extra_text}"
            extra_tokens = self.counter.count(extra_block)
            budget -= extra_tokens
            self._debug.append(f"extra={extra_tokens}, remaining={budget}")
        else:
            extra_block = ""

        # 4. 证据选择
        selected, dropped, drop_reasons = self._select_blocks(
            local_blocks, online_blocks, budget, online_available)
        evidence_tokens = sum(b.token_cost for b in selected)
        budget -= evidence_tokens
        self._debug.append(f"evidence={evidence_tokens}, remaining={budget}")

        # 5. 渲染
        context = mem_block
        ref_num = 1
        ref_map = []
        ref_texts = []
        for block in selected:
            rendered = block.render(ref_num)
            context += rendered + "\n\n"
            ref_map.append((ref_num, block.evidence_id, block.citation_meta))
            ref_texts.append(rendered)
            ref_num += 1
        if extra_block:
            context += extra_block

        # 6. 完整 Prompt 校验
        full_text = system_prompt + "\n" + template.format(query=query, context=context)
        total = self.counter.count(full_text)
        self._debug.append(f"full_prompt={total}")

        # 超预算时安全降级
        within = total <= self.config.input_budget
        if not within and selected:
            # 移除最后一个块后重试
            removed = selected[-1]
            selected = selected[:-1]
            dropped = [removed] + dropped
            drop_reasons = ["budget_exceeded_after_render"] + drop_reasons
            # 重新渲染
            context = mem_block
            ref_num = 1
            ref_map = []
            ref_texts = []
            for block in selected:
                rendered = block.render(ref_num)
                context += rendered + "\n\n"
                ref_map.append((ref_num, block.evidence_id, block.citation_meta))
                ref_texts.append(rendered)
                ref_num += 1
            if extra_block:
                context += extra_block
            full_text = system_prompt + "\n" + template.format(query=query, context=context)
            total = self.counter.count(full_text)
            within = total <= self.config.input_budget

        return AllocationResult(
            context=context,
            selected_blocks=tuple(selected),
            references=tuple(ref_texts),
            reference_map=tuple(ref_map),
            token_usage={
                "fixed": fixed,
                "memory": mem_tokens if mem_text else 0,
                "extra": extra_tokens if extra_text else 0,
                "evidence": sum(b.token_cost for b in selected),
                "total": total,
            },
            dropped_blocks=tuple(dropped),
            drop_reasons=tuple(drop_reasons),
            within_budget=within,
            approximate_token_count=self.counter.approximate,
        )

    # ── 块选择算法 ──

    def _select_blocks(
        self,
        local: list[EvidenceBlock],
        online: list[EvidenceBlock],
        budget: int,
        online_available: bool,
    ) -> tuple[list, list, list]:
        # 过滤低质量
        local = [b for b in local if b.quality_score >= self.config.min_quality_score]
        online = [b for b in online if b.quality_score >= self.config.min_quality_score]

        # 分层：local 优先
        selected = []
        remaining = budget

        # 本地目标
        local_sorted = sorted(local, key=lambda b: b.quality_score, reverse=True)
        for b in local_sorted:
            if len([x for x in selected if x.subject_id == b.subject_id]) < self.config.target_min_per_subject:
                if b.token_cost <= remaining:
                    selected.append(b)
                    remaining -= b.token_cost
        # 剩余本地
        for b in local_sorted:
            if b.evidence_id not in {s.evidence_id for s in selected} and b.token_cost <= remaining:
                selected.append(b)
                remaining -= b.token_cost

        # 在线证据（仅在 online_available 且存在时启用）
        if online_available and online:
            online_sorted = sorted(online, key=lambda b: b.quality_score, reverse=True)
            online_added = 0
            for b in online_sorted:
                if online_added < self.config.target_min_online and b.token_cost <= remaining:
                    selected.append(b)
                    remaining -= b.token_cost
                    online_added += 1
            for b in online_sorted:
                if b.evidence_id not in {s.evidence_id for s in selected} and b.token_cost <= remaining:
                    selected.append(b)
                    remaining -= b.token_cost

        # 被丢弃的
        selected_ids = {b.evidence_id for b in selected}
        dropped = [b for b in local + online if b.evidence_id not in selected_ids]
        reasons = ["quality_below_threshold" if b.quality_score < self.config.min_quality_score
                   else "budget_exhausted" for b in dropped]

        return selected, dropped, reasons

    # ── 辅助 ──

    def _truncate_text(self, text: str, max_tokens: int) -> str:
        if not text:
            return ""
        if self.counter.count(text) <= max_tokens:
            return text
        lo, hi = 0, len(text)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.counter.count(text[:mid]) <= max_tokens:
                lo = mid
            else:
                hi = mid - 1
        cut = lo
        for sep in ["\n\n", "\n", "。", ". "]:
            pos = text.rfind(sep, 0, cut)
            if pos > cut * 0.6:
                cut = pos + len(sep)
                break
        truncated = text[:cut] + "..."
        # 确保含省略号的 token 不超
        if self.counter.count(truncated) > max_tokens:
            truncated = text[:cut] + "…"
        return truncated


# ── 构建辅助 ──

def build_local_blocks(chunks: list, counter: TokenCounter) -> list[EvidenceBlock]:
    """从 Chroma Document 列表构建 EvidenceBlock"""
    blocks = []
    for i, doc in enumerate(chunks):
        meta = doc.metadata
        title = meta.get("paper_title", "未知")
        section = meta.get("section", "未知")
        ps = meta.get("page_start") or meta.get("page", "")
        pe = meta.get("page_end") or meta.get("page", "")
        page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}" if ps and pe else "未知"
        # 归一化质量分：有 reranker 分数时用，否则默认 0.5
        score = meta.get("reranker_score", 0.5)
        if isinstance(score, (int, float)):
            qs = max(0.0, min(1.0, float(score)))
        else:
            qs = 0.5

        raw = doc.page_content
        token_cost = counter.count(
            f"[N] 来源：《{title}》；章节：{section}；页码：{page}；内容：{raw}"
        )

        blocks.append(EvidenceBlock(
            evidence_id=f"local:{i}",
            source_type="local",
            subject_id="",
            source_order=i,
            quality_score=qs,
            citation_meta={
                "title": title, "section": section,
                "page_start": ps, "page_end": pe,
            },
            raw_content=raw,
            token_cost=token_cost,
        ))
    return blocks


def build_online_blocks(results: list[dict], counter: TokenCounter) -> list[EvidenceBlock]:
    """从在线检索结果列表构建 EvidenceBlock"""
    from utils.logger_handler import logger
    logger.info("[CitationTrace][build_online_blocks] input_count=%d", len(results))
    for idx, item in enumerate(results):
        item_content = item.get("content", "")
        logger.info(
            "[CitationTrace][build_online_block_input:%d] title=%r source=%r content_len=%d newline_count=%d repr=%r",
            idx, item.get("title"), item.get("source"),
            len(item_content), item_content.count("\n"), item_content[:200],
        )
    blocks = []
    for i, item in enumerate(results):
        title = item.get("title", "未知")
        source = item.get("source", "在线")
        raw = item.get("content", "")
        token_cost = counter.count(
            f"[N] [在线]《{title}》| 来源：{source}\n{raw}"
        )
        # Support both "score" and "quality_score" keys
        score = item.get("quality_score") or item.get("score", 0.5)
        qs = max(0.0, min(1.0, float(score))) if isinstance(score, (int, float)) else 0.5

        blocks.append(EvidenceBlock(
            evidence_id=f"online:{i}",
            source_type="online",
            subject_id="",
            source_order=i,
            quality_score=qs,
            citation_meta={
                "title": title,
                "source": source,
                "authors": item.get("authors", []),
                "year": item.get("year", ""),
                "doi": item.get("doi", ""),
                "url": item.get("url", ""),
                "evidence_type": item.get("evidence_type", "abstract"),
            },
            raw_content=raw,
            token_cost=token_cost,
        ))
    return blocks

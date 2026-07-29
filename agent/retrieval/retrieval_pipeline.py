"""在线检索管线：SearchIntent → Stage 1 → 身份验证 → 早停（Stage 2/3 预留）"""
from dataclasses import replace
from agent.retrieval.query_rewrite import RuleBasedRewriter
from agent.retrieval.academic_client import AcademicDataClient, SearchIntent
from agent.retrieval.composite_ranker import CompositeRanker
from agent.retrieval.paper_validator import PaperIdentityValidator, ConfidenceLevel
from utils.logger_handler import logger


class OnlineRetrievalPipeline:
    def __init__(self):
        self.rewriter = RuleBasedRewriter()
        self.client = AcademicDataClient()
        self.ranker = CompositeRanker()
        self.validator = PaperIdentityValidator()
        # 请求级状态已迁移到 _execute_intent_structured 的局部变量和 OnlineRetrievalResult

    # ── 带 SearchIntent 的检索（Commit 2: Stage 1 only）──

    def run_with_intent(self, intent: SearchIntent, max_results: int = 20) -> str:
        """三阶段检索（委托 _execute_intent_structured，保持字符串兼容）"""
        result = self._execute_intent_structured(intent, max_results)
        return result.text

    def _execute_intent_structured(
        self, intent: SearchIntent, max_results: int = 20
    ) -> "OnlineRetrievalResult":
        """不写入实例级请求状态的结构化检索方法。
        
        同一 OnlineRetrievalPipeline 实例可被多个并发调用安全执行，
        所有请求级状态仅存在于局部变量和返回值中。
        """
        early_stopped = False
        stop_stage: int | None = None
        all_papers: list = []
        stage_results_list: list = []
        last_scored: list = []
        executed_stages: list[int] = []
        papers_per_stage: list[int] = []

        # ── Stage 1: candidate-only ──
        if intent.candidate:
            logger.info(f"[OnlinePipeline] Stage1 candidate={intent.candidate} type={intent.candidate_type}")
            s1_results = self.client.search_stage(intent, stage=1, max_per_source=5)
            logger.info(
                "[CitationTrace][stage1_sources] total=%d %s",
                len(s1_results),
                {r.source: (r.status, len(r.papers)) for r in s1_results},
            )
            stage_results_list.extend(s1_results)
            executed_stages.append(1)
            all_papers = self._collect_and_dedup(s1_results)
            logger.info("[CitationTrace][stage1_deduped] papers=%d", len(all_papers))
            papers_per_stage.append(len(all_papers))
            if all_papers:
                last_scored, early_stopped = self._score_and_check(
                    intent, all_papers, 1)
                if early_stopped:
                    stop_stage = 1

        # ── Stage 2: candidate + disambiguation keyword ──
        if not early_stopped and intent.candidate:
            keyword = self._extract_disambiguation_keyword(intent)
            if keyword:
                stage2_intent = replace(intent, keyword=keyword)
                logger.info(f"[OnlinePipeline] Stage2 candidate={intent.candidate} keyword={keyword}")
                s2_results = self.client.search_stage(stage2_intent, stage=2, max_per_source=5)
                logger.info(
                    "[CitationTrace][stage2_sources] total=%d %s",
                    len(s2_results),
                    {r.source: (r.status, len(r.papers)) for r in s2_results},
                )
                stage_results_list.extend(s2_results)
                executed_stages.append(2)
                new_papers = self._collect_and_dedup(s2_results)
                logger.info("[CitationTrace][stage2_deduped] papers=%d", len(new_papers))
                papers_per_stage.append(len(new_papers))
                if new_papers:
                    all_papers = self._merge_papers(all_papers, new_papers)
                    last_scored, early_stopped = self._score_and_check(
                        intent, all_papers, 2)
                    if early_stopped:
                        stop_stage = 2

        # ── Stage 3: RuleBasedRewriter fallback variants ──
        if not early_stopped:
            fallback_q = intent.fallback_query or intent.candidate
            variants = self.rewriter.rewrite(fallback_q)
            logger.info(f"[OnlinePipeline] Stage3 variants={variants[:3]}")
            executed_stages.append(3)
            stage3_paper_count = 0
            for variant in variants[:3]:
                if early_stopped:
                    break
                s3_results = self.client.search_stage(
                    intent, stage=3, max_per_source=5, fallback_variant=variant)
                logger.info(
                    "[CitationTrace][stage3_variant:%s] sources=%d %s",
                    variant[:50],
                    len(s3_results),
                    {r.source: (r.status, len(r.papers)) for r in s3_results},
                )
                stage_results_list.extend(s3_results)
                new_papers = self._collect_and_dedup(s3_results)
                logger.info("[CitationTrace][stage3_variant_deduped] papers=%d", len(new_papers))
                stage3_paper_count += len(new_papers)
                if new_papers:
                    all_papers = self._merge_papers(all_papers, new_papers)
                    with_abs = sum(1 for p in all_papers if p.abstract)
                    total = len(all_papers)
                    logger.info(
                        "[AbstractTrace][after_variant_merge] total=%d with_abstract=%d",
                        total, with_abs,
                    )
                    for p in all_papers[:5]:
                        logger.info(
                            "[AbstractTrace][merged_paper] title=%r abstract_len=%d source=%r",
                            p.title[:100], len(p.abstract or ""), p.source,
                        )
                    last_scored, early_stopped = self._score_and_check(
                        intent, all_papers, 3)
                    if early_stopped:
                        stop_stage = 3
            papers_per_stage.append(stage3_paper_count)

        with_abs_scored = sum(1 for p, s in last_scored if p.abstract)
        logger.info(
            "[CitationTrace][before_format] last_scored_len=%d valid_after_threshold=%d with_abstract=%d",
            len(last_scored),
            sum(1 for p, s in last_scored
                if self.validator.validate(intent.candidate, p, s, intent.candidate_type)[0]
                in (ConfidenceLevel.EXACT, ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM)),
            with_abs_scored,
        )
        for p, s in last_scored[:5]:
            logger.info(
                "[AbstractTrace][last_scored] title=%r score=%.3f abstract_len=%d source=%r id=%s",
                p.title[:100], s, len(p.abstract or ""), p.source, id(p),
            )
        text = self._format_scored(last_scored, intent) if last_scored else "未找到相关论文。"
        formatted_line_count = len(text.split("\n")) if text else 0
        paper_count_in_text = text.count("[") if text else 0
        logger.info(
            "[CitationTrace][after_format] text_len=%d text_lines=%d approx_papers_in_text=%d repr=%r",
            len(text), formatted_line_count, paper_count_in_text, text[:200],
        )
        return OnlineRetrievalResult(
            text=text,
            scored_results=tuple(last_scored),
            stage_results=tuple(stage_results_list),
            early_stopped=early_stopped,
            stop_stage=stop_stage,
            executed_stages=tuple(executed_stages),
            papers_per_stage=tuple(papers_per_stage),
            intent_candidate=intent.candidate,
            intent_candidate_type=intent.candidate_type,
        )

    def _score_and_check(self, intent, all_papers, stage) -> tuple[list, bool]:
        """评分 + 早停判断。返回 (scored, early_stopped)，不写入 self。"""
        identity_scores = self.ranker.rank_identity(intent.candidate, all_papers)
        semantic_scores = self.ranker._max_score(
            intent.fallback_query or intent.candidate, all_papers, self.ranker.rankers)

        combined = []
        for p, i_score, s_score in zip(all_papers, identity_scores, semantic_scores):
            level, reason = self.validator.validate(
                intent.candidate, p, i_score, intent.candidate_type)
            combined.append((p, i_score, s_score, level, reason))
            logger.info(
                f"[OnlinePipeline] Stage{stage} validate: {p.title[:80]} "
                f"id_score={i_score:.3f} sem_score={s_score:.3f} level={level.value}"
            )

        scored = [(p, 0.6 * i + 0.3 * s + 0.1) for p, i, s, _, _ in combined]
        scored.sort(key=lambda x: x[1], reverse=True)

        early = False
        for p, i_score, s_score, level, reason in combined:
            if level in (ConfidenceLevel.EXACT, ConfidenceLevel.HIGH):
                early = True
                logger.info(
                    f"[OnlinePipeline] Stage{stage} 早停: {p.title[:80]} "
                    f"level={level.value} reason={reason}"
                )
                break

        return scored, early

    def _format_scored(self, scored: list, intent: SearchIntent, max_output: int = 5) -> str:
        """从 scored 列表生成格式化文本（不依赖 self._last_intent）"""
        if not scored:
            return "未找到相关论文。"

        valid = []
        for paper, score in scored:
            level, _ = self.validator.validate(
                intent.candidate, paper, score, intent.candidate_type)
            if level in (ConfidenceLevel.EXACT, ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM):
                valid.append((paper, score, level))

        logger.info(
            "[CitationTrace][_format_scored] scored_input=%d valid_after_threshold=%d max_output=%d",
            len(scored), len(valid), max_output,
        )
        if not valid:
            top_score = f"{scored[0][1]:.2f}" if scored else "N/A"
            return f"未找到高置信度匹配论文（共检索到 {len(scored)} 条结果，最高分 {top_score}，均低于 0.70 阈值）。"

        lines = []
        for i, (paper, score, level) in enumerate(valid[:max_output]):
            authors = ", ".join(paper.authors[:2]) if paper.authors else ""
            year = f"({paper.year})" if paper.year else ""
            title = paper.title
            lines.append(f"[{i + 1}] {title} | {authors} {year} | {paper.source}")
            if paper.abstract:
                lines.append(f"    摘要: {paper.abstract}")

        return "\n".join(lines)

    def _collect_and_dedup(self, stage_results: list) -> list:
        """从 SourceSearchResult 中提取 papers，跨源去重 + 元数据合并"""
        papers = []
        for r in stage_results:
            if r.status == "ok":
                papers.extend(r.papers)
        if not papers:
            return []
        from agent.retrieval.academic_client import AcademicDataClient
        return AcademicDataClient._merge_duplicates(papers)

    @staticmethod
    def _merge_papers(existing: list, new_papers: list) -> list:
        """合并论文列表，按标题去重"""
        seen = {p.title.lower().strip() for p in existing}
        merged = list(existing)
        for p in new_papers:
            key = p.title.lower().strip()
            if key not in seen:
                seen.add(key)
                merged.append(p)
        return merged

    @staticmethod
    def _extract_disambiguation_keyword(intent: SearchIntent) -> str:
        """从 fallback_query 中提取消歧关键词：移除 candidate 后取最长的英文词"""
        import re
        candidate = intent.candidate.lower().strip()
        fallback = (intent.fallback_query or "").lower().strip()
        if not fallback or fallback == candidate:
            return ""
        remaining = re.sub(re.escape(candidate), "", fallback, count=1).strip()
        # 提取所有纯英文词（>=3 字符），跳过常见停用词
        stop_words = {"the", "and", "for", "with", "based", "using", "via", "from",
                      "new", "3d", "2d", "all", "its", "can", "has", "one", "two"}
        english_words = re.findall(r'[a-z][a-z0-9]{2,}', remaining)
        candidates = [w for w in english_words if w not in stop_words]
        if not candidates:
            return ""
        # 优先最长词
        candidates.sort(key=len, reverse=True)
        return candidates[0]


    # ── 兼容旧接口 ──

    def run(self, query: str) -> str:
        """向后兼容：无 candidate 时走旧逻辑"""
        logger.info(f"[OnlinePipeline]原始query (legacy): {query}")

        variants = self.rewriter.rewrite(query)
        logger.info(f"[OnlinePipeline]query变体: {variants}")

        all_papers = self.client.search(query, max_results=20)

        if not all_papers:
            return "未找到相关论文。"

        scored = self.ranker.rank(query, all_papers)
        # scored 仅作为局部变量

        for i, (paper, score) in enumerate(scored[:3]):
            logger.info(f"[OnlinePipeline] top{i+1}: score={score:.3f} title={paper.title[:80]}")

        return self._format_legacy(scored)

    def _format_legacy(self, scored: list, max_output: int = 5) -> str:
        valid: list[tuple] = []
        for paper, score in scored:
            level, _ = self.validator.validate("", paper, score)
            if level in (ConfidenceLevel.EXACT, ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM):
                valid.append((paper, score, level))

        if not valid:
            top_score = f"{scored[0][1]:.2f}" if scored else "N/A"
            return f"未找到高置信度匹配论文（共检索到 {len(scored)} 条结果，最高分 {top_score}，均低于 0.70 阈值）。"

        lines = []
        for i, (paper, score, level) in enumerate(valid[:max_output]):
            authors = ", ".join(paper.authors[:2]) if paper.authors else ""
            year = f"({paper.year})" if paper.year else ""
            title = paper.title
            lines.append(f"[{i + 1}] {title} | {authors} {year} | {paper.source}")
            if paper.abstract:
                lines.append(f"    摘要: {paper.abstract}")

        return "\n".join(lines)

    def fetch_metadata_by_title(self, title: str) -> dict | None:
        """根据精确标题获取论文元数据（用于 fetch_paper_metadata 工具）"""
        papers = self.client.search(title, max_results=5)
        if not papers:
            return None

        title_lower = title.strip().lower()
        best = None
        for p in papers:
            if p.title.strip().lower() == title_lower:
                best = p
                break
        if not best:
            best = papers[0]

        return {
            "title": best.title,
            "authors": best.authors,
            "year": best.year,
            "source": best.source,
            "doi": best.doi,
            "venue": best.venue,
            "url": best.url,
            "abstract": best.abstract,
            "citation_count": best.citation_count,
        }

    def fetch_citation_info_by_title(self, title: str) -> dict | None:
        """根据精确标题获取引用计数（用于 fetch_citation_info 工具）"""
        papers = self.client.search(title, max_results=5)
        if not papers:
            return None

        title_lower = title.strip().lower()
        best = None
        for p in papers:
            if p.title.strip().lower() == title_lower:
                best = p
                break
        if not best:
            best = papers[0]

        return {
            "title": best.title,
            "citation_count": best.citation_count or 0,
            "source": best.source,
        }




# ── 结构化返回（不可变）──

from dataclasses import dataclass

@dataclass(frozen=True)
class OnlineRetrievalResult:
    """run_with_intent 的不可变结构化返回"""
    text: str                              # 格式化文本（兼容旧字符串接口）
    scored_results: tuple = ()             # ((AcademicPaper, float), ...)
    stage_results: tuple = ()              # (SourceSearchResult, ...)
    early_stopped: bool = False
    stop_stage: int | None = None          # None 表示未早停
    executed_stages: tuple = ()            # 实际执行过的阶段号
    papers_per_stage: tuple = ()           # 各阶段有效论文数
    intent_candidate: str = ""
    intent_candidate_type: str = "unknown"

    def papers_meta(self) -> list[dict]:
        """前端展示用的论文元数据摘要（从 scored_results 派生）"""
        papers = []
        for paper, score in self.scored_results[:5]:
            papers.append({
                "title": paper.title,
                "authors": paper.authors[:3] if paper.authors else [],
                "year": paper.year or "",
                "source": paper.source,
                "score": round(score, 3),
                "abstract": (paper.abstract or "")[:150],
            })
        return papers

    def __str__(self) -> str:
        return self.text



def _auto_index_from_result(result: OnlineRetrievalResult):
    """从结构化结果中提取高分论文，自动写入 kb_missing_papers.json"""
    if not result.scored_results:
        return
    try:
        import json, os
        from datetime import datetime
        from utils.path_tool import get_abs_path
        path = get_abs_path("data/kb_missing_papers.json")
        existing = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f).get("papers", {})

        updated = False
        for paper, score in result.scored_results:
            if score < 0.70:
                continue
            title_lower = paper.title.strip().lower()
            matched_key = None
            for k in existing.keys():
                if title_lower in k or k in title_lower:
                    matched_key = k
                    break
            if matched_key:
                # 已存在：补全缺失字段
                entry = existing[matched_key]
                if not entry.get("abstract") and paper.abstract:
                    entry["abstract"] = paper.abstract
                    updated = True
                if not entry.get("authors") and paper.authors:
                    entry["authors"] = paper.authors
                    updated = True
                if not entry.get("year") and paper.year:
                    entry["year"] = paper.year
                    updated = True
                if not entry.get("doi") and paper.doi:
                    entry["doi"] = paper.doi
                    updated = True
                continue
            key = title_lower
            existing[key] = {
                "display_name": paper.title,
                "online_query": paper.title,
                "authors": paper.authors,
                "year": paper.year,
                "venue": paper.venue,
                "doi": paper.doi,
                "url": paper.url,
                "abstract": paper.abstract or "",
                "status": "auto_indexed",
                "verified": False,
                "added_at": datetime.now().isoformat(),
            }
            updated = True

        if updated:
            from agent.tools.agent_tools import _save_kb_missing_papers
            _save_kb_missing_papers(existing)
    except Exception:
        pass

def search_academic_papers_core(query: str, candidate: str = "") -> OnlineRetrievalResult:
    """在线学术检索核心接口 —— 返回不可变结构化结果。"""
    from agent.tools.agent_tools import online_pipeline as _pipeline
    from agent.retrieval.academic_client import AcademicDataClient, SearchIntent

    if candidate:
        candidate_type = AcademicDataClient._infer_candidate_type(candidate)
        intent = SearchIntent(
            candidate=candidate,
            candidate_type=candidate_type,
            keyword="",
            fallback_query=query,
        )
        result = _pipeline._execute_intent_structured(intent)
    else:
        intent = SearchIntent(
            candidate="",
            candidate_type="unknown",
            keyword="",
            fallback_query=query,
        )
        result = _pipeline._execute_intent_structured(intent)

    # auto-index: 在线检索结果自动写入 kb_missing_papers.json
    _auto_index_from_result(result)
    return result

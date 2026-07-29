"""Agent 工具集：7 个工具 - 本地检索 + 在线检索 + 元数据 + 引用 + 对比 + KB缺失标记 + 综述模式"""
import json
import os
import time
from datetime import datetime
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from agent.retrieval import OnlineRetrievalPipeline
from agent.retrieval.academic_client import SearchIntent, AcademicDataClient
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

import json
import os
import time
from datetime import datetime
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
from agent.retrieval import OnlineRetrievalPipeline
from agent.retrieval.academic_client import SearchIntent, AcademicDataClient
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

rag = RagSummarizeService()
online_pipeline = OnlineRetrievalPipeline()

KB_MISSING_PAPERS_PATH = get_abs_path("data/kb_missing_papers.json")
KB_MISSING_INDEX_PATH = get_abs_path("data/kb_missing_index.json")


def _load_kb_missing_papers() -> dict:
    """加载 kb_missing_papers.json → 返回 papers 字典"""
    if not os.path.exists(KB_MISSING_PAPERS_PATH):
        return {}
    with open(KB_MISSING_PAPERS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("papers", {})


def _save_kb_missing_papers(papers: dict):
    """保存 kb_missing_papers.json"""
    from utils.file_handler import safe_json_dump
    safe_json_dump({"papers": papers}, KB_MISSING_PAPERS_PATH)


def _auto_index_online_papers(papers: list, local_docs: list | None = None,
                               scored: list | None = None, min_score: float = 0.70):
    """在线搜索结果自动写入 kb_missing_papers.json（仅当本地 KB 未命中且尚未索引）。
    若提供 scored 列表 [(paper, score), ...], 仅索引 score ≥ min_score 的论文。"""
    if local_docs:
        return  # 本地 KB 已有，跳过

    if scored is not None and min_score > 0:
        papers = [p for p, s in scored if s >= min_score]

    existing = _load_kb_missing_papers()
    updated = False
    for p in papers:
        title_lower = p.title.strip().lower()
        already_exists = any(
            title_lower in k or k in title_lower
            for k in existing.keys()
        )
        if already_exists:
            continue
        existing[title_lower] = {
            "display_name": p.title,
            "online_query": p.title,
            "authors": p.authors,
            "year": p.year,
            "venue": p.venue,
            "doi": p.doi,
            "url": p.url,
            "abstract": (p.abstract or ""),
            "status": "auto_indexed",
            "verified": False,
            "added_at": datetime.now().isoformat(),
        }
        logger.info(f"[AutoIndex] 已写入 kb_missing: {p.title[:80]}")
        updated = True
    if updated:
        _save_kb_missing_papers(existing)

# ── 共享状态（由 ReactAgent.execute_stream() 注入）──




def _log_tool_call(name: str, query: str):
    logger.info(f"[Tool] 调用 {name}: {query[:200]}")


def _log_tool_result(name: str, result: str, start: float):
    elapsed = time.time() - start
    summary = result[:300].replace("\n", " ")
    logger.info(f"[Tool] {name} 完成 ({elapsed:.1f}s) → {summary}")


# ── KB 缺失索引 ──

def _load_kb_missing_index() -> set:
    if not os.path.exists(KB_MISSING_INDEX_PATH):
        return set()
    with open(KB_MISSING_INDEX_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("titles", []))


def _save_kb_missing_index(index: set):
    from utils.file_handler import safe_json_dump
    safe_json_dump({"titles": sorted(index), "updated_at": str(len(index))}, KB_MISSING_INDEX_PATH)


# ── 在线检索内部函数（Commit 2: SearchIntent 驱动）──

def _search_academic_papers_internal(query: str, candidate: str = "", ctx=None) -> str:
    """内部在线检索：委托 search_academic_papers_core，保持字符串返回兼容。"""
    from agent.retrieval.retrieval_pipeline import search_academic_papers_core

    _log_tool_call("search_academic_papers",
                   f"candidate={candidate}" if candidate else query)
    start = time.time()
    result = search_academic_papers_core(query, candidate)
    _log_tool_result("search_academic_papers", result.text, start)

    # Auto-index
    if result.scored_results:
        _auto_index_online_papers([], scored=list(result.scored_results), min_score=0.70)

    # 标记在线搜索结果已获取
    if ctx is not None:
        ctx.retrieval_state.online_results_obtained = True

    return result.text


# ── 7 个工具 ──

@tool(description="从本地论文向量库中检索相关论文全文片段，返回带编号引用[N]的学术资料内容（含论文标题、章节、页码）。适用于查找具体方法、实验数据、结论等。")
def academic_search(query: str) -> str:
    if err:
        return err
    _log_tool_call("academic_search", query)
    start = time.time()
    result = rag.rag_summarize(query)
    _log_tool_result("academic_search", result, start)
    return result


@tool(description="在线检索学术数据库（arXiv/OpenAlex/DBLP/Crossref/Semantic Scholar），查找最新发表的论文元数据（标题/作者/摘要/来源）。适用于查找尚未加入本地知识库的最新论文、验证论文身份。")
def search_academic_papers(query: str) -> str:
    if err:
        return err
    return _search_academic_papers_internal(query, candidate=query)


@tool(description="根据精确论文标题获取完整元数据：全部作者、摘要、发表年份、DOI、期刊/会议、链接。适用于获取某篇已知论文的详细信息。")
def fetch_paper_metadata(title: str) -> str:
    if err:
        return err
    _log_tool_call("fetch_paper_metadata", title)
    start = time.time()

    papers = online_pipeline.client.search(title, max_results=5)
    if not papers:
        return f"[PAPER_NOT_FOUND] 未找到匹配「{title}」的论文。"

    title_lower = title.strip().lower()
    best = None
    for p in papers:
        if p.title.strip().lower() == title_lower:
            best = p
            break
    if not best:
        best = papers[0]

    lines = [
        f"标题: {best.title}",
        f"作者: {', '.join(best.authors) if best.authors else '未知'}",
        f"年份: {best.year or '未知'}",
        f"来源: {best.source}",
    ]
    if best.doi:
        lines.append(f"DOI: {best.doi}")
    if best.venue:
        lines.append(f"发表: {best.venue}")
    if best.url:
        lines.append(f"链接: {best.url}")
    if best.abstract:
        lines.append(f"摘要: {best.abstract}")
    if best.citation_count:
        lines.append(f"引用数: {best.citation_count}")

    result = "\n".join(lines)
    _log_tool_result("fetch_paper_metadata", result, start)
    return result


@tool(description="根据精确论文标题获取引用计数。适用于了解某篇论文的学术影响力。")
def fetch_citation_info(title: str) -> str:
    if err:
        return err
    _log_tool_call("fetch_citation_info", title)
    start = time.time()

    papers = online_pipeline.client.search(title, max_results=5)
    if not papers:
        return f"[PAPER_NOT_FOUND] 未找到匹配「{title}」的论文。"

    title_lower = title.strip().lower()
    best = None
    for p in papers:
        if p.title.strip().lower() == title_lower:
            best = p
            break
    if not best:
        best = papers[0]

    count = best.citation_count or 0
    source = best.source
    result = f"《{best.title}》引用次数: {count}（来源: {source}）"
    _log_tool_result("fetch_citation_info", result, start)
    return result


def compare_papers(titles_str: str, ctx=None) -> str:
    """同时检索并对比多篇论文（2-4篇）。对每篇论文分别查找本地知识库片段和在线元数据。
    标题用分号(;)分隔。ctx 可传入 ExecutionContext 用于预算检查。"""
    if ctx is not None and not ctx.policy.try_consume():
        return "[TOOL_BUDGET_EXHAUSTED] 工具调用次数已达上限，请基于已有信息直接回答。"
    if ctx is None:
        if err:
            return err
    _log_tool_call("compare_papers", titles_str)

    titles = [t.strip() for t in titles_str.split(";") if t.strip()]
    if len(titles) < 2:
        return "请提供至少 2 篇论文标题，用分号 (;) 分隔。"
    if len(titles) > 4:
        titles = titles[:4]

    start = time.time()
    kb_missing_index = _load_kb_missing_index()
    results = []
    for i, title in enumerate(titles):
        results.append(f"\n=== 论文 {i+1}: {title} ===")

        # KB 缺失索引命中 → 跳过本地检索，直接走在线
        title_lower = title.strip().lower()
        in_kb_missing = any(title_lower in t.lower() or t.lower() in title_lower for t in kb_missing_index)

        local_docs = []
        if in_kb_missing:
            results.append("[本地KB] 论文已在 KB 缺失索引中，跳过本地检索")
        else:
            local_docs = rag.retriever_docs(title)

        if local_docs:
            results.append(f"[本地KB] 找到 {len(local_docs)} 个相关片段:")
            for doc in local_docs[:2]:
                meta = doc.metadata
                src = meta.get("paper_title", "") or meta.get("source_file", "")
                sec = meta.get("section", "")
                content_preview = doc.page_content[:200].replace("\n", " ")
                results.append(f"  - 来源: {src} | 章节: {sec}")
                results.append(f"    内容: {content_preview}...")
            if len(local_docs) >= 3:
                continue
        elif not in_kb_missing:
            results.append("[本地KB] 未找到相关片段")

        papers = online_pipeline.client.search(title, max_results=3)
        if papers:
            _auto_index_online_papers(papers, local_docs=local_docs)
            p = papers[0]
            results.append(f"[在线] {p.title} | {', '.join(p.authors[:3]) if p.authors else ''} | {p.year} | {p.source}")
            if p.abstract:
                results.append(f"  摘要: {p.abstract}")

    result = "\n".join(results)
    _log_tool_result("compare_papers", result, start)
    return result


@tool(description="将某篇论文标记为「本地知识库缺失」。后续检索到该论文时会自动跳过本地搜索，直接引导使用在线工具。")
def mark_paper_not_in_kb(title: str) -> str:
    if err:
        return err
    _log_tool_call("mark_paper_not_in_kb", title)

    index = _load_kb_missing_index()
    title_normalized = title.strip()
    if title_normalized.lower() in {t.lower() for t in index}:
        return f"「{title_normalized}」已在 KB 缺失索引中。"
    index.add(title_normalized)
    _save_kb_missing_index(index)
    logger.info(f"[KB Missing] 已标记: {title_normalized}")
    return f"已标记「{title_normalized}」为 KB 缺失，后续将跳过本地检索。"


@tool(description="触发文献综述模式。对某个研究领域进行系统性搜索和全面归纳。调用后 Agent 将切换为综述视角，进行多轮广泛检索。")
def start_literature_review(topic: str) -> str:
    if err:
        return err
    _log_tool_call("start_literature_review", topic)
    return f"__REVIEW_MODE__:{topic}"

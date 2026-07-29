"""证据判断模块：LLM 逐 chunk 判断相关性、充分性，以及逐 subject 证据评估。

两个函数均为生成器/yield 形式（用于流式输出进度提示），通过传入的 chat_model 实例完成判断。
"""
import re
from typing import Generator

from model.factory import chat_model
from utils.logger_handler import logger


def judge_chunks(chunks: list, query: str) -> Generator[dict, None, dict]:
    """LLM 逐 chunk 判断相关性 + 充分性 + 生成 refine_query
    
    Yields:
        {"type": "system", "content": "...", "name": "system"}  进度提示
        {"type": "text", "content": "...", "name": "system"}     错误信息
    Returns:
        {"sufficient": bool, "relevant_chunks": list, "refine_query": str, "judgment": str}
    """
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
    for chunk in chat_model.stream(prompt):
        if chunk.content and isinstance(chunk.content, str):
            judgment += chunk.content

    sufficient = "SUFFICIENT" in judgment.upper() and "INSUFFICIENT" not in judgment.upper()

    relevant_indices: set[int] = set()
    for m in re.finditer(r"\[(\d+)\]\s*\[相关\]", judgment):
        relevant_indices.add(int(m.group(1)))

    relevant_chunks = [chunks[i - 1] for i in sorted(relevant_indices) if 1 <= i <= len(chunks)]

    refine_query = query
    m_refine = re.search(r"REFINE_QUERY:\s*(.+?)(?:\n|$)", judgment, re.IGNORECASE)
    if m_refine:
        refine_query = m_refine.group(1).strip()

    return {
        "sufficient": sufficient,
        "relevant_chunks": relevant_chunks,
        "refine_query": refine_query,
        "judgment": judgment,
    }


def judge_subject_evidence(docs: list, subject: str, aspects: str) -> dict:
    """逐 subject 判断：是否命中目标论文 + 证据是否覆盖对比维度 + 缺失信息 + 改写建议
    
    Returns:
        {"sufficient": bool, "paper_hit": bool, "missing_dimensions": str, "refine_query": str}
    """
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
    for chunk in chat_model.stream(prompt):
        if chunk.content and isinstance(chunk.content, str):
            judgment += chunk.content

    judgment_clean = judgment.strip().rstrip("*").rstrip()

    paper_hit = "PAPER_HIT: YES" in judgment_clean.upper() or "PAPER_HIT:YES" in judgment_clean.upper()
    sufficient = "SUFFICIENT" in judgment_clean.upper() and "INSUFFICIENT" not in judgment_clean.upper()

    m_missing = re.search(r"INSUFFICIENT:\s*(.+?)(?:\n|$)", judgment_clean, re.IGNORECASE)
    missing_dimensions = m_missing.group(1).strip().rstrip("*").rstrip() if m_missing else ""

    # 用 rewrite_query 根据缺失维度生成改写检索词
    if not sufficient and paper_hit and missing_dimensions:
        from agent.query_planner import rewrite_query
        refine_query = rewrite_query(
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

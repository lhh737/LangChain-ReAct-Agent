"""答案生成模块：统一编号引用构建、LLM 流式生成、引用校验、COMPARE chunk 均衡分配"""
import re
from typing import Generator

from langchain_core.messages import SystemMessage, HumanMessage
from model.factory import chat_model
from utils.logger_handler import logger


def generate_answer(
    chunks: list,
    query: str,
    system_prompt: str,
    *,
    extra_context: str = "",
    max_chunks: int = 0,
    max_tokens: int = 5000,
    memory_context: str = "",
    online_blocks: list | None = None,
) -> Generator[dict, None, None]:
    """从 raw chunks + online_blocks 构建统一编号引用上下文，流式生成答案。

    Args:
        chunks: 本地检索 Document 列表
        query: 用户原始问题
        system_prompt: 已加载的 Prompt 模板文本
        extra_context: 额外上下文（如 compare_papers 结果）
        max_chunks: chunk 条数上限（0 不限制）
        max_tokens: 上下文整体 token 上限（~2 chars/token 估算）
        memory_context: 相关性过滤后的历史对话 + 长期事实
        online_blocks: [{"title": str, "source": str, "content": str}, ...]

    Yields:
        {"type": "text", "content": "...", "name": "assistant" | "system"}
        {"type": "references", "content": "...", "name": "system"}
    """
    from agent.query_planner import strip_pipeline_numbering

    online_blocks = online_blocks or []
    for block in online_blocks:
        block["content"] = strip_pipeline_numbering(block.get("content", ""))

    if not chunks and not extra_context and not online_blocks:
        yield {"type": "text", "content": "[系统] 无可用检索结果", "name": "system"}
        return

    ctx_chunks = chunks[:max_chunks] if max_chunks > 0 else chunks

    # 构建统一编号的引用块
    lines: list[str] = []
    for i, doc in enumerate(ctx_chunks, 1):
        meta = doc.metadata
        title = meta.get("paper_title", "未知")
        section = meta.get("section", "未知")
        ps = meta.get("page_start") or meta.get("page")
        pe = meta.get("page_end") or meta.get("page")
        page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}" if ps and pe else "未知"
        lines.append(f"[{i}] 来源：《{title}》；章节：{section}；页码：{page}；内容：{doc.page_content}")

    online_start = len(ctx_chunks) + 1
    for i, block in enumerate(online_blocks, online_start):
        title = block.get("title", "未知")
        source = block.get("source", "在线")
        content = block.get("content", "")
        lines.append(f"[{i}] [在线]《{title}》| 来源：{source}\n{content}")

    context = ""
    if memory_context:
        context += f"[对话上下文]\n{memory_context}\n\n"
    context += "\n\n".join(lines)

    if extra_context:
        context += f"\n\n---\n{extra_context}"

    # 整体截断
    char_limit = max_tokens * 2
    if len(context) > char_limit:
        cut = context.rfind("\n\n", 0, char_limit)
        if cut < 0 or cut < char_limit * 0.6:
            cut = char_limit
        context = context[:cut] + "\n\n...[上下文超出 token 限制，后续内容已截断]"
        logger.info(f"[Truncate] 上下文截断于 ~{cut} chars, limit={char_limit}")

    system_msg = SystemMessage(content=system_prompt)
    user_msg = HumanMessage(content=f"用户问题：{query}\n\n检索结果：\n{context}")

    collected_text: list[str] = []
    for chunk in chat_model.stream([system_msg, user_msg]):
        if chunk.content and isinstance(chunk.content, str):
            collected_text.append(chunk.content)
            yield {"type": "text", "content": chunk.content, "name": "assistant"}

    final_text = "".join(collected_text)

    # 引用校验
    max_n = len(ctx_chunks) + len(online_blocks)
    cited = set(int(m) for m in re.findall(r"\[(\d+)\]", final_text))
    invalid = sorted(n for n in cited if n < 1 or n > max_n)
    if invalid:
        yield {"type": "text", "content": f"\n\n> 引用校验警告：无效引用 {invalid}，有效范围 [1-{max_n}]。", "name": "system"}

    if max_n > 0 and not cited:
        logger.warning("[Citation] 有 chunk 但回答零引用")
        yield {"type": "text", "content": "\n\n> 引用校验警告：回答未引用任何证据编号，请忽略以上回答并重新提问。", "name": "system"}
        return

    if any(re.search(pat, final_text) for pat in [r"\[N\]", r"\[n\]", r"\[数字\]", r"\[编号\]", r"\[\?\]"]):
        logger.warning("[Placeholder] 检测到占位符引用")
        yield {"type": "text", "content": "\n[系统提示] 回答中包含无效引用占位符，已拦截。\n", "name": "system"}
        return

    # 输出引用元信息映射表
    if max_n > 0:
        ref_lines = []
        for i, doc in enumerate(ctx_chunks, 1):
            meta = doc.metadata
            title = meta.get("paper_title", "未知")
            section = meta.get("section", "未知")
            ps = meta.get("page_start") or meta.get("page")
            pe = meta.get("page_end") or meta.get("page")
            page = f"p.{ps}" if ps == pe else f"pp.{ps}-{pe}" if ps and pe else "未知"
            ref_lines.append(f"[{i}] 《{title}》| {section} | {page}")

        online_start_ref = len(ctx_chunks) + 1
        for i, block in enumerate(online_blocks, online_start_ref):
            title = block.get("title", "未知")
            source = block.get("source", "在线")
            ref_lines.append(f"[{i}] [在线]《{title}》| 来源：{source}")

        yield {"type": "references", "content": "\n\n".join(ref_lines), "name": "system"}


def verify_citations(answer: str, tool_results: list) -> str:
    """校验回答中的 [N] 引用编号。返回警告字符串（可能为空）。"""
    acad_results = [r for r in tool_results if r["name"] == "academic_search" and r.get("is_valid")]
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


def balance_chunks_by_subject(
    chunks: list, counts: dict[str, int], max_total: int, min_per: int, max_per: int
) -> list:
    """按 subject 均衡分配 chunk：每 subject 保留 min_per~max_per 条，总数不超过 max_total"""
    if len(chunks) <= max_total:
        return chunks

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
            if subj_lower in content:
                matched = subj
                break
        if matched:
            groups[matched].append(doc)
        else:
            unassigned.append(doc)

    result = []
    remaining = max_total

    for subj in subject_keys:
        take = min(min_per, len(groups[subj]), remaining)
        result.extend(groups[subj][:take])
        remaining -= take

    for subj in subject_keys:
        if remaining <= 0:
            break
        already = min(min_per, len(groups[subj]))
        extra = min(max_per - already, len(groups[subj]) - already, remaining)
        if extra > 0:
            result.extend(groups[subj][already:already + extra])
            remaining -= extra

    if remaining > 0 and unassigned:
        result.extend(unassigned[:remaining])

    return result

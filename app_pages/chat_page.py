"""科研论文问答对话页面 — 流式输出 + 工具面板 + 记忆管理"""
import streamlit as st
from agent.react_agent import ReactAgent

# ── CSS 常量 ──

PAGE_CSS = """
<style>
/* ── 全局 ── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
}
h1, h2, h3 {
    font-weight: 600;
}

/* ── 主标题 ── */
.main-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}
.main-subtitle {
    font-size: 0.9rem;
    opacity: 0.65;
    margin-bottom: 1.5rem;
}

/* ── 状态指示器 ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 8px;
    background: rgba(59, 92, 204, 0.1);
    border: 1px solid rgba(59, 92, 204, 0.2);
    font-size: 0.85rem;
    margin: 4px 0;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #5b8def;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

/* ── 工具卡片 ── */
.tool-card {
    border: 1px solid rgba(128, 128, 128, 0.18);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    background: rgba(128, 128, 128, 0.04);
    font-size: 0.85rem;
}
.tool-card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
}
.tool-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}
.tool-badge.local {
    background: rgba(59, 130, 246, 0.15);
    color: #3b82f6;
}
.tool-badge.online {
    background: rgba(219, 39, 119, 0.15);
    color: #db2777;
}
.tool-badge.memory {
    background: rgba(5, 150, 105, 0.15);
    color: #059669;
}

/* ── 引用来源 ── */
.ref-block {
    white-space: pre-wrap;
    border-left: 3px solid rgba(59, 130, 246, 0.55);
    padding: 8px 12px;
    margin: 4px 0;
    background: rgba(128, 128, 128, 0.04);
    border-radius: 0 6px 6px 0;
    font-size: 0.85rem;
    line-height: 1.5;
}
.ref-scroll {
    max-height: 360px;
    overflow-y: auto;
}

/* ── 侧边栏 ── */
section[data-testid="stSidebar"] {
    background: rgba(128, 128, 128, 0.02);
}
.sidebar-section {
    padding: 8px 0;
    border-bottom: 1px solid rgba(128, 128, 128, 0.12);
    margin-bottom: 8px;
}
.sidebar-section:last-child {
    border-bottom: none;
}

/* ── 对话消息 ── */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 12px 16px;
}
</style>
"""

# ── 工具图标映射 ──
TOOL_ICONS = {
    "academic_search": ("📚", "local"),
    "search_academic_papers": ("🔍", "online"),
    "fetch_paper_metadata": ("📋", "online"),
    "fetch_citation_info": ("📊", "online"),
    "compare_papers": ("⚖️", "local"),
    "mark_paper_not_in_kb": ("🏷️", "memory"),
    "start_literature_review": ("📖", "memory"),
    "kb_missing_abstract": ("💾", "memory"),
}

TOOL_LABELS = {
    "academic_search": "本地知识库检索",
    "search_academic_papers": "在线学术搜索",
    "fetch_paper_metadata": "获取论文元数据",
    "fetch_citation_info": "获取引用信息",
    "compare_papers": "论文对比分析",
    "mark_paper_not_in_kb": "标记 KB 缺失",
    "start_literature_review": "文献综述模式",
    "kb_missing_abstract": "KB 预存元数据",
}

def _render_references(structured_refs: list, fallback_content: str = ""):
    """渲染引用来源：优先结构化列表，回退到字符串拆分"""
    import html
    if structured_refs:
        parts = []
        for ref in structured_refs:
            idx = ref.get("index", "?")
            title = ref.get("title", "未知")
            source_type = ref.get("source_type", "")
            source = ref.get("source", "")
            authors = ref.get("authors", [])
            year = ref.get("year", "")
            doi = ref.get("doi", "")
            url = ref.get("url", "")
            evidence_type = ref.get("evidence_type", "abstract")
            evidence_text = ref.get("evidence_text", "")

            type_label = {"online": "[在线]", "local": "[本地]"}.get(source_type, "")
            author_str = ", ".join(authors[:3]) if authors else ""
            if len(authors) > 3:
                author_str += " 等"

            lines = []
            lines.append(f"[{idx}] {type_label}《{html.escape(title)}》")
            if author_str:
                lines.append(f"作者：{html.escape(author_str)}")
            if year:
                lines.append(f"年份：{html.escape(str(year))}")
            lines.append(f"来源：{html.escape(source)}")
            lines.append(f"证据类型：{html.escape(evidence_type)}")
            if doi:
                lines.append(f"DOI：{html.escape(doi)}")
            if url:
                escaped = html.escape(url)
                if len(url) > 80:
                    lines.append(f'URL：<a href="{escaped}" target="_blank">{escaped[:80]}...</a>')
                else:
                    lines.append(f'URL：<a href="{escaped}" target="_blank">{escaped}</a>')
            if evidence_text:
                lines.append("")
                lines.append(html.escape(evidence_text))

            block_html = "<br>".join(lines)
            parts.append(f'<div class="ref-block">{block_html}</div>')

        st.markdown(f'<div class="ref-scroll">{"".join(parts)}</div>', unsafe_allow_html=True)
    elif fallback_content:
        # Legacy fallback: split by double newline
        parts = [f'<div class="ref-block">{html.escape(l.strip())}</div>'
                 for l in fallback_content.split("\n\n") if l.strip()]
        st.markdown(f'<div class="ref-scroll">{"".join(parts)}</div>', unsafe_allow_html=True)


def _render_tool_card(name: str, content: str, query: str = "", elapsed: float = 0,
                      meta: dict | None = None):
    """以卡片样式渲染工具调用结果"""
    icon, category = TOOL_ICONS.get(name, ("🔧", "local"))
    label = TOOL_LABELS.get(name, name)
    badge_class = f"tool-badge {category}"

    with st.container():
        st.markdown(
            f'<div class="tool-card">'
            f'<div class="tool-card-header">'
            f'<span>{icon}</span>'
            f'<strong>{label}</strong>'
            f'<span class="{badge_class}">{["本地","在线","记忆"][["local","online","memory"].index(category)]}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if query:
            st.caption(f"🔎 `{query[:80]}`")
        if elapsed:
            st.caption(f"⏱ {elapsed:.1f}s")

        if meta:
            _render_meta(name, meta)

        if content:
            with st.expander("查看详情", expanded=False):
                st.text(content[:500])


def _render_meta(name: str, meta: dict):
    """按工具类型渲染 meta 字段"""
    if name in ("academic_search",):
        sources = meta.get("sources", [])
        count = meta.get("count", 0)
        if count:
            st.caption(f"📄 返回 {count} 个片段")
        if sources:
            for src in sources[:5]:
                title = src.get("title", "?")
                section = src.get("section", "?")
                page = src.get("page", "?")
                preview = src.get("preview", "")[:60]
                st.markdown(
                    f'<div class="ref-block">'
                    f'<strong>{title}</strong> · {section} · p.{page}<br>'
                    f'<span style="color:#6b7280">{preview}...</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    elif name in ("search_academic_papers",):
        papers = meta.get("papers", [])
        if papers:
            st.caption(f"📄 匹配 {len(papers)} 篇论文")
            for p in papers:
                authors = ", ".join(p.get("authors", [])[:3])
                year = p.get("year", "")
                source = p.get("source", "")
                score = p.get("score", 0)
                abstract = p.get("abstract", "")[:150]
                score_bar = "🟢" if score >= 0.85 else ("🟡" if score >= 0.70 else "🔴")
                st.markdown(
                    f'<div class="ref-block">'
                    f'<strong>{p.get("title", "?")}</strong><br>'
                    f'{authors} · {year} · {source} · {score_bar} {score:.2f}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if abstract:
                    st.caption(f"摘要: {abstract}...")
        else:
            st.caption("无匹配论文（全部低于阈值）")

    elif name == "kb_missing_abstract":
        parts = []
        if meta.get("authors"):
            parts.append(f"作者: {', '.join(meta['authors'][:5])}")
        if meta.get("year"):
            parts.append(f"年份: {meta['year']}")
        if meta.get("venue"):
            parts.append(f"发表: {meta['venue']}")
        if meta.get("doi"):
            parts.append(f"DOI: `{meta['doi']}`")
        if meta.get("url"):
            parts.append(f"[链接]({meta['url']})")
        if parts:
            st.caption(" · ".join(parts))

    elif name == "compare_papers":
        titles = meta.get("titles", [])
        if titles:
            st.caption(f"📄 对比论文: {' · '.join(titles)}")


def render_chat_page():
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    # --- Session state init ---
    if "agent" not in st.session_state:
        st.session_state.agent = ReactAgent()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "tool_history" not in st.session_state:
        st.session_state.tool_history = []

    # --- Sidebar ---
    with st.sidebar:
        st.markdown("### 📊 会话状态")

        turn_count = sum(1 for m in st.session_state.messages if m.get("role") == "user")

        col1, col2 = st.columns(2)
        col1.metric("对话轮次", turn_count)
        col2.metric("工具调用", len(st.session_state.tool_history))

        st.divider()

        # 长期事实
        facts = st.session_state.agent.fact_store.get_facts_text()
        if facts:
            with st.expander("🧠 长期事实", expanded=False):
                st.caption(facts[:400])

        # 累积摘要
        summary_msg = st.session_state.agent.summary.get_summary_message()
        if summary_msg:
            with st.expander("📋 累积摘要", expanded=False):
                st.caption(summary_msg["content"][:300])

        # 工具调用记录
        if st.session_state.tool_history:
            with st.expander("🔧 工具调用记录", expanded=False):
                for entry in st.session_state.tool_history[-10:]:
                    icon, _ = TOOL_ICONS.get(entry.get("name", ""), ("🔧", "local"))
                    query_str = entry.get("query", "")
                    elapsed_str = f" · {entry['elapsed']:.1f}s" if entry.get("elapsed") else ""
                    st.caption(f"{icon} {entry.get('name', '?')}{elapsed_str}")
                    if query_str:
                        st.caption(f"&nbsp;&nbsp;&nbsp;&nbsp;`{query_str[:50]}`")

        st.divider()

        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = []
            st.session_state.tool_history = []
            st.rerun()

    # --- Main chat area ---
    st.markdown('<div class="main-title">📄 PaperMind-科研论文问答系统</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">多意图 Agent · 本地知识库 + 在线学术检索 · '
        'QA / 对比 / 综述</div>',
        unsafe_allow_html=True,
    )

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("type") == "tool":
                _render_tool_card(
                    name=msg.get("name", "unknown"),
                    content=msg.get("content", ""),
                    query=msg.get("query", ""),
                    elapsed=msg.get("elapsed", 0),
                    meta=msg.get("meta"),
                )
            elif msg.get("type") == "references":
                ref_hist_content = msg.get("content", "")
                structured_refs = msg.get("references", [])
                from utils.logger_handler import logger
                logger.info(
                    "[CitationTrace][frontend_history_render] len=%d newline_count=%d structured_count=%d",
                    len(ref_hist_content), ref_hist_content.count("\n"), len(structured_refs),
                )
                with st.expander("📎 引用来源", expanded=False):
                    _render_references(structured_refs, ref_hist_content)
            else:
                st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("💬 请输入你的科研问题...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})

        with st.chat_message("assistant"):
            text_placeholder = st.empty()
            tool_placeholder = st.empty()
            status_placeholder = st.empty()
            collected_text: list[str] = []

            for chunk in st.session_state.agent.execute_stream(prompt):
                chunk_type = chunk.get("type", "text")

                if chunk_type == "intent":
                    intent_map = {"qa": "问答", "compare": "对比分析", "review": "文献综述"}
                    intent_label = intent_map.get(chunk["content"], chunk["content"])
                    with st.sidebar:
                        st.info(f"🎯 意图识别: **{intent_label}**")

                elif chunk_type == "text":
                    collected_text.append(chunk["content"])
                    text_placeholder.markdown("".join(collected_text) + "▌")

                elif chunk_type == "references":
                    ref_content = chunk.get("content", "")
                    structured_refs = chunk.get("references", [])
                    # === CitationTrace: frontend receive ===
                    from utils.logger_handler import logger
                    logger.info(
                        "[CitationTrace][frontend_receive] len=%d newline_count=%d structured_count=%d",
                        len(ref_content), ref_content.count("\n"), len(structured_refs),
                    )
                    # === end CitationTrace ===
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ref_content,
                        "type": "references",
                        "references": structured_refs,
                    })
                    with tool_placeholder.container():
                        with st.expander("📎 引用来源", expanded=False):
                            _render_references(structured_refs, ref_content)

                elif chunk_type == "tool":
                    tool_name = chunk.get("name", "unknown")
                    tool_content = chunk.get("content", "")
                    tool_query = chunk.get("query", "")
                    tool_elapsed = chunk.get("elapsed", 0)
                    tool_meta = chunk.get("meta")

                    st.session_state.tool_history.append({
                        "name": tool_name,
                        "content": tool_content,
                        "query": tool_query,
                        "elapsed": tool_elapsed,
                        "meta": tool_meta,
                    })

                    with tool_placeholder.container():
                        _render_tool_card(
                            name=tool_name, content=tool_content,
                            query=tool_query, elapsed=tool_elapsed, meta=tool_meta,
                        )

                elif chunk_type == "system":
                    content = chunk.get("content", "")
                    if content:
                        status_placeholder.markdown(
                            f'<div class="status-bar">'
                            f'<span class="status-dot"></span> {content}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

            # Remove cursor and status
            final_text = "".join(collected_text)
            text_placeholder.markdown(final_text)
            status_placeholder.empty()

            st.session_state.messages.append({
                "role": "assistant",
                "content": final_text,
                "type": "text",
            })

        st.rerun()

"""历史记录页面 — 会话对话 + 累积摘要 + 长期事实"""
import streamlit as st

HISTORY_CSS = """
<style>
.turn-container {
    border: 1px solid rgba(128, 128, 128, 0.15);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 12px 0;
    background: rgba(128, 128, 128, 0.03);
}
.turn-header {
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 8px;
    opacity: 0.7;
}
.turn-user {
    margin-bottom: 10px;
}
.turn-user-label {
    font-size: 0.8rem;
    font-weight: 500;
    opacity: 0.6;
    margin-bottom: 2px;
}
.turn-assistant {
    border-left: 3px solid rgba(59, 130, 246, 0.4);
    padding-left: 12px;
    margin-top: 6px;
}
.turn-assistant-label {
    font-size: 0.8rem;
    font-weight: 500;
    opacity: 0.6;
    margin-bottom: 2px;
}
.tool-inline {
    font-size: 0.82rem;
    padding: 4px 10px;
    margin: 4px 0;
    border-radius: 6px;
    background: rgba(128, 128, 128, 0.06);
    border: 1px solid rgba(128, 128, 128, 0.12);
}
.ref-inline {
    font-size: 0.82rem;
    padding: 6px 10px;
    margin: 4px 0;
    border-radius: 6px;
    background: rgba(59, 130, 246, 0.06);
    border: 1px solid rgba(59, 130, 246, 0.12);
}
.ref-scroll {
    max-height: 360px;
    overflow-y: auto;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid rgba(128, 128, 128, 0.15);
}
.fact-category {
    font-size: 0.9rem;
    font-weight: 600;
    margin: 10px 0 4px 0;
}
.fact-item {
    font-size: 0.88rem;
    margin: 2px 0 2px 16px;
    opacity: 0.85;
}
.summary-box {
    padding: 14px 18px;
    border-radius: 10px;
    background: rgba(128, 128, 128, 0.04);
    border: 1px solid rgba(128, 128, 128, 0.12);
    font-size: 0.9rem;
    line-height: 1.6;
}
.empty-hint {
    text-align: center;
    padding: 40px 0;
    opacity: 0.5;
    font-size: 0.95rem;
}
</style>
"""

TOOL_ICONS = {
    "academic_search": "📚",
    "search_academic_papers": "🔍",
    "fetch_paper_metadata": "📋",
    "fetch_citation_info": "📊",
    "compare_papers": "⚖️",
    "mark_paper_not_in_kb": "🏷️",
    "start_literature_review": "📖",
    "kb_missing_abstract": "💾",
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


def render_history_page():
    st.markdown(HISTORY_CSS, unsafe_allow_html=True)
    st.markdown("### 📝 历史记录")

    agent = st.session_state.get("agent")
    messages = st.session_state.get("messages", [])
    tool_history = st.session_state.get("tool_history", [])

    # ── Tab 1: 当前会话 ──
    st.markdown('<div class="section-title">💬 当前会话</div>', unsafe_allow_html=True)

    if not messages:
        st.markdown('<div class="empty-hint">暂无对话记录</div>', unsafe_allow_html=True)
    else:
        # 按轮次分组 (user 消息作为一轮的起点)
        turns = []
        current_turn = None
        for msg in messages:
            if msg["role"] == "user":
                if current_turn is not None:
                    turns.append(current_turn)
                current_turn = {"user": msg, "assistant_parts": []}
            elif current_turn is not None:
                current_turn["assistant_parts"].append(msg)
        if current_turn is not None:
            turns.append(current_turn)

        for i, turn in enumerate(turns, 1):
            with st.container():
                st.markdown(f'<div class="turn-container">', unsafe_allow_html=True)
                st.markdown(f'<div class="turn-header">第 {i} 轮</div>', unsafe_allow_html=True)

                # 用户消息
                user_content = turn["user"].get("content", "")
                st.markdown(f'<div class="turn-user-label">👤 用户</div>', unsafe_allow_html=True)
                st.markdown(user_content)

                # 助手消息部分
                if turn["assistant_parts"]:
                    st.markdown(f'<div class="turn-assistant-label">🤖 助手</div>', unsafe_allow_html=True)
                    st.markdown('<div class="turn-assistant">', unsafe_allow_html=True)

                    for part in turn["assistant_parts"]:
                        msg_type = part.get("type", "text")

                        if msg_type == "text":
                            st.markdown(part.get("content", ""))

                        elif msg_type == "tool":
                            icon = TOOL_ICONS.get(part.get("name", ""), "🔧")
                            label = TOOL_LABELS.get(part.get("name", ""), part.get("name", "?"))
                            query_str = part.get("query", "")
                            elapsed = part.get("elapsed", 0)
                            meta = part.get("meta")

                            st.markdown(
                                f'<div class="tool-inline">'
                                f'{icon} <strong>{label}</strong>'
                                f'{f" · {elapsed:.1f}s" if elapsed else ""}'
                                f'{f"<br><code>{query_str[:100]}</code>" if query_str else ""}'
                                f'</div>',
                                unsafe_allow_html=True,
                            )

                            # 展示工具返回的 meta 摘要
                            if meta:
                                if part.get("name") == "academic_search":
                                    count = meta.get("count", 0)
                                    if count:
                                        st.caption(f"返回 {count} 个片段")
                                elif part.get("name") == "search_academic_papers":
                                    papers = meta.get("papers", [])
                                    if papers:
                                        st.caption(f"匹配 {len(papers)} 篇论文")

                            # 工具内容可展开
                            content = part.get("content", "")
                            if content:
                                with st.expander("查看详情", expanded=False):
                                    st.text(content[:600])

                        elif msg_type == "references":
                            ref_content = part.get("content", "")
                            with st.expander("📎 引用来源", expanded=False):
                                parts = [f'<div class="ref-inline">{l.strip()}</div>' for l in ref_content.split("\n\n") if l.strip()]
                                st.markdown(f'<div class="ref-scroll">{"".join(parts)}</div>', unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

    # ── Tab 2: 工具调用统计 ──
    if tool_history:
        st.markdown('<div class="section-title">🔧 工具调用统计</div>', unsafe_allow_html=True)
        tool_counts = {}
        for entry in tool_history:
            name = entry.get("name", "unknown")
            tool_counts[name] = tool_counts.get(name, 0) + 1

        cols = st.columns(min(len(tool_counts), 4))
        for i, (name, count) in enumerate(tool_counts.items()):
            icon = TOOL_ICONS.get(name, "🔧")
            label = TOOL_LABELS.get(name, name)
            cols[i % 4].metric(f"{icon} {label}", count)

    # ── 短期记忆（持久化） ──
    if agent is not None:
        buffer = agent.memory.buffer
        if buffer:
            st.markdown('<div class="section-title">📝 短期记忆（已持久化）</div>', unsafe_allow_html=True)
            for msg in buffer:
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                ts = msg.get("timestamp", "")[:19]
                content = msg.get("content", "")
                st.markdown(
                    f'<div class="tool-inline">'
                    f'{role_icon} <strong>{msg["role"]}</strong>'
                    f'{f" · {ts}" if ts else ""}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(content)
                st.markdown("---")

    # ── 累积摘要 ──
    if agent is not None:
        summary_msg = agent.summary.get_summary_message()
        if summary_msg:
            st.markdown('<div class="section-title">📋 累积摘要</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="summary-box">{summary_msg["content"]}</div>',
                unsafe_allow_html=True,
            )

        # ── 长期事实 ──
        facts = agent.fact_store
        if facts and facts.facts:
            st.markdown('<div class="section-title">🧠 长期事实</div>', unsafe_allow_html=True)
            for category, items in facts.facts.items():
                if items:
                    st.markdown(f'<div class="fact-category">{category}</div>', unsafe_allow_html=True)
                    for item in items:
                        st.markdown(f'<div class="fact-item">• {item}</div>', unsafe_allow_html=True)

"""PaperMind-科研论文问答系统 — 基于 LangChain ReAct Agent + RAG 检索增强"""
import streamlit as st

st.set_page_config(
    page_title="PaperMind-科研论文问答系统",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="auto",
)

with st.sidebar:
    st.markdown("### 🧭 导航")
    page = st.radio(
        "选择页面",
        ["💬 对话", "📝 历史记录", "📖 关于"],
        label_visibility="collapsed",
    )

if page == "💬 对话":
    from app_pages.chat_page import render_chat_page
    render_chat_page()

elif page == "📝 历史记录":
    from app_pages.history_page import render_history_page
    render_history_page()

elif page == "📖 关于":
    ABOUT_CSS = """
    <style>
    .about-section {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem 0;
    }
    .about-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin: 20px 0;
    }
    .feature-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        background: rgba(128, 128, 128, 0.04);
    }
    .feature-card h4 {
        margin: 0 0 8px 0;
        font-size: 1rem;
    }
    .feature-card p {
        margin: 0;
        font-size: 0.85rem;
        opacity: 0.7;
        line-height: 1.5;
    }
    </style>
    """
    st.markdown(ABOUT_CSS, unsafe_allow_html=True)

    st.markdown('<div class="about-section">', unsafe_allow_html=True)
    st.markdown(
        '<div class="about-title">📄 PaperMind-科研论文问答系统</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "基于 LangChain + ReAct 范式 + RAG 检索增强，支持多意图路由、双通道检索、"
        "身份感知验证的PaperMind-科研论文问答系统。"
    )

    st.markdown("### 核心能力")
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

    features = [
        ("🧠 多意图路由", "自动识别 QA / 对比分析 / 文献综述三种意图，切换对应 Prompt 和检索策略"),
        ("📚 混合本地检索", "Chroma 向量库 + BM25 关键词 + Reranker 精排，中英文混合检索论文全文"),
        ("🌐 五源在线检索", "arXiv / OpenAlex / DBLP / Crossref / Semantic Scholar 三阶段管线"),
        ("🛡️ 身份感知验证", "DOI / arXiv ID / 标题 / 作者 / 年份 多信号交叉验证，四级置信度"),
        ("💾 知识库自动补全", "在线检索结果自动写入缺失索引，下次查询直接复用"),
        ("🧠 三层记忆系统", "短期缓冲 + LLM 累积摘要 + 长期事实提取，支持多轮对话"),
        ("📎 引用溯源", "回答中 [N] 编号关联检索片段来源，可展开查看完整引用"),
        ("⚡ 流式输出", "LLM 生成逐字流式输出，工具调用和检索进度实时可见"),
    ]

    for icon, desc in features:
        title, body = desc.split("：", 1) if "：" in desc else (desc, "")
        st.markdown(
            f'<div class="feature-card">'
            f'<h4>{icon} {title}</h4>'
            f'<p>{body}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 7 工具一览")
    tools_data = [
        ("📚", "academic_search", "本地", "Chroma + BM25 + Reranker 混合检索论文全文片段"),
        ("🔍", "search_academic_papers", "在线", "五源学术数据库聚合，三阶段管线检索"),
        ("📋", "fetch_paper_metadata", "在线", "精确标题获取完整元数据（作者/年份/DOI/摘要）"),
        ("📊", "fetch_citation_info", "在线", "精确标题获取引用计数"),
        ("⚖️", "compare_papers", "聚合", "多篇论文并行检索 + 结构化对比分析"),
        ("🏷️", "mark_paper_not_in_kb", "持久", "标记本地知识库缺失论文，自动跳过本地检索"),
        ("📖", "start_literature_review", "模式", "触发文献综述模式，广泛检索 + 分类归纳"),
    ]

    for icon, name, category, desc in tools_data:
        badge_color = {"本地": "rgba(59,130,246,0.15)", "在线": "rgba(219,39,119,0.15)", "聚合": "rgba(245,158,11,0.15)", "持久": "rgba(5,150,105,0.15)", "模式": "rgba(99,102,241,0.15)"}
        text_color = {"本地": "#3b82f6", "在线": "#db2777", "聚合": "#d97706", "持久": "#059669", "模式": "#6366f1"}
        st.markdown(
            f'{icon} **`{name}`** '
            f'<span style="background:{badge_color[category]};color:{text_color[category]};'
            f'padding:2px 8px;border-radius:12px;font-size:0.72rem;font-weight:500;">{category}</span> '
            f'— {desc}',
            unsafe_allow_html=True,
        )

    st.markdown("### 技术栈")
    st.markdown(
        "`Python 3.10+` · `LangChain 0.3` · `LangGraph 0.2` · `Streamlit 1.40` · "
        "`Chroma` · `BM25` · `DeepSeek-V3.2` · `BGE-M3` · `SiliconFlow API` · "
        "`arXiv` · `OpenAlex` · `DBLP` · `Crossref` · `Semantic Scholar`"
    )

    st.markdown('</div>', unsafe_allow_html=True)

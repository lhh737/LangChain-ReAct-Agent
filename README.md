<div align="center">

# PaperMind — 科研论文问答系统

**基于 LangChain + ReAct 范式 + RAG 检索增强的科研论文智能问答 Agent**

</div>

---

## 项目简介

多意图、状态感知的科研论文智能问答 Agent。系统根据用户问题自动识别意图（QA / 对比 / 综述），通过**本地 RAG 检索 + 在线学术搜索**双通道获取证据，经 LLM 推理后生成带引用编号的专业回答。前端提供 Streamlit 流式界面，实时展示工具调用、检索来源和推理过程。

### 核心能力

- **本地知识库检索**：Chroma 向量库 + BM25 关键词 + Reranker 精排，混合检索论文全文片段
- **在线学术搜索**：arXiv / OpenAlex / DBLP / Crossref / Semantic Scholar 五源聚合，三阶段管线（候选精确匹配 → 关键词消歧 → 改写变体兜底）
- **身份感知验证**：DOI / arXiv ID / 标题 / 作者 / 年份多信号交叉验证，四级置信度（EXACT → HIGH → MEDIUM → LOW）
- **自动知识库补全**：在线检索到的论文自动写入缺失索引（`kb_missing_papers.json`），下次查询直接复用预存元数据
- **证据 Token 预算分配**：分层 budget 策略（固定开销 → memory → extra → evidence），保障关键证据不丢失
- **统一引用编号**：本地 chunk + 在线 block 渲染为带 `[N]` 编号的统一引用上下文，回答后完成引用校验

## 技术架构

```
用户输入 (Streamlit)
      │
      ▼
┌──────────────────────────────────────────────────────┐
│                   IntentRouter                        │
│          QA / COMPARE / REVIEW 三意图分类              │
│     高置信正则优先 → LLM 兜底 → 关键词回退             │
└──────────────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────────┐
│               ReactAgent (execute_stream)             │
│  按意图路由：QA / COMPARE / REVIEW 三条独立管线         │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │ ExecutionContext (per-request 上下文)             │ │
│  │  · AgentExecutionPolicy (工具配额 15 次/请求)      │ │
│  │  · AgentRetrievalState (miss检测/本地KB禁用)      │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  Middleware: AgentCallback (工具调用日志 · LLM 调用日志) │
└──────────────────────────────────────────────────────┘
      │                           │
      ▼                           ▼
┌──────────────┐    ┌────────────────────────────┐
│  本地 RAG     │    │     在线检索管线              │
│              │    │                              │
│ Chroma 向量库 │    │ ┌─────┐ ┌─────┐ ┌─────┐   │
│ + BM25 关键词 │    │ │Stage1│→│Stage2│→│Stage3│   │
│ + Reranker   │    │ │候选精确│ │+关键词│ │改写变体│   │
│              │    │ └─────┘ └─────┘ └─────┘   │
└──────────────┘    │                              │
                    │ PaperIdentityValidator       │
                    │ CompositeRanker (身份+语义)   │
                    │ 身份早停 (EXACT/HIGH → 跳过   │
                    │   后续 stage)                 │
                    └────────────────────────────┘
      │                           │
      ▼                           ▼
┌──────────────────────────────────────────────────────┐
│             证据 Token 预算分配器 (EvidenceBudgeter)    │
│                                                       │
│  fixed cost → memory 截断 → extra 截断 → 证据选择      │
│  · 按 quality_score 排序，每 subject 最低 1 条保障       │
│  · 在线证据不低于 1 条，超预算安全降级                    │
│  · 最终引用：统一 [N] 编号渲染 + 元数据引用表              │
└──────────────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────────┐
│                    三层记忆系统                        │
│  ShortTermMemory (4 轮缓冲) · CumulativeSummary        │
│  (LLM 压缩) · FactStore (每 3 轮提取长期事实)           │
│  · 记忆 Jaccard 相似度过滤后注入回答上下文                │
└──────────────────────────────────────────────────────┘
```

### 7 工具一览

| 工具 | 类型 | 功能 |
|---|---|---|
| `academic_search` | 本地 | Chroma + BM25 + Reranker 混合检索论文全文片段，返回带 `[N]` 编号的内容 |
| `search_academic_papers` | 在线 | 五源学术数据库聚合搜索，自动构建 SearchIntent 走三阶段管线 |
| `fetch_paper_metadata` | 在线 | 精确标题 → 作者 / 年份 / DOI / 期刊 / 摘要 / 链接 |
| `fetch_citation_info` | 在线 | 精确标题 → 引用计数 |
| `compare_papers` | 聚合 | 多篇论文（2-4 篇）并行检索本地 KB + 在线元数据，结构化对比 |
| `mark_paper_not_in_kb` | 持久 | 标记论文为本地知识库缺失，后续自动跳过本地检索 |
| `start_literature_review` | 模式 | 触发文献综述模式，Agent 切换为广泛检索 + 分类归纳 |

## 技术栈

| 层级 | 技术 |
|---|---|
| LLM | DeepSeek-V3.2 / 通义千问（SiliconFlow API） |
| Embedding | BGE-M3（SiliconFlow API） |
| Agent 框架 | LangChain 0.3 + LangGraph 0.2 |
| 向量数据库 | Chroma 0.5 |
| 关键词检索 | BM25（rank-bm25 + jieba 分词） |
| Reranker | BGE-Reranker-v2-m3（SiliconFlow API） |
| 文档处理 | PyPDF + DocParser 结构化解析 + 句子级分块 |
| 在线检索 | httpx 异步 → arXiv / OpenAlex / DBLP / Crossref / Semantic Scholar |
| Token 计数 | tiktoken (cl100k_base) |
| 前端 | Streamlit 1.40 流式对话 + 工具面板 |
| 配置 | YAML 驱动（7 个配置文件） |

## 快速开始

### 环境要求

- **Python** ≥ 3.10
- **OpenAI 兼容 API**（SiliconFlow / DeepSeek / OpenAI / vLLM 等任一即可）

### 1. 克隆仓库

```bash
git clone https://github.com/mulanxiaodingdang/LangChain-ReAct-Agent.git
cd LangChain-ReAct-Agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 API Key 等信息
```

系统通过 OpenAI 兼容 API 调用 LLM 和 Embedding 模型，支持任意兼容服务商。

| 变量 | 说明 | 默认值 |
|---|---|---|
| `LLM_MODEL` | 对话模型名称 | `deepseek-ai/DeepSeek-V3.2` |
| `LLM_BASE_URL` | LLM API 地址 | `https://api.siliconflow.cn/v1` |
| `LLM_API_KEY` | LLM API 密钥 | — |
| `EMBED_MODEL` | Embedding 模型名称 | `BAAI/bge-m3` |
| `EMBED_BASE_URL` | Embedding API 地址 | `https://api.siliconflow.cn/v1` |
| `EMBED_API_KEY` | Embedding API 密钥 | — |
| `LLM_TIMEOUT` | 调用超时（秒） | `120` |
| `LLM_MAX_RETRIES` | 最大重试次数 | `3` |

LLM 和 Embedding 可分别使用不同的服务商。模型名称需与对应 API 支持的名称一致。

**常见配置示例：**

```bash
# SiliconFlow（默认）
LLM_MODEL=deepseek-ai/DeepSeek-V3.2
LLM_BASE_URL=https://api.siliconflow.cn/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx

# DeepSeek 官方 API
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx

# OpenAI 官方 API
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx

# 本地 vLLM / Ollama
LLM_MODEL=qwen2.5-72b
LLM_BASE_URL=http://localhost:8000/v1
LLM_API_KEY=not-needed
```

向后兼容：未设置上述变量时，系统会自动回退读取 `SILICONFLOW_API_KEY` 环境变量和 `config/rag.yml` 中的模型名。

### 4. 初始化知识库

将论文 PDF 或 TXT 文件放入 `data/` 目录，然后依次执行：

**Step 1 — 入库**：从 `data/` 读取 PDF/TXT，经 DocParser 结构化解析为 section → 按句子边界分块（句子贪心打包，带 overlap）→ MD5 去重后写入 Chroma 向量库。

```bash
python -c "from rag.vector_store import VectorStoreService; VectorStoreService().load_document()"
```

**Step 2 — 建索引**：从 Chroma 向量库读取全部文档，构建 BM25 关键词索引 + 缩写验证索引 + 文档清单（`index_manifest.json`），用于混合检索一致性校验。

```bash
python -c "from rag.rag_service import RagSummarizeService; RagSummarizeService().rebuild_bm25_index()"
```

> 每次新增或替换 `data/` 目录下的论文文件后，都需要重新执行以上两步。缺少 Step 2 会导致混合检索退化为纯向量检索。

### 5. 启动应用

```bash
streamlit run app.py
```

浏览器访问 http://localhost:8501

### 测试示例

| 意图 | 问题示例 |
|---|---|
| QA | "Transformer 模型的核心机制是什么？" |
| QA | "ELSA3D 解决了计算机视觉领域的什么问题？" |
| COMPARE | "BERT 和 GPT 在架构上有哪些主要区别？" |
| COMPARE | "对比 FlippedRAG 和传统 RAG 在安全性上的差异" |
| REVIEW | "LLM 安全领域的攻击与防御研究现状综述" |

## 项目结构

```
LangChain-ReAct-Agent/
│
├── agent/                              # Agent 核心模块
│   ├── react_agent.py                  #   ReAct Agent 主逻辑（三条独立管线 · 流式执行 · 引用渲染 · 会话记忆）
│   ├── intent_router.py                #   意图分类器（高置信正则 → LLM 兜底 → 关键词回退）
│   ├── execution_policy.py             #   执行策略（工具调用配额控制 · 线程安全）
│   ├── execution_context.py            #   Per-request 执行上下文（不可变配置 + 可变状态）
│   ├── retrieval_state.py              #   检索状态机（miss 计数 · 本地 KB 禁用 · 质量信号）
│   ├── memory_manager.py               #   三层记忆（短期缓冲 · 累积摘要 · 长期事实 · Jaccard 过滤）
│   ├── evidence_budgeter.py            #   证据 Token 预算分配器（分层 budget · 引用渲染 · 降级）
│   ├── answer_generator.py             #   答案生成（统一引用编号 · 流式输出 · 引用校验）
│   ├── evidence_judge.py               #   证据判断（LLM chunk 评委 · 逐 subject 评估）
│   ├── query_planner.py                #   查询规划（候选提取 · 查询改写 · 在线 query 构建）
│   │
│   ├── retrieval/                      #   在线检索子系统
│   │   ├── academic_client.py          #     五源学术数据聚合客户端 · SearchIntent · 缓存 · 多级去重
│   │   ├── retrieval_pipeline.py       #     三阶段检索管线（候选 → 消歧 → 改写兜底 · 早停）
│   │   ├── composite_ranker.py         #     组合排序器（身份 + 语义双评分）
│   │   ├── paper_validator.py          #     身份感知验证器（DOI/arXiv/标题/作者/年份多信号 · 四级置信度）
│   │   ├── query_rewrite.py            #     查询改写器（规则 + 同义词扩展）
│   │   ├── retry_policy.py             #     重试策略（指数退避 · Retry-After · 分源配置）
│   │   └── cache_safety.py             #     缓存安全（原子读写 · 过期清理）
│   │
│   └── tools/                          #   Agent 工具
│       ├── agent_tools.py              #     7 工具定义 + 自动索引 + KB 缺失管理
│       └── middleware.py               #     AgentCallback（工具/LLM 调用日志 · 轮次统计）
│
├── rag/                                # RAG 检索增强
│   ├── vector_store.py                 #   Chroma 向量库 · 文档加载 · MD5 去重 · 句子级分块
│   ├── rag_service.py                  #   RAG 检索 → LLM 总结 · 检索质量检测 · 缩写索引
│   ├── bm25_store.py                   #   BM25 关键词索引 · jieba 分词 · 领域术语词典
│   ├── retrieval_strategy.py           #   检索策略（混合检索 · RRF 融合 · Reranker + 元数据融合）
│   ├── topic_analyzer.py               #   领域主题分析
│   ├── paper_metadata.py               #   论文元数据解析
│   └── paper_parser.py                 #   论文结构解析（DocParser）
│
├── model/
│   └── factory.py                      # 模型工厂（ChatOpenAI + OpenAIEmbeddings）
│
├── config/                             # YAML 配置文件
│   ├── rag.yml                         #   对话模型 · Embedding 模型
│   ├── chroma.yml                      #   Chroma 路径 · 分块参数 · Top-K · 章节过滤 · SLM 模型
│   ├── prompts.yml                     #   提示词模板路径
│   ├── agent.yml                       #   Agent 行为配置（检索并行 · 超时 · 重试）
│   ├── reranker.yml                    #   Reranker 模型配置（Score Fusion α / Meta Boost 权重）
│   ├── acronyms.yml                    #   缩写词词典
│   └── domain_terms.yml                #   领域术语词典
│
├── prompts/                            # 提示词模板
│   ├── academic_main.txt               #   默认 QA 意图 System Prompt
│   ├── paper_comparison.txt            #   对比分析 Prompt
│   ├── review.txt                      #   文献综述 Prompt
│   └── rag_summarize.txt               #   RAG 总结 Prompt
│
├── app_pages/                          # Streamlit 页面
│   ├── chat_page.py                    #   对话页面（流式输出 · 工具面板 · 记忆管理 · 引用展示）
│   └── history_page.py                 #   历史记录页面
│
├── utils/                              # 工具函数
│   ├── config_handler.py               #   YAML 配置加载
│   ├── file_handler.py                 #   文件解析（PDF/TXT）
│   ├── logger_handler.py               #   日志管理
│   ├── path_tool.py                    #   路径工具
│   └── prompt_loader.py                #   提示词加载
│
├── evaluation/                         # 评估模块
│   ├── evaluator.py                    #   评估主逻辑
│   ├── ragas_eval.py                   #   RAGAS 评估
│   ├── retrieval_eval.py               #   检索评估
│   ├── test_questions.yml              #   评估问题集
│   └── reports/                        #   评估报告
│
├── data/                               # 数据目录
│   ├── cache/                          #   在线检索缓存（per-source TTL · 基于 SourceQuerySpec 键）
│   ├── kb_missing_papers.json          #   KB 缺失论文索引（自动补全元数据）
│   ├── kb_missing_index.json           #   KB 缺失索引（跳过本地检索标记）
│   ├── short_term_memory.json          #   短期记忆持久化（最近 4 轮）
│   ├── long_term_facts.json            #   长期事实存储（每 3 轮提取）
│   ├── cumulative_summary.json         #   LLM 累积摘要
│   ├── index_manifest.json             #   索引清单（Chroma/BM25/Abbreviation 同步校验）
│   └── abbreviation_index.json         #   已验证缩写缓存
│
├── chroma_db/                          # Chroma 向量库持久化
├── logs/                               # 运行日志
├── app.py                              # Streamlit 应用入口
├── requirements.txt
└── README.md
```

## 系统工作流

### 意图路由 (IntentRouter)

```
用户问题 → IntentRouter.classify()
  ├─ 高置信正则匹配
  │   ├─ 含比较词 + 多主体分隔 → COMPARE（立即返回）
  │   └─ 含综述信号且无假阳性 → REVIEW（立即返回）
  ├─ 双信号冲突或都不命中 → LLM 分类（temperature=0）
  └─ LLM 失败 → 关键词打分回退（默认 QA）
```

### 三条独立处理管线

系统按意图路由到三个完全独立的处理管线，每个管线有各自的检索策略和生成逻辑：

**QA 管线**
```
_extract_candidates() → 提取论文名
  ↓
Round 1: 本地 Chroma + BM25 + Reranker 检索 → _llm_judge_chunks()
  ├─ SUFFICIENT + relevant_chunks 非空 → 构建证据上下文 → 流式生成答案
  └─ INSUFFICIENT / judge_failed →
      Round 2: _llm_rewrite_query() 改写 → 二次本地检索 → 再次 judge
        ├─ SUFFICIENT → 合并两轮 chunk（去重）→ 流式生成
        └─ INSUFFICIENT →
            Round 3: _build_online_query() 构建在线检索 → search_academic_papers_core()
              → 在线 block 并入证据上下文 → 流式生成
  ↓
引用渲染 + 引用校验 → 更新短期记忆
```

**COMPARE 管线**
```
_extract_candidates() → 提取论文名（≤4 篇）
_extract_compare_aspects() → 提取对比维度关键词
  ↓
并行处理（ThreadPoolExecutor, max_workers=3）:
  每 subject 独立执行 _process_compare_subject():
    ├─ 检查 kb_missing_papers 索引（有预存元数据 → 直接使用）
    ├─ KB 缺失索引命中 → 直接走在线
    ├─ Round 1: subject + aspects 本地检索 → _judge_subject_evidence()
    │   ├─ SUFFICIENT → 返回 chunk
    │   ├─ 未命中目标论文 → 在线检索
    │   └─ 命中但证据不足 → Round 2: 改写检索 → 合并 chunk（去重）
    └─ 在线 block 或本地 chunk 返回
  ↓
chunk 均衡分配（_balance_chunks_by_subject: min_per~max_per 条/篇）
  ↓
_llm_judge_chunks() 整体 judge → compare_papers() 辅助结构化对比
  ↓
流式生成答案 → 引用渲染 → 更新记忆
```

**REVIEW 管线**
```
本地 Chroma + BM25 + Reranker 检索 → _llm_judge_chunks()
  ├─ SUFFICIENT → 流式生成答案
  └─ INSUFFICIENT →
      在线学术检索 → _build_review_online_blocks()
        (每篇论文一个 EvidenceBlock, 含标题/作者/年份/摘要/DOI/URL)
        → max_papers=30, 去重, 过滤无摘要论文
  ↓
统一 evidence budget 分配 → 流式生成答案 → 引用渲染 → 更新记忆
```

### 在线检索三阶段管线 (OnlineRetrievalPipeline)

```
SearchIntent(candidate, candidate_type, keyword, fallback_query)
  │
  ├─ Stage 1: candidate 精确搜索（5 源并行）→ 身份验证 → EXACT/HIGH → 早停
  │    各源 SearchIntent → SourceQuerySpec → 缓存优先 → 重试（指数退避）
  ├─ Stage 2: candidate + keyword 消歧搜索（keyword 由 LLM 从 query 提取）
  └─ Stage 3: RuleBasedRewriter 改写变体搜索（最多 3 个变体）
  │
  → 多级去重（DOI → arXiv ID → 归一化标题） + 元数据合并
  → CompositeRanker: 身份分(60%) + 语义分(30%) + 偏置(10%)
  → 四级置信度过滤 → formatted text + scored_results
```

### 身份感知验证（6 层多信号）

```
Tier 1: DOI / arXiv ID 全标识符并行精确匹配 → EXACT
Tier 2: 从 query 提取作者姓氏 + 年份
Tier 3: 标题匹配（acronym 字母验证 · 全文相似度）
Tier 4: 作者 + 年份交叉信号（±1 年容差）
Tier 5: 多信号共识决策（标题 + 作者 + 年份加权）
Tier 6: 分数兜底（match_score 阈值）
```

### 证据 Token 预算分配 (EvidenceBudgeter)

```
allocate(system_prompt, query, local_blocks, online_blocks, ...):
  1. 固定开销：system_prompt + query + 模板（fixed cost）
  2. memory_context：8% 预算，Jaccard 相似度过滤，截断
  3. extra_context：8% 预算，二分截断
  4. 证据选择：
     · 过滤低质量（quality_score < min_quality_score）
     · 本地优先：每 subject 至少 target_min_per_subject 条
     · 在线保障：不低于 target_min_online 条
     · 超预算时移除最后一块（safety degration）
  5. 统一 [N] 编号渲染：
     · 本地 block: [N] 来源：《标题》；章节：xxx；页码：pp.xx-xx；内容：...
     · 在线 block: [N] [在线]《标题》| 作者：xxx | 年份：xxx | DOI：xxx | URL：xxx | 摘要
  6. 完整 Prompt 校验（总 token ≤ input_budget）
```

### 记忆系统

```
ShortTermMemory: 最近 4 轮对话缓冲（JSON 持久化）
  ↓ 超过 4 轮 → 触发压缩
CumulativeSummary: LLM 压缩为累积摘要（中文，≤200 字）
  ↓ 每 3 轮
FactStore: LLM 提取长期事实（研究偏好、方法名、实验数据）
  ↓ 回答时
_memory_context(): Jaccard 相似度过滤 → "相关历史对话" + "相关已知事实"
  → 注入到 EvidenceBudgeter 的 memory 预算池
```

## 配置说明

首次运行只需设置 API Key 环境变量，并将论文文档放入 `data/` 目录。

| 配置文件 | 说明 |
|---|---|
| `config/rag.yml` | LLM 模型名称、Embedding 模型名称、缩写词映射 |
| `config/chroma.yml` | Chroma 持久化路径、分块策略（句子级）、chunk 大小、检索 Top-K、RRF k 值、章节过滤模式、Reranker 模型 |
| `config/prompts.yml` | 各意图对应的 Prompt 模板路径 |
| `config/agent.yml` | Agent 行为配置（检索并行开关/workers、LLM 超时/最大重试） |
| `config/reranker.yml` | Reranker 模型与参数（Score Fusion α、Meta Boost 权重） |
| `config/acronyms.yml` | 论文缩写词映射词典（ELSA → Efficient Label-consistent Subsampled Atlas 等） |
| `config/domain_terms.yml` | 领域术语扩展词典（确保 jieba/BGE 正确切分专业术语） |

## 数据持久化

| 文件 | 说明 |
|---|---|
| `data/kb_missing_papers.json` | KB 缺失论文索引，在线检索命中后自动写入元数据（标题/作者/摘要/DOI 等），含 `auto_indexed` 状态标记 |
| `data/kb_missing_index.json` | KB 缺失标题索引，标记后 `mark_paper_not_in_kb` 工具和 COMPARE 管线自动跳过本地检索 |
| `data/short_term_memory.json` | 短期对话记忆（最近 4 轮，8 条消息），每次对话后自动更新 |
| `data/cumulative_summary.json` | LLM 生成的累积对话摘要（中文 ≤200 字，合并关键论文名/方法名/发现） |
| `data/long_term_facts.json` | 长期事实提取（每 3 轮触发），按 category 分类存储研究进展 |
| `data/cache/*.json` | 在线检索缓存，按 `source|mode|method|endpoint|params` 生成 MD5 键，分源 TTL（arxiv/dblp: 24h, crossref/openalex/semantic_scholar: 1h） |
| `data/index_manifest.json` | 索引一致性清单（Chroma doc 数 / BM25 doc 数 / 缩写数），用于运行时同步检测 |
| `data/abbreviation_index.json` | 已验证缩写缓存（缩写→全称，仅保留语料中出现的全称） |
| `chroma_db/` | Chroma 向量库持久化目录 |
| `logs/agent_YYYYMMDD.log` | 按日切割的运行日志 |

## 检索质量四信号

每次本地检索后自动检测质量（`_check_retrieval_quality()`），任一 ≥2 个信号触发记为 "soft miss"：

| 信号 | 检测条件 | 默认阈值 |
|---|---|---|
| S1: Reranker 分过低 | `max_score < min_score` | 0.35 |
| S2: 论文名不匹配 | query 中论文名不在 chunk 标题中 | — |
| S3: 关键词覆盖率低 | jieba 分词后覆盖率 | 0.30 |
| S4: 领域相似度低 | embedding 余弦相似度 | 0.45 |

## 运行测试

```bash
# 单元测试
python -m pytest tests/ -v

# 评估
python -m evaluation
```


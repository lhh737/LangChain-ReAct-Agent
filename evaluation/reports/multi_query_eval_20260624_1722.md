# Multi-Query 结构化检索评估报告

**生成时间**: 2026-06-24 17:22  
**数据集**: `rag_eval_20.jsonl` (16 answerable questions)  
**策略**: raw vs rewrite vs translate vs mq_zscore vs mq_rawmax vs mq_rrf  
**Multi-Query 配额**: per-entity BM25=15, Vector=5, min=3, total=50  
**k 值**: [5, 10, 20]  

---

# 1. Multi-Query 结构化计划

## cross_001_en (comparison, EN)

**原问题**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are t  
**类型**: comparison | **实体**: ['PoisonedRAG', 'Machine Against the RAG']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | PoisonedRAG | PoisonedRAG attack method on RAG systems threat model |
| 2 | Machine Against the RAG | Machine Against the RAG attack RAG threat model differences |

## cross_002_en (comparison, EN)

**原问题**: Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect D  
**类型**: comparison | **实体**: ['FlatD', 'MACO', 'Hardening DNN Binaries']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | FlatD | FlatD approach to protect DNN models from reverse engineering |
| 2 | MACO | MACO method for protecting DNN models against reverse engineering |
| 3 | Hardening DNN Binaries | Hardening DNN Binaries technique to prevent reverse engineering of DNNs |

## single_001_en (method, EN)

**原问题**: How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its  
**类型**: single | **实体**: ['AgentSentinel']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | AgentSentinel | AgentSentinel end-to-end security defense for LLM agents |
| 2 | AgentSentinel | AgentSentinel real-time security defense mechanism |
| 3 | AgentSentinel | AgentSentinel core architecture design |

## single_002_en (method, EN)

**原问题**: What is Appatch's automated adaptive prompting approach? How does it improve program repair or code   
**类型**: single | **实体**: ['Appatch']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | Appatch | Appatch automated adaptive prompting approach architecture |
| 2 | Appatch | Appatch improves program repair via adaptive prompting |
| 3 | Appatch | Appatch improves code generation using adaptive prompting |

## single_003_en (method, EN)

**原问题**: How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for impro  
**类型**: single | **实体**: ['CodeLLM-Devkit']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | CodeLLM-Devkit | CodeLLM-Devkit contextualization approach for code LLMs |
| 2 | CodeLLM-Devkit | CodeLLM-Devkit framework components for code intelligence |
| 3 | CodeLLM-Devkit | CodeLLM-Devkit evaluation on code intelligence tasks |

## single_004_en (method, EN)

**原问题**: How does BTD recover DNN model specifications from compiled x86 executables? What techniques does it  
**类型**: single | **实体**: ['BTD']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | BTD | BTD architecture for recovering DNN model specifications from x86 executables |
| 2 | BTD | BTD techniques used to extract DNN model specifications from compiled binaries |
| 3 | BTD | BTD key evaluation results on DNN model recovery from x86 executables |

## single_005_en (fact, EN)

**原问题**: What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, accordi  
**类型**: single | **实体**: ['Pitfalls survey']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | Pitfalls survey | Pitfalls survey taxonomy of pitfalls for LLMs in code intelligence |
| 2 | Pitfalls survey | Pitfalls survey main categories of pitfalls when using LLMs for code |
| 3 | Pitfalls survey | Pitfalls survey classification of pitfalls in code intelligence with LLMs |

## single_006_en (method, EN)

**原问题**: How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what   
**类型**: single | **实体**: ['FlippedRAG']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | FlippedRAG | FlippedRAG black-box opinion manipulation attack methodology |
| 2 | FlippedRAG | FlippedRAG attack access requirements and assumptions |
| 3 | FlippedRAG | FlippedRAG retrieval manipulation mechanism for opinion change |

## cross_001_zh (comparison, ZH)

**原问题**: 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？  
**类型**: comparison | **实体**: ['PoisonedRAG', 'Machine Against the RAG']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | PoisonedRAG | PoisonedRAG attack method on RAG systems threat model details |
| 2 | Machine Against the RAG | Machine Against the RAG attack method on RAG systems threat model details |

## cross_002_zh (comparison, ZH)

**原问题**: 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？  
**类型**: comparison | **实体**: ['FlatD', 'MACO', 'Hardening DNN Binaries']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | FlatD | FlatD method for protecting DNN models from reverse engineering attacks |
| 2 | MACO | MACO approach to defend DNN models against reverse engineering |
| 3 | Hardening DNN Binaries | Hardening DNN Binaries technique for protecting DNN models from reverse engineering |

## single_001_zh (method, ZH)

**原问题**: AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？  
**类型**: single | **实体**: ['AgentSentinel']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | AgentSentinel | AgentSentinel architecture for end-to-end real-time security defense in LLM agents |
| 2 | AgentSentinel | AgentSentinel core components and mechanisms for real-time defense |
| 3 | AgentSentinel | AgentSentinel evaluation results and performance in real-time security |

## single_002_zh (method, ZH)

**原问题**: Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？  
**类型**: single | **实体**: ['Appatch']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | Appatch | Appatch automatic adaptive prompting method architecture and details |
| 2 | Appatch | Appatch improvement on program repair performance evaluation |
| 3 | Appatch | Appatch enhancement for code generation tasks mechanism |

## single_003_zh (method, ZH)

**原问题**: CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？  
**类型**: single | **实体**: ['CodeLLM-Devkit']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | CodeLLM-Devkit | CodeLLM-Devkit context provision mechanism for code LLM |
| 2 | CodeLLM-Devkit | CodeLLM-Devkit framework components for code intelligence tasks |
| 3 | CodeLLM-Devkit | CodeLLM-Devkit architecture and design for code LLM support |

## single_004_zh (method, ZH)

**原问题**: BTD 如何从编译后的 x86 可执行文件中恢复 DNN 模型规格？它使用了哪些技术，关键评估结果是什么？  
**类型**: single | **实体**: ['BTD']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | BTD | BTD method for recovering DNN model specifications from compiled x86 binaries |
| 2 | BTD | Techniques used in BTD for DNN model extraction from x86 executables |
| 3 | BTD | Key evaluation results of BTD on DNN model recovery from x86 binaries |

## single_005_zh (fact, ZH)

**原问题**: 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？  
**类型**: single | **实体**: ['Pitfalls']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | Pitfalls | Pitfalls taxonomy of pitfalls in code intelligence using LLMs |
| 2 | Pitfalls | Pitfalls classification system for LLM-based code intelligence |
| 3 | Pitfalls | Pitfalls survey main categories of pitfalls in code intelligence with LLMs |

## single_006_zh (method, ZH)

**原问题**: FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？  
**类型**: single | **实体**: ['FlippedRAG']

| # | Entity | Sub-query |
|---|--------|----------|
| 1 | FlippedRAG | FlippedRAG black-box opinion manipulation attack method |
| 2 | FlippedRAG | FlippedRAG attack architecture and mechanism |
| 3 | FlippedRAG | FlippedRAG required access permissions for attack |

---

# 2. 逐题指标对比（raw vs rewrite vs translate vs mq_zscore vs mq_rawmax vs mq_rrf）

## cross_001_en (comparison, EN)

**Raw**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are the key differences i  
**Rewritten**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are the key differences i  
**Translated**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are the key differences i  
**Multi-Query**: PoisonedRAG attack method on RAG systems threat model | Machine Against the RAG attack RAG threat model differences

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.6000 | 0.6000 | 0.6000 | 0.4000 | 0.4000 | 0.4000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 0.4000 | 0.4000 | 0.4000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 0.4000 | 0.4000 | 0.4000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.6000 | 0.6000 | 0.6000 | 0.6000 | 0.6000 | 0.6000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 0.6000 | 0.6000 | 0.6000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 0.6000 | 0.6000 | 0.6000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 0.5000 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## cross_002_en (comparison, EN)

**Raw**: Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect DNN models from rever  
**Rewritten**: Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect DNN models from rever  
**Translated**: Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect DNN models from rever  
**Multi-Query**: FlatD approach to protect DNN models from reverse engineerin | MACO method for protecting DNN models against reverse engine | Hardening DNN Binaries technique to prevent reverse engineer

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.5000 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.5000 |
| 10 | 0.5000 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.5000 |
| 20 | 0.7500 | 0.7500 | 0.7500 | 1.0000 | 0.7500 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.5000 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.5000 |
| 10 | 0.5000 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.5000 |
| 20 | 0.7500 | 0.7500 | 0.7500 | 1.0000 | 0.7500 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.6667 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.3333 | 0.3333 |
| 10 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.6667 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.6667 | 0.3333 |
| 20 | 0.6667 | 0.6667 | 0.6667 | 1.0000 | 0.6667 | 1.0000 | 0.6667 | 0.6667 | 0.6667 | 0.6667 | 0.6667 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_001_en (method, EN)

**Raw**: How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its core architecture?  
**Rewritten**: How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its core architecture?  
**Translated**: How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its core architecture?  
**Multi-Query**: AgentSentinel end-to-end security defense for LLM agents | AgentSentinel real-time security defense mechanism | AgentSentinel core architecture design

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.7500 | 0.7500 | 0.7500 | 0.7500 | 0.7500 | 0.5000 |
| 10 | 0.7500 | 0.7500 | 0.7500 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.7500 | 0.7500 | 0.7500 | 1.0000 | 0.7500 | 0.5000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_002_en (method, EN)

**Raw**: What is Appatch's automated adaptive prompting approach? How does it improve program repair or code generation?  
**Rewritten**: What is Appatch's automated adaptive prompting approach? How does it improve program repair or code generation?  
**Translated**: What is Appatch's automated adaptive prompting approach? How does it improve program repair or code generation?  
**Multi-Query**: Appatch automated adaptive prompting approach architecture | Appatch improves program repair via adaptive prompting | Appatch improves code generation using adaptive prompting

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.2500 | 0.2500 | 0.2500 | 0.5000 | 0.5000 | 0.2500 |
| 10 | 0.7500 | 0.7500 | 0.7500 | 0.5000 | 0.5000 | 0.7500 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 0.7500 | 0.7500 | 0.7500 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.2500 | 0.2500 | 0.2500 | 0.5000 | 0.5000 | 0.5000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 0.7500 | 0.7500 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_003_en (method, EN)

**Raw**: How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for improving code intelligen  
**Rewritten**: How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for improving code intelligen  
**Translated**: How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for improving code intelligen  
**Multi-Query**: CodeLLM-Devkit contextualization approach for code LLMs | CodeLLM-Devkit framework components for code intelligence | CodeLLM-Devkit evaluation on code intelligence tasks

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_004_en (method, EN)

**Raw**: How does BTD recover DNN model specifications from compiled x86 executables? What techniques does it use and what are th  
**Rewritten**: How does BTD recover DNN model specifications from compiled x86 executables? What techniques does it use and what are th  
**Translated**: How does BTD recover DNN model specifications from compiled x86 executables? What techniques does it use and what are th  
**Multi-Query**: BTD architecture for recovering DNN model specifications fro | BTD techniques used to extract DNN model specifications from | BTD key evaluation results on DNN model recovery from x86 ex

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.5000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 0.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_005_en (fact, EN)

**Raw**: What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, according to the Pitfalls s  
**Rewritten**: What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, according to the Pitfalls s  
**Translated**: What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, according to the Pitfalls s  
**Multi-Query**: Pitfalls survey taxonomy of pitfalls for LLMs in code intell | Pitfalls survey main categories of pitfalls when using LLMs  | Pitfalls survey classification of pitfalls in code intellige

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_006_en (method, EN)

**Raw**: How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what access does it requi  
**Rewritten**: How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what access does it requi  
**Translated**: How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what access does it requi  
**Multi-Query**: FlippedRAG black-box opinion manipulation attack methodology | FlippedRAG attack access requirements and assumptions | FlippedRAG retrieval manipulation mechanism for opinion chan

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.3333 | 0.3333 | 0.3333 | 0.0000 | 0.0000 | 0.6667 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.6667 | 0.6667 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.3333 | 0.3333 | 0.3333 | 0.0000 | 0.0000 | 0.6667 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.6667 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## cross_001_zh (comparison, ZH)

**Raw**: 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？  
**Rewritten**: 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？  
**Translated**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack the RAG system? What are the key differences in  
**Multi-Query**: PoisonedRAG attack method on RAG systems threat model detail | Machine Against the RAG attack method on RAG systems threat 

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.4000 | 0.4000 | 0.8000 | 0.2000 | 0.2000 | 0.4000 |
| 10 | 0.4000 | 0.4000 | 1.0000 | 0.4000 | 0.4000 | 0.4000 |
| 20 | 0.4000 | 0.4000 | 1.0000 | 0.4000 | 0.4000 | 0.4000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.4000 | 0.4000 | 1.0000 | 0.6000 | 0.4000 | 0.6000 |
| 10 | 0.8000 | 0.8000 | 1.0000 | 0.8000 | 0.8000 | 0.6000 |
| 20 | 0.8000 | 0.8000 | 1.0000 | 0.8000 | 0.8000 | 0.8000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## cross_002_zh (comparison, ZH)

**Raw**: 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？  
**Rewritten**: 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？  
**Translated**: Compare FlatD, MACO, and Hardening DNN Binaries: what methods do they each use to protect DNN models from reverse engine  
**Multi-Query**: FlatD method for protecting DNN models from reverse engineer | MACO approach to defend DNN models against reverse engineeri | Hardening DNN Binaries technique for protecting DNN models f

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.2500 | 0.2500 | 0.5000 | 0.7500 | 0.7500 | 0.2500 |
| 10 | 0.5000 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.5000 |
| 20 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.2500 | 0.2500 | 0.5000 | 0.7500 | 0.7500 | 0.2500 |
| 10 | 0.5000 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.5000 |
| 20 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.6667 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 |
| 10 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.6667 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 |
| 20 | 0.6667 | 0.6667 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.3333 | 0.3333 | 0.6667 | 1.0000 | 0.6667 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_001_zh (method, ZH)

**Raw**: AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？  
**Rewritten**: AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？  
**Translated**: How does AgentSentinel provide end-to-end real-time security defense for LLM agents? What is its core architecture?  
**Multi-Query**: AgentSentinel architecture for end-to-end real-time security | AgentSentinel core components and mechanisms for real-time d | AgentSentinel evaluation results and performance in real-tim

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.2500 | 0.2500 | 0.7500 | 0.5000 | 0.2500 | 0.5000 |
| 10 | 0.5000 | 0.5000 | 0.7500 | 0.7500 | 0.7500 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.2500 | 0.2500 | 0.7500 | 0.5000 | 0.2500 | 0.5000 |
| 10 | 0.7500 | 0.7500 | 1.0000 | 1.0000 | 0.7500 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_002_zh (method, ZH)

**Raw**: Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？  
**Rewritten**: Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？  
**Translated**: What is the automatic adaptive prompting method of Appatch? How does it improve program repair or code generation?  
**Multi-Query**: Appatch automatic adaptive prompting method architecture and | Appatch improvement on program repair performance evaluation | Appatch enhancement for code generation tasks mechanism

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.2500 | 0.2500 | 0.2500 | 0.2500 | 0.2500 | 0.0000 |
| 10 | 0.2500 | 0.2500 | 0.5000 | 0.2500 | 0.5000 | 0.2500 |
| 20 | 0.2500 | 0.2500 | 1.0000 | 0.7500 | 0.7500 | 0.7500 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.2500 | 0.2500 | 0.7500 | 0.5000 | 0.7500 | 0.5000 |
| 10 | 0.7500 | 0.7500 | 0.7500 | 0.7500 | 0.7500 | 0.7500 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_003_zh (method, ZH)

**Raw**: CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？  
**Rewritten**: CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？  
**Translated**: How does CodeLLM-Devkit provide context for code LLMs? What framework components does it provide for improving code inte  
**Multi-Query**: CodeLLM-Devkit context provision mechanism for code LLM | CodeLLM-Devkit framework components for code intelligence ta | CodeLLM-Devkit architecture and design for code LLM support

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_004_zh (method, ZH)

**Raw**: BTD 如何从编译后的 x86 可执行文件中恢复 DNN 模型规格？它使用了哪些技术，关键评估结果是什么？  
**Rewritten**: BTD 如何从编译后的 x86 可执行文件中恢复 DNN 模型规格？它使用了哪些技术，关键评估结果是什么？  
**Translated**: How to recover DNN model specifications from compiled x86 executable files? What techniques does it use, and what are th  
**Multi-Query**: BTD method for recovering DNN model specifications from comp | Techniques used in BTD for DNN model extraction from x86 exe | Key evaluation results of BTD on DNN model recovery from x86

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 1.0000 | 1.0000 | 0.5000 | 0.0000 | 0.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 1.0000 | 1.0000 | 0.5000 | 0.5000 | 0.5000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_005_zh (fact, ZH)

**Raw**: 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？  
**Rewritten**: 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？  
**Translated**: According to the Pitfalls survey, what are the main pitfall categories and classification system when using LLM for code  
**Multi-Query**: Pitfalls taxonomy of pitfalls in code intelligence using LLM | Pitfalls classification system for LLM-based code intelligen | Pitfalls survey main categories of pitfalls in code intellig

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

## single_006_zh (method, ZH)

**Raw**: FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？  
**Rewritten**: FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？  
**Translated**: FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？  
**Multi-Query**: FlippedRAG black-box opinion manipulation attack method | FlippedRAG attack architecture and mechanism | FlippedRAG required access permissions for attack

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.3333 | 0.6667 |
| 10 | 0.6667 | 0.6667 | 0.6667 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 0.6667 | 0.6667 | 0.6667 | 1.0000 | 1.0000 | 1.0000 |

| k | raw window | rw window | tr window | mq_zscore window | mq_rawmax window | mq_rrf window |
|---|-----------|----------|----------|-----------------|-----------------|---------------|
| 5 | 0.3333 | 0.3333 | 0.3333 | 0.6667 | 0.3333 | 1.0000 |
| 10 | 0.6667 | 0.6667 | 0.6667 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

| k | raw source | rw source | tr source | mq_zscore source | mq_rawmax source | mq_rrf source | raw evid | rw evid | tr evid | mq_zscore evid | mq_rawmax evid | mq_rrf evid |
|---|-----------|----------|----------|-----------------|-----------------|---------------|---------|--------|--------|---------------|---------------|-------------|
| 5 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

**Entity Coverage**: raw=1.00 | rw=1.00 | tr=1.00 | mq_zscore=1.00 | mq_rawmax=1.00 | mq_rrf=1.00

---

# 3. 全局平均指标对比

## Raw Query

| k | strict_chunk | window_chunk | source | evidence |
|---|-------------|-------------|--------|----------|
| 5 | 0.4948 | 0.4948 | 0.8854 | 0.8854 |
| 10 | 0.7073 | 0.8729 | 0.9167 | 0.9167 |
| 20 | 0.8479 | 0.9406 | 0.9583 | 0.9375 |

## Query Rewrite

| k | strict_chunk | window_chunk | source | evidence |
|---|-------------|-------------|--------|----------|
| 5 | 0.4948 | 0.4948 | 0.8854 | 0.8854 |
| 10 | 0.7073 | 0.8729 | 0.9167 | 0.9167 |
| 20 | 0.8479 | 0.9406 | 0.9583 | 0.9375 |

## ZH→EN Translate + HybridScorer

| k | strict_chunk | window_chunk | source | evidence |
|---|-------------|-------------|--------|----------|
| 5 | 0.5979 | 0.6417 | 0.8854 | 0.8854 |
| 10 | 0.8385 | 0.9010 | 0.9167 | 0.9167 |
| 20 | 0.9635 | 0.9844 | 0.9792 | 0.9583 |

## MQ Z-Score Max-Fusion

| k | strict_chunk | window_chunk | source | evidence |
|---|-------------|-------------|--------|----------|
| 5 | 0.5271 | 0.6479 | 0.9583 | 0.8750 |
| 10 | 0.7479 | 0.8792 | 0.9583 | 0.9375 |
| 20 | 0.8938 | 0.9625 | 1.0000 | 0.9792 |

## MQ Raw Max-Fusion (方案A)

| k | strict_chunk | window_chunk | source | evidence |
|---|-------------|-------------|--------|----------|
| 5 | 0.5115 | 0.5990 | 0.9271 | 0.8229 |
| 10 | 0.7323 | 0.8323 | 0.9583 | 0.9375 |
| 20 | 0.8573 | 0.9469 | 0.9792 | 0.9583 |

## MQ RRF Fusion (方案B)

| k | strict_chunk | window_chunk | source | evidence |
|---|-------------|-------------|--------|----------|
| 5 | 0.6021 | 0.7260 | 0.9167 | 0.9167 |
| 10 | 0.7792 | 0.8719 | 0.9167 | 0.9167 |
| 20 | 0.8938 | 0.9625 | 1.0000 | 1.0000 |

## Raw → Rewrite → Translate → MQ Variants 变化（strict_chunk）


### 绝对值

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.4948 | 0.4948 | 0.5979 | 0.5271 | 0.5115 | 0.6021 |
| 10 | 0.7073 | 0.7073 | 0.8385 | 0.7479 | 0.7323 | 0.7792 |
| 20 | 0.8479 | 0.8479 | 0.9635 | 0.8938 | 0.8573 | 0.8938 |

### Delta vs Raw raw→rw

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf | raw→rw | raw→tr | raw→zscore | raw→rawmax | raw→rrf |
|---|-----|----|----|----------|----------|--------|--------|--------|-----------|-----------|---------|
| 5 | 0.4948 | 0.4948 | 0.5979 | 0.5271 | 0.5115 | 0.6021 | +0.0000 | +0.1031 | +0.0323 | +0.0167 | +0.1073 |
| 10 | 0.7073 | 0.7073 | 0.8385 | 0.7479 | 0.7323 | 0.7792 | +0.0000 | +0.1312 | +0.0406 | +0.0250 | +0.0719 |
| 20 | 0.8479 | 0.8479 | 0.9635 | 0.8938 | 0.8573 | 0.8938 | +0.0000 | +0.1156 | +0.0458 | +0.0094 | +0.0458 |

### Delta vs Raw raw→tr

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf | raw→rw | raw→tr | raw→zscore | raw→rawmax | raw→rrf |
|---|-----|----|----|----------|----------|--------|--------|--------|-----------|-----------|---------|
| 5 | 0.4948 | 0.4948 | 0.5979 | 0.5271 | 0.5115 | 0.6021 | +0.0000 | +0.1031 | +0.0323 | +0.0167 | +0.1073 |
| 10 | 0.7073 | 0.7073 | 0.8385 | 0.7479 | 0.7323 | 0.7792 | +0.0000 | +0.1312 | +0.0406 | +0.0250 | +0.0719 |
| 20 | 0.8479 | 0.8479 | 0.9635 | 0.8938 | 0.8573 | 0.8938 | +0.0000 | +0.1156 | +0.0458 | +0.0094 | +0.0458 |

### Delta vs Raw raw→zscore

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf | raw→rw | raw→tr | raw→zscore | raw→rawmax | raw→rrf |
|---|-----|----|----|----------|----------|--------|--------|--------|-----------|-----------|---------|
| 5 | 0.4948 | 0.4948 | 0.5979 | 0.5271 | 0.5115 | 0.6021 | +0.0000 | +0.1031 | +0.0323 | +0.0167 | +0.1073 |
| 10 | 0.7073 | 0.7073 | 0.8385 | 0.7479 | 0.7323 | 0.7792 | +0.0000 | +0.1312 | +0.0406 | +0.0250 | +0.0719 |
| 20 | 0.8479 | 0.8479 | 0.9635 | 0.8938 | 0.8573 | 0.8938 | +0.0000 | +0.1156 | +0.0458 | +0.0094 | +0.0458 |

### Delta vs Raw raw→rawmax

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf | raw→rw | raw→tr | raw→zscore | raw→rawmax | raw→rrf |
|---|-----|----|----|----------|----------|--------|--------|--------|-----------|-----------|---------|
| 5 | 0.4948 | 0.4948 | 0.5979 | 0.5271 | 0.5115 | 0.6021 | +0.0000 | +0.1031 | +0.0323 | +0.0167 | +0.1073 |
| 10 | 0.7073 | 0.7073 | 0.8385 | 0.7479 | 0.7323 | 0.7792 | +0.0000 | +0.1312 | +0.0406 | +0.0250 | +0.0719 |
| 20 | 0.8479 | 0.8479 | 0.9635 | 0.8938 | 0.8573 | 0.8938 | +0.0000 | +0.1156 | +0.0458 | +0.0094 | +0.0458 |

### Delta vs Raw raw→rrf

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf | raw→rw | raw→tr | raw→zscore | raw→rawmax | raw→rrf |
|---|-----|----|----|----------|----------|--------|--------|--------|-----------|-----------|---------|
| 5 | 0.4948 | 0.4948 | 0.5979 | 0.5271 | 0.5115 | 0.6021 | +0.0000 | +0.1031 | +0.0323 | +0.0167 | +0.1073 |
| 10 | 0.7073 | 0.7073 | 0.8385 | 0.7479 | 0.7323 | 0.7792 | +0.0000 | +0.1312 | +0.0406 | +0.0250 | +0.0719 |
| 20 | 0.8479 | 0.8479 | 0.9635 | 0.8938 | 0.8573 | 0.8938 | +0.0000 | +0.1156 | +0.0458 | +0.0094 | +0.0458 |

---

# 4. 按问题类型汇总（strict_chunk）

## comparison (4 questions)

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.4375 | 0.4375 | 0.5250 | 0.5250 | 0.3875 |
| 10 | 0.6000 | 0.6000 | 0.5750 | 0.5750 | 0.4500 |
| 20 | 0.6625 | 0.6625 | 0.7000 | 0.6375 | 0.7000 |

## fact (2 questions)

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 0.5000 | 0.5000 | 1.0000 | 1.0000 | 1.0000 |
| 20 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

## method (10 questions)

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.5167 | 0.5167 | 0.4333 | 0.4083 | 0.6083 |
| 10 | 0.7917 | 0.7917 | 0.7667 | 0.7417 | 0.8667 |
| 20 | 0.8917 | 0.8917 | 0.9500 | 0.9167 | 0.9500 |

---

# 5. 按语言汇总（strict_chunk）

## EN (8 questions)

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.5542 | 0.5542 | 0.5500 | 0.5500 | 0.6021 |
| 10 | 0.8750 | 0.8750 | 0.7271 | 0.6646 | 0.7896 |
| 20 | 0.9688 | 0.9688 | 0.8938 | 0.8208 | 0.8938 |

## ZH (8 questions)

| k | raw | rw | tr | mq_zscore | mq_rawmax | mq_rrf |
|---|-----|----|----|----------|----------|--------|
| 5 | 0.4354 | 0.4354 | 0.5042 | 0.4729 | 0.6021 |
| 10 | 0.5396 | 0.5396 | 0.7688 | 0.8000 | 0.7688 |
| 20 | 0.7271 | 0.7271 | 0.8938 | 0.8938 | 0.8938 |


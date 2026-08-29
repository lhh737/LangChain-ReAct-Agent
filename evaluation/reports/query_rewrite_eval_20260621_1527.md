# Query Rewrite 消融评估报告

**生成时间**: 2026-06-21 15:27  
**数据集**: `rag_eval_20.jsonl` (16 answerable questions)  
**评估策略**: ['vector_only', 'hybrid_no_rerank', 'hybrid_rerank', 'hybrid_score']  
**k 值**: [5, 10, 20]  
**缓存文件**: `query_rewrite_cache.json`

---

# 1. 改写前后 Query 对照

| ID | Lang | Raw Query | Rewritten Query |
|----|------|-----------|-----------------|
| cross_001_en | EN | Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG sys | PoisonedRAG Machine Against the Retrieval-Augmented Generation attack methods th |
| cross_002_en | EN | Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do th | Compare FlatD, MACO, and Hardening Deep Neural Network Binaries: different appro |
| single_001_en | EN | How does AgentSentinel provide end-to-end and real-time security defense for LLM | AgentSentinel end-to-end real-time security defense Large Language Model agents  |
| single_002_en | EN | What is Appatch's automated adaptive prompting approach? How does it improve pro | Appatch automated adaptive prompting approach program repair code generation imp |
| single_003_en | EN | How does CodeLLM-Devkit contextualize code LLMs? What framework components does  | Code Large Language Model Development Kit context integration code large languag |
| single_004_en | EN | What method does 'LLMs: Understanding Code Syntax and Semantics' propose for usi | Large Language Models code comprehension method syntax semantics paper Understan |
| single_005_en | EN | What are the main categories and taxonomy of pitfalls when using LLMs for code i | pitfalls taxonomy categories Large Language Model code intelligence survey error |
| single_006_en | EN | How does FlippedRAG achieve black-box opinion manipulation? What is its attack m | FlippedRAG black-box opinion manipulation attack methodology access requirements |
| cross_001_zh | ZH | 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？ | 检索增强生成系统 攻击方法 比较 PoisonedRAG Machine Against the RAG 威胁模型 区别 对抗攻击 数据投毒 检索污染 安全漏洞 |
| cross_002_zh | ZH | 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？ | 比较 FlatD、MACO 和 Hardening DNN Binaries 三种方法保护深度神经网络模型免受逆向工程攻击的技术手段 深度神经网络模型保护 逆向 |
| single_001_zh | ZH | AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？ | AgentSentinel 如何为大语言模型代理提供端到端的实时安全防御？其核心架构是什么？安全监控 威胁检测 防护机制 |
| single_002_zh | ZH | Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？ | Appatch 自动自适应提示方法 程序修复 代码生成 补丁生成 提示工程 大语言模型 动态提示优化 |
| single_003_zh | ZH | CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？ | 代码大语言模型开发工具包 如何为代码大语言模型提供上下文 代码智能任务改进 框架组件 上下文管理 代码表示学习 代码生成与理解 |
| single_004_zh | ZH | 《LLMs: Understanding Code Syntax and Semantics》提出了什么方法来利用 LLM 进行代码理解？ | 大语言模型 代码语法和语义理解 方法 代码表示学习 程序分析 利用大语言模型进行代码理解 |
| single_005_zh | ZH | 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？ | 根据陷阱综述，使用大语言模型进行代码智能时的主要陷阱类别和分类体系是什么 代码生成 代码理解 错误类型 挑战 局限性 |
| single_006_zh | ZH | FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？ | FlippedRAG 检索增强生成 黑盒观点操纵 攻击方法 访问权限 对抗攻击 文本操纵 模型安全性 |

---

# 2. 逐题指标对比（策略：hybrid_score）

## cross_001_en (comparison, EN)

**Raw**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are the key differences i  
**Rewritten**: PoisonedRAG Machine Against the Retrieval-Augmented Generation attack methods threat models comparison adversarial attac

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1000 | 0.1000 | +0.0000 | 0.2000 | 0.1000 | -0.1000 | 1.0000 | 0.5000 | -0.5000 | 0.5000 | 0.5000 | +0.0000 |
| 10 | 0.2000 | 0.1000 | -0.1000 | 0.3000 | 0.1000 | -0.2000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 0.5000 | -0.5000 |
| 20 | 0.4000 | 0.2000 | -0.2000 | 0.7000 | 0.2000 | -0.5000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 0.5000 | -0.5000 |

## cross_002_en (comparison, EN)

**Raw**: Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect DNN models from rever  
**Rewritten**: Compare FlatD, MACO, and Hardening Deep Neural Network Binaries: different approaches for protecting Deep Neural Network

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.2000 | 0.0000 | -0.2000 | 0.2000 | 0.0000 | -0.2000 | 0.3333 | 0.6667 | +0.3333 | 0.3333 | 0.0000 | -0.3333 |
| 10 | 0.2000 | 0.0000 | -0.2000 | 0.2000 | 0.1000 | -0.1000 | 0.3333 | 0.6667 | +0.3333 | 0.3333 | 0.3333 | +0.0000 |
| 20 | 0.2000 | 0.2000 | +0.0000 | 0.3000 | 0.4000 | +0.1000 | 0.6667 | 1.0000 | +0.3333 | 0.6667 | 0.6667 | +0.0000 |

## single_001_en (method, EN)

**Raw**: How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its core architecture?  
**Rewritten**: AgentSentinel end-to-end real-time security defense Large Language Model agents core architecture system design threat m

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.5000 | 0.3333 | -0.1667 | 0.6667 | 0.5000 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.6667 | 0.6667 | +0.0000 | 0.8333 | 1.0000 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_002_en (method, EN)

**Raw**: What is Appatch's automated adaptive prompting approach? How does it improve program repair or code generation?  
**Rewritten**: Appatch automated adaptive prompting approach program repair code generation improvement technique dynamic prompt adjust

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.6667 | 0.5000 | -0.1667 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.6667 | 0.6667 | +0.0000 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 1.0000 | 0.8333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_003_en (method, EN)

**Raw**: How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for improving code intelligen  
**Rewritten**: Code Large Language Model Development Kit context integration code large language models framework components architectu

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.1667 | +0.0000 | 0.3333 | 0.3333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.3333 | 0.3333 | +0.0000 | 0.5000 | 0.3333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.3333 | -0.1667 | 0.5000 | 0.3333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_004_en (method, EN)

**Raw**: What method does 'LLMs: Understanding Code Syntax and Semantics' propose for using LLMs in code comprehension?  
**Rewritten**: Large Language Models code comprehension method syntax semantics paper Understanding Code Syntax and Semantics program u

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.5000 | 0.3333 | -0.1667 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.6667 | 0.6667 | +0.0000 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.8333 | 1.0000 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_005_en (fact, EN)

**Raw**: What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, according to the Pitfalls s  
**Rewritten**: pitfalls taxonomy categories Large Language Model code intelligence survey errors limitations challenges software engine

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.3333 | +0.1667 | 0.1667 | 0.3333 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.5000 | 0.3333 | -0.1667 | 0.6667 | 0.3333 | -0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.5000 | +0.0000 | 0.6667 | 0.6667 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_006_en (method, EN)

**Raw**: How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what access does it requi  
**Rewritten**: FlippedRAG black-box opinion manipulation attack methodology access requirements Retrieval-Augmented Generation adversar

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.5000 | +0.5000 | 0.0000 | 0.5000 | +0.5000 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | 1.0000 | +1.0000 |
| 10 | 0.5000 | 0.6667 | +0.1667 | 0.5000 | 0.6667 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## cross_001_zh (comparison, ZH)

**Raw**: 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？  
**Rewritten**: 检索增强生成系统 攻击方法 比较 PoisonedRAG Machine Against the RAG 威胁模型 区别 对抗攻击 数据投毒 检索污染 安全漏洞

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1000 | 0.1000 | +0.0000 | 0.2000 | 0.2000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.1000 | 0.1000 | +0.0000 | 0.2000 | 0.2000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.3000 | 0.1000 | -0.2000 | 0.4000 | 0.2000 | -0.2000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## cross_002_zh (comparison, ZH)

**Raw**: 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？  
**Rewritten**: 比较 FlatD、MACO 和 Hardening DNN Binaries 三种方法保护深度神经网络模型免受逆向工程攻击的技术手段 深度神经网络模型保护 逆向工程防御 模型混淆 二进制加固 神经网络加密

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 0.6667 | 0.6667 | +0.0000 | 0.3333 | 0.0000 | -0.3333 |
| 10 | 0.0000 | 0.1000 | +0.1000 | 0.0000 | 0.2000 | +0.2000 | 0.6667 | 0.6667 | +0.0000 | 0.3333 | 0.6667 | +0.3333 |
| 20 | 0.1000 | 0.2000 | +0.1000 | 0.2000 | 0.4000 | +0.2000 | 0.6667 | 0.6667 | +0.0000 | 0.6667 | 0.6667 | +0.0000 |

## single_001_zh (method, ZH)

**Raw**: AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？  
**Rewritten**: AgentSentinel 如何为大语言模型代理提供端到端的实时安全防御？其核心架构是什么？安全监控 威胁检测 防护机制

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.0000 | -0.1667 | 0.1667 | 0.0000 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.1667 | 0.1667 | +0.0000 | 0.1667 | 0.1667 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.1667 | -0.3333 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_002_zh (method, ZH)

**Raw**: Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？  
**Rewritten**: Appatch 自动自适应提示方法 程序修复 代码生成 补丁生成 提示工程 大语言模型 动态提示优化

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.3333 | 0.1667 | -0.1667 | 0.8333 | 0.5000 | -0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_003_zh (method, ZH)

**Raw**: CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？  
**Rewritten**: 代码大语言模型开发工具包 如何为代码大语言模型提供上下文 代码智能任务改进 框架组件 上下文管理 代码表示学习 代码生成与理解

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.0000 | -0.1667 | 0.3333 | 0.0000 | -0.3333 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |
| 10 | 0.8333 | 0.0000 | -0.8333 | 0.8333 | 0.0000 | -0.8333 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |
| 20 | 0.8333 | 0.0000 | -0.8333 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |

## single_004_zh (method, ZH)

**Raw**: 《LLMs: Understanding Code Syntax and Semantics》提出了什么方法来利用 LLM 进行代码理解？  
**Rewritten**: 大语言模型 代码语法和语义理解 方法 代码表示学习 程序分析 利用大语言模型进行代码理解

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.1667 | 0.0000 | -0.1667 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |
| 10 | 0.1667 | 0.0000 | -0.1667 | 0.5000 | 0.0000 | -0.5000 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |
| 20 | 0.5000 | 0.0000 | -0.5000 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |

## single_005_zh (fact, ZH)

**Raw**: 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？  
**Rewritten**: 根据陷阱综述，使用大语言模型进行代码智能时的主要陷阱类别和分类体系是什么 代码生成 代码理解 错误类型 挑战 局限性

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.1667 | 0.0000 | -0.1667 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |
| 10 | 0.1667 | 0.0000 | -0.1667 | 0.5000 | 0.0000 | -0.5000 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |
| 20 | 0.1667 | 0.0000 | -0.1667 | 0.5000 | 0.0000 | -0.5000 | 1.0000 | 0.0000 | -1.0000 | 1.0000 | 0.0000 | -1.0000 |

## single_006_zh (method, ZH)

**Raw**: FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？  
**Rewritten**: FlippedRAG 检索增强生成 黑盒观点操纵 攻击方法 访问权限 对抗攻击 文本操纵 模型安全性

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 0.0000 | -1.0000 |
| 10 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

---

# 3. 全局平均指标对比（所有策略）

## vector_only

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.0208 | 0.0104 | -0.0104 | 0.0417 | 0.0104 | -0.0312 | 0.4688 | 0.2917 | -0.1771 | 0.1667 | 0.0625 | -0.1042 | 0.4688 | 0.2687 | -0.2000 |
| 10 | 0.0208 | 0.0104 | -0.0104 | 0.0417 | 0.0167 | -0.0250 | 0.7812 | 0.4583 | -0.3229 | 0.3229 | 0.1667 | -0.1563 | 0.5437 | 0.3344 | -0.2094 |
| 20 | 0.0271 | 0.0104 | -0.0167 | 0.0479 | 0.0271 | -0.0208 | 0.8229 | 0.7292 | -0.0938 | 0.4062 | 0.4167 | +0.0104 | 0.5687 | 0.3969 | -0.1719 |

## hybrid_no_rerank

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.0687 | 0.0521 | -0.0167 | 0.1271 | 0.0625 | -0.0646 | 0.9271 | 0.6250 | -0.3021 | 0.7188 | 0.3958 | -0.3229 | 0.5813 | 0.5031 | -0.0781 |
| 10 | 0.1625 | 0.0854 | -0.0771 | 0.2521 | 0.1021 | -0.1500 | 0.9271 | 0.7188 | -0.2083 | 0.8646 | 0.5208 | -0.3438 | 0.6062 | 0.5531 | -0.0531 |
| 20 | 0.2583 | 0.1500 | -0.1083 | 0.3438 | 0.1771 | -0.1667 | 0.9792 | 0.9167 | -0.0625 | 0.9583 | 0.7604 | -0.1979 | 0.6312 | 0.6188 | -0.0125 |

## hybrid_rerank

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.1437 | 0.1000 | -0.0437 | 0.2021 | 0.1896 | -0.0125 | 0.8854 | 0.8125 | -0.0729 | 0.7292 | 0.6146 | -0.1146 | 0.5938 | 0.5531 | -0.0406 |
| 10 | 0.3333 | 0.1729 | -0.1604 | 0.4396 | 0.2583 | -0.1813 | 0.9062 | 0.8333 | -0.0729 | 0.8438 | 0.6354 | -0.2083 | 0.6062 | 0.6062 | +0.0000 |
| 20 | 0.4604 | 0.3063 | -0.1542 | 0.6375 | 0.4313 | -0.2062 | 0.9583 | 0.8854 | -0.0729 | 0.9583 | 0.7917 | -0.1667 | 0.6312 | 0.6188 | -0.0125 |

## hybrid_score

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.1708 | 0.1479 | -0.0229 | 0.2458 | 0.2062 | -0.0396 | 0.9375 | 0.7396 | -0.1979 | 0.8229 | 0.5938 | -0.2292 | 0.5938 | 0.5687 | -0.0250 |
| 10 | 0.3438 | 0.2479 | -0.0958 | 0.4813 | 0.3292 | -0.1521 | 0.9375 | 0.7708 | -0.1667 | 0.9167 | 0.7188 | -0.1979 | 0.6312 | 0.5687 | -0.0625 |
| 20 | 0.5104 | 0.3667 | -0.1437 | 0.6729 | 0.4813 | -0.1917 | 0.9583 | 0.7917 | -0.1667 | 0.9583 | 0.7396 | -0.2188 | 0.6312 | 0.5813 | -0.0500 |

---

# 4. 按问题类型汇总（hybrid_score）

## comparison (4 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.1000 | 0.0500 | -0.0500 | 0.5417 | 0.3750 | -0.1667 |
| 10 | 0.1250 | 0.0750 | -0.0500 | 0.6667 | 0.6250 | -0.0417 |
| 20 | 0.2500 | 0.1750 | -0.0750 | 0.8333 | 0.7083 | -0.1250 |

## fact (2 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.0833 | 0.1667 | +0.0833 | 1.0000 | 0.5000 | -0.5000 |
| 10 | 0.3333 | 0.1667 | -0.1667 | 1.0000 | 0.5000 | -0.5000 |
| 20 | 0.3333 | 0.2500 | -0.0833 | 1.0000 | 0.5000 | -0.5000 |

## method (10 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.2167 | 0.1833 | -0.0333 | 0.9000 | 0.7000 | -0.2000 |
| 10 | 0.4333 | 0.3333 | -0.1000 | 1.0000 | 0.8000 | -0.2000 |
| 20 | 0.6500 | 0.4667 | -0.1833 | 1.0000 | 0.8000 | -0.2000 |

---

# 5. 按语言汇总（hybrid_score）

## EN (8 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.2875 | 0.2833 | -0.0042 | 0.7292 | 0.8125 | +0.0833 |
| 10 | 0.4667 | 0.4292 | -0.0375 | 0.9167 | 0.8542 | -0.0625 |
| 20 | 0.6583 | 0.6125 | -0.0458 | 0.9583 | 0.8958 | -0.0625 |

## ZH (8 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.0542 | 0.0125 | -0.0417 | 0.9167 | 0.3750 | -0.5417 |
| 10 | 0.2208 | 0.0667 | -0.1542 | 0.9167 | 0.5833 | -0.3333 |
| 20 | 0.3625 | 0.1208 | -0.2417 | 0.9583 | 0.5833 | -0.3750 |


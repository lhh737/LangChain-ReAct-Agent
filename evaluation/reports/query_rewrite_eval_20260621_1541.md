# Query Rewrite 消融评估报告

**生成时间**: 2026-06-21 15:41  
**数据集**: `rag_eval_20.jsonl` (16 answerable questions)  
**评估策略**: ['vector_only', 'hybrid_no_rerank', 'hybrid_rerank', 'hybrid_score']  
**k 值**: [5, 10, 20]  
**缓存文件**: `query_rewrite_cache.json`

---

# 1. 改写前后 Query 对照

| ID | Lang | Raw Query | Rewritten Query |
|----|------|-----------|-----------------|
| cross_001_en | EN | Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG sys | PoisonedRAG Machine Against the RAG attack RAG systems threat model differences  |
| cross_002_en | EN | Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do th | FlatD MACO Hardening DNN Binaries approaches protect Deep Neural Network models  |
| single_001_en | EN | How does AgentSentinel provide end-to-end and real-time security defense for LLM | AgentSentinel end-to-end real-time security defense Large Language Model agents  |
| single_002_en | EN | What is Appatch's automated adaptive prompting approach? How does it improve pro | Appatch automated adaptive prompting approach program repair code generation imp |
| single_003_en | EN | How does CodeLLM-Devkit contextualize code LLMs? What framework components does  | CodeLLM-Devkit contextualization framework components code Large Language Models |
| single_004_en | EN | What method does 'LLMs: Understanding Code Syntax and Semantics' propose for usi | Large Language Models Understanding Code Syntax and Semantics proposed method LL |
| single_005_en | EN | What are the main categories and taxonomy of pitfalls when using LLMs for code i | categories taxonomy pitfalls Large Language Models code intelligence Pitfalls su |
| single_006_en | EN | How does FlippedRAG achieve black-box opinion manipulation? What is its attack m | FlippedRAG black-box opinion manipulation attack methodology access requirements |
| cross_001_zh | ZH | 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？ | Comparison of PoisonedRAG and Machine Against the RAG: how do they attack RAG sy |
| cross_002_zh | ZH | 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？ | Comparison of FlatD, MACO, and Hardening DNN Binaries: methods for protecting DN |
| single_001_zh | ZH | AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？ | AgentSentinel end-to-end real-time security defense LLM agents core architecture |
| single_002_zh | ZH | Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？ | Appatch automatic adaptive prompting method program repair code generation impro |
| single_003_zh | ZH | CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？ | CodeLLM-Devkit context provision for code LLM, framework components for code int |
| single_004_zh | ZH | 《LLMs: Understanding Code Syntax and Semantics》提出了什么方法来利用 LLM 进行代码理解？ | LLMs: Understanding Code Syntax and Semantics proposed method for leveraging LLM |
| single_005_zh | ZH | 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？ | Pitfalls survey pitfalls categories taxonomy code intelligence LLM |
| single_006_zh | ZH | FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？ | poisoning</think> manipulation

注意：FlippedRAG本身是方法名，保留。添加black-box, opinion mani |

---

# 2. 逐题指标对比（策略：hybrid_score）

## cross_001_en (comparison, EN)

**Raw**: Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are the key differences i  
**Rewritten**: PoisonedRAG Machine Against the RAG attack RAG systems threat model differences comparison retrieval poisoning adversari

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1000 | 0.0000 | -0.1000 | 0.2000 | 0.0000 | -0.2000 | 1.0000 | 0.5000 | -0.5000 | 0.5000 | 0.5000 | +0.0000 |
| 10 | 0.2000 | 0.1000 | -0.1000 | 0.3000 | 0.1000 | -0.2000 | 1.0000 | 0.5000 | -0.5000 | 1.0000 | 0.5000 | -0.5000 |
| 20 | 0.4000 | 0.2000 | -0.2000 | 0.7000 | 0.3000 | -0.4000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 0.5000 | -0.5000 |

## cross_002_en (comparison, EN)

**Raw**: Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect DNN models from rever  
**Rewritten**: FlatD MACO Hardening DNN Binaries approaches protect Deep Neural Network models reverse engineering obfuscation model se

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.2000 | 0.0000 | -0.2000 | 0.2000 | 0.0000 | -0.2000 | 0.3333 | 0.3333 | +0.0000 | 0.3333 | 0.0000 | -0.3333 |
| 10 | 0.2000 | 0.1000 | -0.1000 | 0.2000 | 0.1000 | -0.1000 | 0.3333 | 0.3333 | +0.0000 | 0.3333 | 0.3333 | +0.0000 |
| 20 | 0.2000 | 0.3000 | +0.1000 | 0.3000 | 0.4000 | +0.1000 | 0.6667 | 1.0000 | +0.3333 | 0.6667 | 0.6667 | +0.0000 |

## single_001_en (method, EN)

**Raw**: How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its core architecture?  
**Rewritten**: AgentSentinel end-to-end real-time security defense Large Language Model agents core architecture security framework thr

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.5000 | 0.1667 | -0.3333 | 0.6667 | 0.3333 | -0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.6667 | 0.6667 | +0.0000 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_002_en (method, EN)

**Raw**: What is Appatch's automated adaptive prompting approach? How does it improve program repair or code generation?  
**Rewritten**: Appatch automated adaptive prompting approach program repair code generation improvement methodology self-healing softwa

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.6667 | 0.6667 | +0.0000 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.6667 | 0.6667 | +0.0000 | 0.8333 | 1.0000 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_003_en (method, EN)

**Raw**: How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for improving code intelligen  
**Rewritten**: CodeLLM-Devkit contextualization framework components code Large Language Models code intelligence tasks code generation

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.1667 | +0.0000 | 0.3333 | 0.3333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.3333 | 0.3333 | +0.0000 | 0.5000 | 0.3333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.5000 | +0.0000 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_004_en (method, EN)

**Raw**: What method does 'LLMs: Understanding Code Syntax and Semantics' propose for using LLMs in code comprehension?  
**Rewritten**: Large Language Models Understanding Code Syntax and Semantics proposed method LLMs code comprehension program understand

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.5000 | 0.1667 | -0.3333 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.6667 | 0.3333 | -0.3333 | 0.8333 | 0.6667 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.8333 | 1.0000 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_005_en (fact, EN)

**Raw**: What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, according to the Pitfalls s  
**Rewritten**: categories taxonomy pitfalls Large Language Models code intelligence Pitfalls survey software engineering code generatio

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.3333 | +0.1667 | 0.1667 | 0.3333 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.5000 | 0.5000 | +0.0000 | 0.6667 | 0.6667 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.6667 | +0.1667 | 0.6667 | 0.8333 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_006_en (method, EN)

**Raw**: How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what access does it requi  
**Rewritten**: FlippedRAG black-box opinion manipulation attack methodology access requirements adversarial attack retrieval-augmented 

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.5000 | +0.5000 | 0.0000 | 0.5000 | +0.5000 | 1.0000 | 1.0000 | +0.0000 | 0.0000 | 1.0000 | +1.0000 |
| 10 | 0.5000 | 0.5000 | +0.0000 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 1.0000 | 0.8333 | -0.1667 | 1.0000 | 0.8333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## cross_001_zh (comparison, ZH)

**Raw**: 比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？  
**Rewritten**: Comparison of PoisonedRAG and Machine Against the RAG: how do they attack RAG systems? Key differences in threat models,

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1000 | 0.2000 | +0.1000 | 0.2000 | 0.4000 | +0.2000 | 1.0000 | 0.5000 | -0.5000 | 1.0000 | 0.5000 | -0.5000 |
| 10 | 0.1000 | 0.2000 | +0.1000 | 0.2000 | 0.4000 | +0.2000 | 1.0000 | 0.5000 | -0.5000 | 1.0000 | 0.5000 | -0.5000 |
| 20 | 0.3000 | 0.3000 | +0.0000 | 0.4000 | 0.7000 | +0.3000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## cross_002_zh (comparison, ZH)

**Raw**: 比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？  
**Rewritten**: Comparison of FlatD, MACO, and Hardening DNN Binaries: methods for protecting DNN models against reverse engineering att

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 0.6667 | 0.3333 | -0.3333 | 0.3333 | 0.3333 | +0.0000 |
| 10 | 0.0000 | 0.0000 | +0.0000 | 0.0000 | 0.0000 | +0.0000 | 0.6667 | 0.3333 | -0.3333 | 0.3333 | 0.3333 | +0.0000 |
| 20 | 0.1000 | 0.0000 | -0.1000 | 0.2000 | 0.0000 | -0.2000 | 0.6667 | 1.0000 | +0.3333 | 0.6667 | 0.3333 | -0.3333 |

## single_001_zh (method, ZH)

**Raw**: AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？  
**Rewritten**: AgentSentinel end-to-end real-time security defense LLM agents core architecture threat detection mitigation

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.5000 | +0.3333 | 0.1667 | 0.5000 | +0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.1667 | 0.5000 | +0.3333 | 0.1667 | 0.8333 | +0.6667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.6667 | +0.1667 | 0.5000 | 0.8333 | +0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_002_zh (method, ZH)

**Raw**: Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？  
**Rewritten**: Appatch automatic adaptive prompting method program repair code generation improvement

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.1667 | +0.1667 | 0.0000 | 0.3333 | +0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.3333 | 0.5000 | +0.1667 | 0.8333 | 0.8333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 0.8333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_003_zh (method, ZH)

**Raw**: CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？  
**Rewritten**: CodeLLM-Devkit context provision for code LLM, framework components for code intelligence tasks, context augmentation, c

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.1667 | 0.1667 | +0.0000 | 0.3333 | 0.3333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.8333 | 0.5000 | -0.3333 | 0.8333 | 0.5000 | -0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.8333 | 0.6667 | -0.1667 | 1.0000 | 0.6667 | -0.3333 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_004_zh (method, ZH)

**Raw**: 《LLMs: Understanding Code Syntax and Semantics》提出了什么方法来利用 LLM 进行代码理解？  
**Rewritten**: LLMs: Understanding Code Syntax and Semantics proposed method for leveraging LLM in code understanding, code syntax anal

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.1667 | 0.3333 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.1667 | 0.1667 | +0.0000 | 0.5000 | 0.6667 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.5000 | 0.6667 | +0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_005_zh (fact, ZH)

**Raw**: 根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？  
**Rewritten**: Pitfalls survey pitfalls categories taxonomy code intelligence LLM

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.0000 | +0.0000 | 0.1667 | 0.1667 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.1667 | 0.1667 | +0.0000 | 0.5000 | 0.3333 | -0.1667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.1667 | 0.1667 | +0.0000 | 0.5000 | 0.5000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

## single_006_zh (method, ZH)

**Raw**: FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？  
**Rewritten**: poisoning</think> manipulation

注意：FlippedRAG本身是方法名，保留。添加black-box, opinion manipulation, adversarial attack, retrieval-

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|
| 5 | 0.0000 | 0.3333 | +0.3333 | 0.0000 | 0.5000 | +0.5000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.0000 | 0.3333 | +0.3333 | 0.0000 | 0.5000 | +0.5000 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.0000 | 0.5000 | +0.5000 | 0.0000 | 0.6667 | +0.6667 | 1.0000 | 1.0000 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |

---

# 3. 全局平均指标对比（所有策略）

## vector_only

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.0208 | 0.0000 | -0.0208 | 0.0417 | 0.0063 | -0.0354 | 0.4688 | 0.5521 | +0.0833 | 0.1667 | 0.2604 | +0.0938 | 0.4688 | 0.3406 | -0.1281 |
| 10 | 0.0208 | 0.0104 | -0.0104 | 0.0417 | 0.0583 | +0.0167 | 0.7812 | 0.7083 | -0.0729 | 0.3229 | 0.4479 | +0.1250 | 0.5437 | 0.4438 | -0.1000 |
| 20 | 0.0271 | 0.0333 | +0.0062 | 0.0479 | 0.1208 | +0.0729 | 0.8229 | 0.9062 | +0.0833 | 0.4062 | 0.5833 | +0.1771 | 0.5687 | 0.5062 | -0.0625 |

## hybrid_no_rerank

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.0687 | 0.0896 | +0.0208 | 0.1271 | 0.1208 | -0.0063 | 0.9271 | 0.8542 | -0.0729 | 0.7188 | 0.6562 | -0.0625 | 0.5813 | 0.5938 | +0.0125 |
| 10 | 0.1625 | 0.1417 | -0.0208 | 0.2521 | 0.1937 | -0.0583 | 0.9271 | 0.8542 | -0.0729 | 0.8646 | 0.7188 | -0.1458 | 0.6062 | 0.6188 | +0.0125 |
| 20 | 0.2583 | 0.2458 | -0.0125 | 0.3438 | 0.3146 | -0.0292 | 0.9792 | 0.9271 | -0.0521 | 0.9583 | 0.9062 | -0.0521 | 0.6312 | 0.6312 | +0.0000 |

## hybrid_rerank

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.1437 | 0.1979 | +0.0542 | 0.2125 | 0.2833 | +0.0708 | 0.8854 | 0.8750 | -0.0104 | 0.7292 | 0.7292 | +0.0000 | 0.5938 | 0.6062 | +0.0125 |
| 10 | 0.3438 | 0.3354 | -0.0083 | 0.4396 | 0.4375 | -0.0021 | 0.9062 | 0.8750 | -0.0312 | 0.8438 | 0.7917 | -0.0521 | 0.5938 | 0.6312 | +0.0375 |
| 20 | 0.4500 | 0.5083 | +0.0583 | 0.6271 | 0.6813 | +0.0542 | 0.9583 | 0.9167 | -0.0417 | 0.9583 | 0.8958 | -0.0625 | 0.6312 | 0.6312 | +0.0000 |

## hybrid_score

| k | raw strict_chunk | rw strict_chunk | Δ | raw window_chunk | rw window_chunk | Δ | raw source | rw source | Δ | raw evidence | rw evidence | Δ | raw keyword | rw keyword | Δ |
|---|-----------------|-----------------|---|------------------|-----------------|---|------------|-----------|---|--------------|-------------|---|---|-------------|---|
| 5 | 0.1708 | 0.2104 | +0.0396 | 0.2458 | 0.3375 | +0.0917 | 0.9375 | 0.8542 | -0.0833 | 0.8229 | 0.8333 | +0.0104 | 0.5938 | 0.6031 | +0.0094 |
| 10 | 0.3438 | 0.3479 | +0.0042 | 0.4813 | 0.5167 | +0.0354 | 0.9375 | 0.8542 | -0.0833 | 0.9167 | 0.8542 | -0.0625 | 0.6312 | 0.6188 | -0.0125 |
| 20 | 0.5104 | 0.5500 | +0.0396 | 0.6729 | 0.6917 | +0.0188 | 0.9583 | 1.0000 | +0.0417 | 0.9583 | 0.9062 | -0.0521 | 0.6312 | 0.6438 | +0.0125 |

---

# 4. 按问题类型汇总（hybrid_score）

## comparison (4 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.1000 | 0.0500 | -0.0500 | 0.5417 | 0.3333 | -0.2083 |
| 10 | 0.1250 | 0.1000 | -0.0250 | 0.6667 | 0.4167 | -0.2500 |
| 20 | 0.2500 | 0.2000 | -0.0500 | 0.8333 | 0.6250 | -0.2083 |

## fact (2 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.0833 | 0.1667 | +0.0833 | 1.0000 | 1.0000 | +0.0000 |
| 10 | 0.3333 | 0.3333 | +0.0000 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.3333 | 0.4167 | +0.0833 | 1.0000 | 1.0000 | +0.0000 |

## method (10 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.2167 | 0.2833 | +0.0667 | 0.9000 | 1.0000 | +0.1000 |
| 10 | 0.4333 | 0.4500 | +0.0167 | 1.0000 | 1.0000 | +0.0000 |
| 20 | 0.6500 | 0.7167 | +0.0667 | 1.0000 | 1.0000 | +0.0000 |

---

# 5. 按语言汇总（hybrid_score）

## EN (8 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.2875 | 0.2500 | -0.0375 | 0.7292 | 0.8125 | +0.0833 |
| 10 | 0.4667 | 0.4000 | -0.0667 | 0.9167 | 0.8542 | -0.0625 |
| 20 | 0.6583 | 0.6667 | +0.0083 | 0.9583 | 0.8958 | -0.0625 |

## ZH (8 questions)

| k | raw strict_chunk | rw strict_chunk | Δ | raw evidence | rw evidence | Δ |
|---|-----------------|-----------------|---|--------------|-------------|---|
| 5 | 0.0542 | 0.1708 | +0.1167 | 0.9167 | 0.8542 | -0.0625 |
| 10 | 0.2208 | 0.2958 | +0.0750 | 0.9167 | 0.8542 | -0.0625 |
| 20 | 0.3625 | 0.4333 | +0.0708 | 0.9583 | 0.9167 | -0.0417 |


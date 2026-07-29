"""根据当前 ChromaDB 构建 rag_eval_20.jsonl 数据集"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path

OUTPUT_PATH = get_abs_path("evaluation/rag_eval_20.jsonl")

# ─── 20 道题目定义 ───
QUESTIONS = [
    # ===== EN =====
    {
        "id": "cross_001_en",
        "question": "Compare PoisonedRAG and Machine Against the RAG: how do they each attack RAG systems, and what are the key differences in their threat models?",
        "answer_type": "comparison",
        "should_answer": True,
        "gold_facts": [
            "PoisonedRAG injects malicious passages into the knowledge corpus to corrupt retrieval results, requiring corpus access.",
            "Machine Against the RAG jams RAG systems with blocker documents that suppress relevant retrieval without corpus poisoning.",
            "PoisonedRAG requires attacker access to the knowledge base; Machine Against the RAG only requires the ability to inject documents at query time.",
        ],
        "expected_sources": [
            {"filename_contains": "PoisonedRAG", "pages_any": [2, 3, 4]},
            {"filename_contains": "Machine Against the RAG", "pages_any": [2, 3, 4]},
        ],
        "must_contain": ["attack", "RAG", "knowledge", "corpus", "retrieval"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "cross_002_en",
        "question": "Compare FlatD, MACO, and Hardening DNN Binaries: what different approaches do they take to protect DNN models from reverse engineering?",
        "answer_type": "comparison",
        "should_answer": True,
        "gold_facts": [
            "FlatD uses Control Flow Flattening to conceal the CFG of DNN programs integrated into TVM compilation.",
            "MACO uses compiler-level obfuscation to prevent model extraction from compiled binaries.",
            "Hardening DNN Binaries proposes hardening techniques against reverse engineering attacks on DNN executables.",
            "All three target protecting DNN intellectual property at the binary level but differ in their obfuscation strategies.",
        ],
        "expected_sources": [
            {"filename_contains": "FlatD", "pages_any": [2, 3, 4]},
            {"filename_contains": "MACO", "pages_any": [2, 3, 4]},
            {"filename_contains": "Hardening Deep Neural Network", "pages_any": [2, 3, 4]},
        ],
        "must_contain": ["protect", "DNN", "obfuscation", "reverse"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "single_001_en",
        "question": "How does AgentSentinel provide end-to-end and real-time security defense for LLM agents? What is its core architecture?",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "AgentSentinel is an end-to-end real-time security defense system for LLM agents.",
            "It monitors agent behavior and detects security threats during LLM agent execution.",
        ],
        "expected_sources": [
            {"filename_contains": "AgentSentinel", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["AgentSentinel", "security", "defense", "agent", "LLM"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "single_002_en",
        "question": "What is Appatch's automated adaptive prompting approach? How does it improve program repair or code generation?",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "Appatch uses automated adaptive prompting to improve code generation and program repair.",
            "It dynamically adjusts prompts based on feedback or context to achieve better results.",
        ],
        "expected_sources": [
            {"filename_contains": "Appatch", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["Appatch", "adaptive", "prompting", "code", "repair"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "single_003_en",
        "question": "How does CodeLLM-Devkit contextualize code LLMs? What framework components does it provide for improving code intelligence tasks?",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "CodeLLM-Devkit is a framework for contextualizing code LLMs to improve code intelligence.",
            "It provides tooling and components for integrating context into code LLM workflows.",
        ],
        "expected_sources": [
            {"filename_contains": "Codellm-Devkit", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["CodeLLM", "Devkit", "code", "framework", "LLM"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "single_004_en",
        "question": "What method does 'LLMs: Understanding Code Syntax and Semantics' propose for using LLMs in code comprehension?",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "The paper proposes methods for LLMs to understand both code syntax and semantics.",
            "It addresses how LLMs can be applied to code comprehension tasks beyond surface-level patterns.",
        ],
        "expected_sources": [
            {"filename_contains": "LLMs: Understanding Code Syntax", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["LLM", "code", "syntax", "semantics", "understanding"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "single_005_en",
        "question": "What are the main categories and taxonomy of pitfalls when using LLMs for code intelligence, according to the Pitfalls survey?",
        "answer_type": "fact",
        "should_answer": True,
        "gold_facts": [
            "The Pitfalls survey provides a taxonomy of common failure modes when applying LLMs to code intelligence tasks.",
            "Categories include issues related to data quality, model evaluation, and task formulation.",
        ],
        "expected_sources": [
            {"filename_contains": "Pitfalls", "pages_any": [2, 3, 4, 5, 6]},
        ],
        "must_contain": ["pitfall", "code", "intelligence", "LLM", "taxonomy"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "single_006_en",
        "question": "How does FlippedRAG achieve black-box opinion manipulation? What is its attack methodology and what access does it require?",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "FlippedRAG uses black-box opinion manipulation through crafted queries without modifying the knowledge base.",
            "FlippedRAG does not need access to the knowledge corpus.",
        ],
        "expected_sources": [
            {"filename_contains": "FlippedRAG", "pages_any": [2, 3, 4]},
        ],
        "must_contain": ["FlippedRAG", "black-box", "opinion", "manipulation", "query"],
        "must_not_contain": ["unable to find"],
    },
    {
        "id": "unanswerable_001_en",
        "question": "How does GPT-5 compare against the methods in these papers for code intelligence and DNN security tasks?",
        "answer_type": "scope",
        "should_answer": False,
        "gold_facts": [],
        "expected_sources": [],
        "must_contain": ["unable to find", "not covered", "no information"],
        "must_not_contain": ["GPT-5 outperforms"],
    },
    {
        "id": "unanswerable_002_en",
        "question": "What is the carbon footprint and energy consumption of training the models discussed in these papers?",
        "answer_type": "scope",
        "should_answer": False,
        "gold_facts": [],
        "expected_sources": [],
        "must_contain": ["unable to find", "not covered", "no information"],
        "must_not_contain": ["The carbon footprint is"],
    },

    # ===== ZH =====
    {
        "id": "cross_001_zh",
        "question": "比较 PoisonedRAG 和 Machine Against the RAG：它们各自如何攻击 RAG 系统？威胁模型的关键区别是什么？",
        "answer_type": "comparison",
        "should_answer": True,
        "gold_facts": [
            "PoisonedRAG 向知识库注入恶意段落来污染检索结果，需要访问知识库。",
            "Machine Against the RAG 通过阻塞文档压制相关检索，无需污染知识库。",
            "PoisonedRAG 需要攻击者访问知识库；Machine Against the RAG 仅需在查询时注入文档。",
        ],
        "expected_sources": [
            {"filename_contains": "PoisonedRAG", "pages_any": [2, 3, 4]},
            {"filename_contains": "Machine Against the RAG", "pages_any": [2, 3, 4]},
        ],
        "must_contain": ["攻击", "RAG", "知识库", "检索"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "cross_002_zh",
        "question": "比较 FlatD、MACO 和 Hardening DNN Binaries：它们各自采用什么方法保护 DNN 模型免受逆向工程攻击？",
        "answer_type": "comparison",
        "should_answer": True,
        "gold_facts": [
            "FlatD 使用控制流平坦化隐藏 DNN 程序的控制流图，集成到 TVM 编译中。",
            "MACO 使用编译器级混淆防止从编译二进制文件中提取模型。",
            "Hardening DNN Binaries 提出针对 DNN 可执行文件逆向攻击的加固技术。",
        ],
        "expected_sources": [
            {"filename_contains": "FlatD", "pages_any": [2, 3, 4]},
            {"filename_contains": "MACO", "pages_any": [2, 3, 4]},
            {"filename_contains": "Hardening Deep Neural Network", "pages_any": [2, 3, 4]},
        ],
        "must_contain": ["保护", "DNN", "混淆", "逆向"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "single_001_zh",
        "question": "AgentSentinel 如何为 LLM 代理提供端到端的实时安全防御？其核心架构是什么？",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "AgentSentinel 是一个端到端的实时 LLM 代理安全防御系统。",
            "它监控代理行为并在 LLM 代理执行过程中检测安全威胁。",
        ],
        "expected_sources": [
            {"filename_contains": "AgentSentinel", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["AgentSentinel", "安全", "防御", "代理", "LLM"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "single_002_zh",
        "question": "Appatch 的自动自适应提示方法是什么？它如何改进程序修复或代码生成？",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "Appatch 使用自动自适应提示来改进代码生成和程序修复。",
            "它根据反馈或上下文动态调整提示以获得更好的结果。",
        ],
        "expected_sources": [
            {"filename_contains": "Appatch", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["Appatch", "自适应", "提示", "代码", "修复"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "single_003_zh",
        "question": "CodeLLM-Devkit 如何为代码 LLM 提供上下文？它为改进代码智能任务提供了哪些框架组件？",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "CodeLLM-Devkit 是一个为代码 LLM 提供上下文的框架，用于改进代码智能。",
            "它提供了将上下文集成到代码 LLM 工作流中的工具和组件。",
        ],
        "expected_sources": [
            {"filename_contains": "Codellm-Devkit", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["CodeLLM", "Devkit", "代码", "框架", "LLM"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "single_004_zh",
        "question": "《LLMs: Understanding Code Syntax and Semantics》提出了什么方法来利用 LLM 进行代码理解？",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "该论文提出了让 LLM 理解代码语法和语义的方法。",
            "它解决了 LLM 如何应用于超越表面模式的代码理解任务。",
        ],
        "expected_sources": [
            {"filename_contains": "LLMs: Understanding Code Syntax", "pages_any": [2, 3, 4, 5]},
        ],
        "must_contain": ["LLM", "代码", "语法", "语义", "理解"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "single_005_zh",
        "question": "根据 Pitfalls 综述，使用 LLM 进行代码智能时的主要陷阱类别和分类体系是什么？",
        "answer_type": "fact",
        "should_answer": True,
        "gold_facts": [
            "Pitfalls 综述提供了将 LLM 应用于代码智能任务时常见失败模式的分类体系。",
            "类别包括数据质量、模型评估和任务制定等方面的问题。",
        ],
        "expected_sources": [
            {"filename_contains": "Pitfalls", "pages_any": [2, 3, 4, 5, 6]},
        ],
        "must_contain": ["陷阱", "代码", "智能", "LLM", "分类"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "single_006_zh",
        "question": "FlippedRAG 如何实现黑盒观点操纵？其攻击方法是什么？需要什么访问权限？",
        "answer_type": "method",
        "should_answer": True,
        "gold_facts": [
            "FlippedRAG 通过精心构造的查询进行黑盒观点操纵，无需修改知识库。",
            "FlippedRAG 不需要访问知识库。",
        ],
        "expected_sources": [
            {"filename_contains": "FlippedRAG", "pages_any": [2, 3, 4]},
        ],
        "must_contain": ["FlippedRAG", "黑盒", "观点", "操纵", "查询"],
        "must_not_contain": ["无法找到"],
    },
    {
        "id": "unanswerable_001_zh",
        "question": "GPT-5 与这些论文中提出的方法在代码智能和 DNN 安全任务上相比如何？",
        "answer_type": "scope",
        "should_answer": False,
        "gold_facts": [],
        "expected_sources": [],
        "must_contain": ["无法找到", "未涉及", "没有相关信息"],
        "must_not_contain": ["GPT-5 优于"],
    },
    {
        "id": "unanswerable_002_zh",
        "question": "这些论文中讨论的模型训练的碳排放和能源消耗是多少？",
        "answer_type": "scope",
        "should_answer": False,
        "gold_facts": [],
        "expected_sources": [],
        "must_contain": ["无法找到", "未涉及", "没有相关信息"],
        "must_not_contain": ["碳排放为"],
    },
]


def build():
    client = chromadb.PersistentClient(path=get_abs_path("chroma_db"))
    collection = client.get_collection(chroma_conf["collection_name"])
    all_data = collection.get(include=["metadatas", "documents"], limit=5000)

    # Build index: source_file -> list of (chunk_id, metadata, content)
    file_index = {}
    for m, doc in zip(all_data["metadatas"], all_data["documents"]):
        cid = m.get("chunk_id", "")
        if not cid:
            continue
        src = m.get("source_file", "")
        file_index.setdefault(src, []).append((cid, m, doc))

    def match_source(chunks, src_spec):
        """Filter chunks by filename_contains + pages_any"""
        keyword = src_spec.get("filename_contains", "")
        pages = set(src_spec.get("pages_any", []))
        matched = []
        for cid, m, doc in chunks:
            if keyword.lower() not in m.get("source_file", "").lower():
                continue
            if pages:
                ps = m.get("page_start")
                pe = m.get("page_end")
                if ps is not None and pe is not None:
                    chunk_pages = set(range(int(ps), int(pe) + 1))
                    if not (chunk_pages & pages):
                        continue
            matched.append((cid, m, doc))
        return matched

    def score_chunk(content, must_contain):
        """Keyword overlap score for ranking"""
        content_lower = content.lower()
        score = 0
        for kw in must_contain:
            if kw.lower() in content_lower:
                score += 1
        return score / len(must_contain) if must_contain else 0

    output = []
    for q in QUESTIONS:
        entry = {
            "id": q["id"],
            "question": q["question"],
            "answer_type": q["answer_type"],
            "should_answer": q["should_answer"],
            "gold_facts": q.get("gold_facts", []),
            "expected_sources": q.get("expected_sources", []),
            "must_contain": q.get("must_contain", []),
            "must_not_contain": q.get("must_not_contain", []),
            "expected_chunk_ids": [],
        }

        if q["should_answer"] and q["expected_sources"]:
            # Collect candidates from all expected sources
            candidates = []
            for src_spec in q["expected_sources"]:
                keyword = src_spec.get("filename_contains", "")
                # Find matching source file
                matched_src = None
                for src_name in file_index:
                    if keyword.lower() in src_name.lower():
                        matched_src = src_name
                        break
                if not matched_src:
                    print(f"  WARNING: no file matching '{keyword}'")
                    continue
                matched_chunks = match_source(file_index[matched_src], src_spec)
                candidates.extend(matched_chunks)

            # Score + filter by must_contain
            must_contain = q.get("must_contain", [])
            scored = []
            for cid, m, doc in candidates:
                sc = score_chunk(doc, must_contain)
                scored.append((sc, cid, m, doc))

            scored.sort(key=lambda x: x[0], reverse=True)

            # Deduplicate: max 6 chunks per source
            per_src_count = {}
            selected = []
            for sc, cid, m, doc in scored:
                src = m.get("source_file", "")
                if per_src_count.get(src, 0) >= 6:
                    continue
                selected.append(cid)
                per_src_count[src] = per_src_count.get(src, 0) + 1
                if len(selected) >= 10:
                    break

            entry["expected_chunk_ids"] = selected
            print(f"{q['id']}: {len(selected)} chunk_ids from {len(candidates)} candidates")

        output.append(entry)

    # Write
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for entry in output:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\nWritten to {OUTPUT_PATH} ({len(output)} questions)")


if __name__ == "__main__":
    build()

def main(argv=None) -> int:
    """CLI 入口"""
    if argv:
        print(f"Unknown arguments: {argv}", file=__import__("sys").stderr)
        return 1
    build()
    return 0

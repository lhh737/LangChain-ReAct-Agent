"""输出 evaluation/rag_eval_20.jsonl 中每题 expected_chunk_ids 的完整内容。"""
import json
import chromadb

from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path


def main():
    chroma_path = get_abs_path(chroma_conf.get("persist_directory", "chroma_db"))
    collection_name = chroma_conf.get("collection_name", "papers")
    jsonl_path = get_abs_path("evaluation/rag_eval_20.jsonl")

    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_collection(collection_name)
    all_chunks = collection.get(include=["metadatas", "documents"])

    id_map = {}
    for meta, doc in zip(all_chunks["metadatas"], all_chunks["documents"]):
        cid = meta.get("chunk_id", "")
        if cid:
            id_map[cid] = {"metadata": meta, "content": doc}

    print(f"ChromaDB 共 {len(id_map)} 个 chunk\n")

    with open(jsonl_path, "r", encoding="utf-8") as f:
        questions = [json.loads(line) for line in f if line.strip()]

    for q in questions:
        raw = q.get("expected_chunk_ids", [])
        if not raw:
            continue
        # 归一化为 grouped 格式: [["cid1"], ["cid2","cid3"], ...]
        groups = raw if isinstance(raw[0], list) else [[c] for c in raw]

        print("=" * 100)
        print(f"[{q['id']}] {q['question']}")
        print(f"type={q['answer_type']} | expected_groups={len(groups)}")
        print("=" * 100)

        for gi, group in enumerate(groups, 1):
            alt_tag = " (可替代)" if len(group) > 1 else ""
            for ci, cid in enumerate(group, 1):
                entry = id_map.get(cid)
                label = f"[G{gi}{alt_tag}]" if ci == 1 else "       "
                if entry is None:
                    print(f"\n  {label} {cid}  <<< NOT FOUND IN CHROMADB >>>")
                    continue
                meta = entry["metadata"]
                content = entry["content"]
                print(f"\n  {label} chunk_id={cid}")
                print(f"       paper: {meta.get('paper_title', 'N/A')[:80]}")
                print(f"       source: {meta.get('source_file', 'N/A')}")
                print(f"       section: {meta.get('section', 'N/A')} | pages: {meta.get('page_start', '?')}-{meta.get('page_end', '?')}")
                print(f"       tokens: ~{len(content.split())}")
                print(f"  " + "-" * 90)
                print(f"  {content}")
                print(f"  " + "-" * 90)

    print("\nDone.")


if __name__ == "__main__":
    main()

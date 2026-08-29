"""导出 ChromaDB 中所有 chunk 到文件。"""
import sys, json

OUTPUT = "/home/hgs/project/LangChain-ReAct-Agent/evaluation/all_chunks.jsonl"

try:
    import chromadb
    client = chromadb.PersistentClient(path="/home/hgs/project/LangChain-ReAct-Agent/chroma_db")
    collection = client.get_collection("agent")
    result = collection.get(include=["metadatas", "documents"])

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for i, (meta, doc) in enumerate(zip(result["metadatas"], result["documents"])):
            record = {
                "index": i,
                "chunk_id": meta.get("chunk_id", ""),
                "paper_title": meta.get("paper_title", ""),
                "source_file": meta.get("source_file", ""),
                "section": meta.get("section", ""),
                "section_title": meta.get("section_title", ""),
                "page_start": meta.get("page_start", ""),
                "page_end": meta.get("page_end", ""),
                "paper_id": meta.get("paper_id", ""),
                "content": doc,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Done. {i+1} chunks → {OUTPUT}")

except ImportError:
    print("chromadb 不可用，请先确保环境正确")
    sys.exit(1)

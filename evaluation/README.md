 # 1. 清除旧数据
  cd <project_root>
  rm -rf chroma_db/ md5.txt bm25_index.pkl data/abbreviation_index.json data/index_manifest.json data/academic_cache/

  # 2. 重建 ChromaDB（分块+入库）
  python3 -c "from rag.vector_store import VectorStoreService; VectorStoreService().load_document()"

  # 3. 重建 BM25 索引 + 缩写索引
  python3 -c "from rag.rag_service import RagSummarizeService; RagSummarizeService().rebuild_bm25_index()"

 python evaluation/dump_chunks.py > evaluation/evalution_test_chunk.txt 2>&1
 python evaluation/multi_query_eval.py
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config_handler import chroma_conf

from model.factory import embed_model


from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger

from rag.paper_parser import DocParser

import hashlib
import json
import os
import re

import tiktoken

_TIK_ENCODER: tiktoken.Encoding | None = None


def _tiktoken_count(text: str) -> int:
    """使用 tiktoken cl100k_base 做 token 计数，与 SiliconFlow OpenAI兼容 API 一致，纯本地无网络请求"""
    global _TIK_ENCODER
    if _TIK_ENCODER is None:
        _TIK_ENCODER = tiktoken.get_encoding("cl100k_base")
    return max(1, len(_TIK_ENCODER.encode(text)))


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )


    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def section_filtered_retriever(self, section: str, k: int | None = None):
        """按文档章节过滤的检索器，只检索指定章节的内容"""
        k = k or chroma_conf["k"]
        return self.vector_store.as_retriever(
            search_kwargs={"k": k, "filter": {"section": section}}
        )

    def _find_page_from_map(self, global_offset: int, char_to_page: list[tuple[int, int]]) -> int:
        """根据全局字符偏移 + char_to_page 映射查表得页码"""
        page = 1
        for start, page_num in char_to_page:
            if global_offset >= start:
                page = page_num
        return page

    # ── Sentence-priority chunking ──

    def _clean_section_text(self, text: str) -> str:
        """文本级去噪：过滤论文元数据行、图表残片区域、纯数字/URL/引用标号行"""

        # ── 论文模板元数据行 ──
        _META_PATTERNS = [
            r'CCS\s+Concepts',
            r'Keywords[:\s]|^Keywords$',
            r'ACM\s+Reference',
            r'Permission\s+to\s+make\s+digital',
            r'Authors.\s+addresses',
            r'Corresponding\s+author',
            r"Conference\s+'?\d{2}",
            r'Published\s+as',
            r'Preprint[:\s]',
            r'Under\s+review',
            r'Accepted\s+by',
            r'\d{4}\.\s*\d+\s*/\s*\d+\.\s*\$\d+',   # DOI-like
        ]
        _META_RE = re.compile('|'.join(_META_PATTERNS), re.IGNORECASE)

        def _is_short_fragment(line: str) -> bool:
            """图表节点标签/公式残片：≤3 词 且 ≤40 字符"""
            stripped = line.strip()
            if not stripped:
                return False
            return len(stripped.split()) <= 3 and len(stripped) <= 40

        def _is_noise_line(line: str) -> bool:
            stripped = line.strip()
            if not stripped:
                return False
            if _META_RE.search(stripped):
                return True
            if re.fullmatch(r'\s*(Fig\.?\s*|Figure|Table)\s+\d+[.:\s\-].{0,50}', stripped, re.IGNORECASE):
                return True
            if re.fullmatch(r'\s*https?://\S+\s*', stripped):
                return True
            if len(stripped) < 10 and re.fullmatch(r'[\d\s]+', stripped):
                return True
            if len(stripped) < 10 and re.fullmatch(r'\s*\[\d+(?:,\d+)*\]\s*', stripped):
                return True
            return False

        lines = text.split('\n')

        # ── 标记图表残片区域 ──
        # 连续 ≥3 行短碎片 → 标记为图表区域，整块移除
        DIAGRAM_MIN_RUN = 3
        diagram_mask = [False] * len(lines)
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped and _is_short_fragment(lines[i]) and not _is_noise_line(lines[i]):
                run_start = i
                while i < len(lines) and _is_short_fragment(lines[i]):
                    i += 1
                run_len = i - run_start
                if run_len >= DIAGRAM_MIN_RUN:
                    for j in range(run_start, i):
                        diagram_mask[j] = True
            else:
                i += 1

        kept = []
        for idx, line in enumerate(lines):
            if diagram_mask[idx]:
                continue
            if _is_noise_line(line):
                continue
            kept.append(line)

        return '\n'.join(kept)

    def _split_to_sentences(self, text: str) -> list[str]:
        """按句号、英文句点后接大写/CJK 字符切分句子"""
        raw = re.split(r'(?<=[。.?!])\s*(?=[A-Z一-鿿])', text)
        result = []
        for s in raw:
            s = s.strip()
            if not s:
                continue
            if re.fullmatch(r'[\s\W_]+', s):
                continue
            result.append(s)
        return result

    def _pack_sentences_to_chunks(
        self,
        sentences: list[str],
        max_tokens: int,
        overlap_tokens: int,
        parent_meta: dict,
        section_char_start: int,
        char_to_page: list[tuple[int, int]],
    ) -> list[Document]:
        """句子贪心打包：累计 token ≤ max_tokens 则继续，超过则新建 chunk，相邻 chunk 共享 overlap_tokens 重叠。"""
        chunks: list[Document] = []
        if not sentences:
            return chunks

        # sentence → char offset 映射
        sent_offsets: dict[int, int] = {}
        cum_offset = 0
        full_text = " ".join(sentences)
        for i, s in enumerate(sentences):
            idx = full_text.find(s, cum_offset)
            sent_offsets[i] = idx if idx >= 0 else cum_offset
            cum_offset = sent_offsets[i] + len(s)

        start = 0
        while start < len(sentences):
            chunk_parts: list[str] = []
            chunk_tokens = 0
            end = start
            while end < len(sentences) and chunk_tokens + self._token_count(sentences[end]) <= max_tokens:
                chunk_parts.append(sentences[end])
                chunk_tokens += self._token_count(sentences[end])
                end += 1

            if not chunk_parts:
                # 单句超过 max_tokens，强制打包为自己的 chunk
                chunk_parts = [sentences[start]]
                end = start + 1

            global_start = section_char_start + sent_offsets.get(start, 0)
            chunks.append(self._make_chunk(
                chunk_parts, parent_meta, global_start, char_to_page, len(chunks),
            ))

            if end >= len(sentences):
                break

            # 回溯凑 overlap：从 end 往回退，累计直到 ≥ overlap_tokens，但不得退到 start 或更前
            chunk_start = start
            overlap_accum = 0
            start = end
            while start > chunk_start and overlap_accum < overlap_tokens:
                start -= 1
                overlap_accum += self._token_count(sentences[start])

            if start <= chunk_start:
                start = end  # 凑不够 overlap，尾部自然结束，无重叠

        return chunks

    def _split_section_to_chunks(self, section_doc: Document) -> list[Document]:
        """Section → 去噪 → 切句 → 打包 chunk"""
        skip_sections = chroma_conf.get("skip_sections", [])
        if section_doc.metadata.get("section", "") in skip_sections:
            return []

        meta = section_doc.metadata
        char_page_json = meta.get("_char_page_map", "")
        char_to_page: list[tuple[int, int]] = json.loads(char_page_json) if char_page_json else []
        section_char_start = meta.get("char_start", 0)

        max_tokens = chroma_conf["chunk_size"]
        overlap_tokens = chroma_conf.get("chunk_overlap", 0)

        # 1. 文本去噪
        clean_text = self._clean_section_text(section_doc.page_content)

        # 2. 切句子
        sentences = self._split_to_sentences(clean_text)

        # 3. 句子打包 → chunk
        chunks = self._pack_sentences_to_chunks(
            sentences, max_tokens, overlap_tokens, meta, section_char_start, char_to_page
        )

        # 4. 清理临时字段
        for c in chunks:
            c.metadata.pop("char_start", None)
            c.metadata.pop("char_end", None)
            c.metadata.pop("_char_page_map", None)
            c.metadata["chunk_strategy"] = chroma_conf.get("chunk_strategy", "section_paragraph")

        return chunks

    def _make_chunk(
        self,
        texts: list[str],
        parent_meta: dict,
        global_start: int,
        char_to_page: list[tuple[int, int]],
        chunk_index: int,
    ) -> Document:
        """构造一个 chunk Document"""
        content = "\n\n".join(texts)
        global_end = global_start + len(content)

        meta = {**parent_meta}
        if char_to_page:
            meta["page_start"] = self._find_page_from_map(global_start, char_to_page)
            meta["page_end"] = self._find_page_from_map(max(global_start, global_end - 1), char_to_page)
            raw_id = f"{meta.get('paper_id', '')}:{meta.get('section', 'unknown')}:{global_start}:{global_end}"
            meta["chunk_id"] = hashlib.md5(raw_id.encode()).hexdigest()[:16]

        meta["chunk_index"] = chunk_index
        return Document(page_content=content, metadata=meta)

    def _token_count(self, text: str) -> int:
        """token 计数（tiktoken cl100k_base，SiliconFlow 兼容）"""
        return _tiktoken_count(text)

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        对 PDF 文件使用 DocParser 做结构化解析，TXT 文件保持普通加载
        计算文件的 MD5 做去重
        """

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                parser = DocParser()
                return parser.parse_paper(read_path)

            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            logger.info(f"[加载知识库]▶ {os.path.basename(path)}")
            try:
                section_docs: list[Document] = get_file_documents(path)

                if not section_docs:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                split_documents: list[Document] = []
                for doc in section_docs:
                    chunks = self._split_section_to_chunks(doc)
                    split_documents.extend(chunks)

                if not split_documents:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]  ✅ {os.path.basename(path)} → {len(section_docs)} sections → {len(split_documents)} chunks")
            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue


if __name__ == '__main__':
    vs = VectorStoreService()
    vs.load_document()

    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-" * 20)

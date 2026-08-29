import re
import json
import os
from dataclasses import dataclass
import fitz
from langchain_core.documents import Document
from utils.logger_handler import logger
from rag.paper_metadata import DocumentMeta, DocSection, SECTION_HEADER_PATTERNS


@dataclass
class SectionBoundary:
    section: str
    start_char: int
    end_char: int
    title: str


class DocParser:
    """结构感知的论文 PDF 解析器：页级清洗 → 逐行扫描章节检测 → section-level Document 输出"""

    DOI_RE = re.compile(r"\b10\.\d{4,}/[^\s\"']+")
    YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")

    # ── 页级噪声清洗 ──

    # 高置信度整行噪声模式（仅匹配整行，不做正文内替换）
    NOISE_LINE_PATTERNS: list[re.Pattern] = [
        # arXiv 水印
        re.compile(r'^arXiv:\d+\.\d+', re.IGNORECASE),
        # 版权声明
        re.compile(r'^©\s*\d{4}'),
        re.compile(r'^Copyright\s+©?\s*\d{4}', re.IGNORECASE),
        # ACM ISBN/ISSN
        re.compile(r'^ACM\s+ISBN', re.IGNORECASE),
        re.compile(r'^ISBN[:\s]', re.IGNORECASE),
        re.compile(r'^ISSN[:\s]', re.IGNORECASE),
        # 裸 ISBN-13（978-1-939133-52-6 等）
        re.compile(r'^\d{3}-\d-\d{5,7}-\d{2,4}-\d$'),
        # DOI 孤行 + 通用会议 URL
        re.compile(r'^https?://doi\.org/', re.IGNORECASE),
        re.compile(r'^DOI[:\s]+10\.', re.IGNORECASE),
        re.compile(r'^https?://(?:www\.)?usenix\.org/', re.IGNORECASE),
        re.compile(r'^https?://(?:dl\.)?acm\.org/', re.IGNORECASE),
        re.compile(r'^https?://(?:proceedings\.|www\.)?(?:neurips|icml|iclr|aaai|acl|emnlp)\.', re.IGNORECASE),
        # License / Open Access
        re.compile(r'^(This\s+work\s+is\s+)?licensed\s+under', re.IGNORECASE),
        re.compile(r'^Creative\s+Commons\s+Attribution', re.IGNORECASE),
        re.compile(r'^(This\s+is\s+an?\s+)?Open\s+access\s+to\s+the\s+Proceedings', re.IGNORECASE),
        # USENIX 前置声明
        re.compile(r'^This\s+paper\s+is\s+included\s+in\s+the\s+Proceedings\s+of', re.IGNORECASE),
        re.compile(r'^is\s+sponsored\s+by\s+USENIX', re.IGNORECASE),
        # 投稿状态声明
        re.compile(r'^(Preprint|Under\s+review|Accepted\s+by|Published\s+as|Camera\s+Ready)', re.IGNORECASE),
        re.compile(r'^All\s+rights?\s+reserved', re.IGNORECASE),
        # IEEE 版权横幅 / 会议头
        re.compile(r'^\d{4} IEEE(?:/ACM)? \d+(?:st|nd|rd|th) International Conference', re.IGNORECASE),
        re.compile(r'^\d{4}\-\d{4}/\d{2}/\$\d{2}\.\d{2} ©\d{4} IEEE', re.IGNORECASE),
        # IEEE 下载声明
        re.compile(r'^Authorized licensed use limited to', re.IGNORECASE),
        re.compile(r'^Downloaded on .+ from IEEE Xplore', re.IGNORECASE),
        # 会议/研讨会页眉（如 "31st USENIX Security Symposium"）
        re.compile(r'^\d{1,2}(?:st|nd|rd|th)\s.{5,80}(?:Symposium|Conference|Workshop)', re.IGNORECASE),
        # 组织名称孤行（如 "USENIX Association"）
        re.compile(r'^(?:The\s+)?USENIX\s+Association', re.IGNORECASE),
        # 顶级会议名称孤行（不含实质内容，仅会议头）
        re.compile(
            r"^(?:(?:Annual\s+)?(?:USENIX|ACM|IEEE|NDSS|SIGCOMM|SIGMOD|WWW|ICSE|FSE|ASE|ISSTA|CCS|S&P|OSDI|SOSP|NSDI|VLDB|AAAI|NeurIPS|ICML|ICLR|CVPR|ICCV|EMNLP|ACL|NAACL|SIGIR|KDD|SIGSOFT|SIGACT|SIGPLAN|SIGOPS|SIGMETRICS|EuroSys|SOSP)\s*(?:'?\d{2})?\s*(?:Conference|Symposium|Workshop|Annual|Proceedings|Technical|Annual\s+Technical\s+Conference))\b",
            re.IGNORECASE,
        ),
        # 会议日期/地点（如 "August 13–15, 2025 • Seattle, WA, USA"）
        re.compile(
            r'^(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}[–—\-]\d{1,2},\s+\d{4}',
            re.IGNORECASE,
        ),
        # 页脚：页码 + 会议名（如 "3828    34th USENIX Security Symposium"）
        re.compile(r'^\d{1,4}\s{2,}\d{1,2}(?:st|nd|rd|th)\s.{5,80}(?:Symposium|Conference|Workshop)', re.IGNORECASE),
        # 孤立页码（纯数字行，1-4 位）—— 放在最后，避免误删正文编号
        re.compile(r'^\d{1,4}\s*$'),
    ]

    @classmethod
    def clean_page_text(cls, page_text: str) -> str:
        """逐行清洗高置信度噪声，返回清洗后文本"""
        lines = page_text.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                cleaned.append(line)
                continue
            is_noise = False
            for pat in cls.NOISE_LINE_PATTERNS:
                if pat.search(stripped):
                    is_noise = True
                    break
            if not is_noise:
                cleaned.append(line)
        return '\n'.join(cleaned)

    # ── PDF 页面加载 ──

    # 孤立的章节编号模式：用于检测被 PyMuPDF 拆成两行的标题（如 "1\nIntroduction"）
    _BARE_SECTION_NUM_RE = re.compile(r'^\d+(?:\.\d+)*\.?\s*$')

    @classmethod
    def _merge_split_section_headers(cls, block_text: str) -> str:
        """合并块内被拆分的章节标题。'1\\nIntroduction' → '1 Introduction'"""
        lines = block_text.split('\n')
        if len(lines) < 2:
            return block_text

        merged = []
        skip_next = False
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            stripped = line.strip()
            if i + 1 < len(lines) and cls._BARE_SECTION_NUM_RE.match(stripped):
                next_line = lines[i + 1].strip()
                # 下一行是短标题（≤8 词，首字母大写或全大写）
                words = next_line.split()
                if words and 1 <= len(words) <= 8:
                    first_w = words[0]
                    if first_w[0].isupper() or next_line.isupper():
                        merged.append(stripped + " " + next_line)
                        skip_next = True
                        continue
            merged.append(line)
        return '\n'.join(merged)

    @classmethod
    def _dehyphenate_block(cls, block_text: str) -> str:
        """合并行间断词连字符。'experi-\\nment' → 'experiment'。

        仅当 - 前小写片段 ≥ 3 字符且下行首字母小写时合并，
        避免 'state-of-\\nthe-art'（of 仅 2 字符）误合并。
        链式合并：若合并结果仍以断词结尾，继续与后续行合并。
        """
        lines = block_text.split('\n')
        if len(lines) < 2:
            return block_text

        merged = []
        i = 0
        while i < len(lines):
            cur = lines[i]
            # 链式合并：只要当前行以断词结尾且下一行首字母小写，就继续吞并
            while i + 1 < len(lines):
                m = re.match(r'^(.*?)([a-zA-Z]{2,}[a-z][a-zA-Z]*)-\s*$', cur)
                if not m:
                    break
                next_line = lines[i + 1]
                if not (next_line and next_line[0].islower()):
                    break
                cur = m.group(1) + m.group(2) + next_line.strip()
                i += 1
            merged.append(cur)
            i += 1
        return '\n'.join(merged)

    @classmethod
    def _load_pages_with_pymupdf(cls, pdf_path: str) -> list[Document]:
        """使用 PyMuPDF 按分栏阅读顺序提取页面文本。

        每页：先左栏（按 y0 排序）→ 再右栏（按 y0 排序）。
        块内预处理：合并孤立的章节编号与标题行（"1\\nIntroduction" → "1 Introduction"）。
        """
        fitz_doc = fitz.open(pdf_path)
        documents = []

        for i, page in enumerate(fitz_doc):
            blocks = page.get_text("blocks")
            text_blocks = [
                (b[0], b[1], b[4].strip())
                for b in blocks if b[6] == 0 and b[4].strip()
            ]

            if not text_blocks:
                documents.append(Document(
                    page_content="",
                    metadata={"page": i, "source": pdf_path}
                ))
                continue

            # 检测分栏
            x0_vals = sorted({b[0] for b in text_blocks})
            mid_x = (min(x0_vals) + max(x0_vals)) / 2

            left_blocks = [b for b in text_blocks if b[0] < mid_x]
            right_blocks = [b for b in text_blocks if b[0] >= mid_x]

            # 单栏回退
            right_ratio = len(right_blocks) / max(len(text_blocks), 1)
            if right_ratio < 0.15:
                text = page.get_text("text", sort=True)
                documents.append(Document(
                    page_content=text,
                    metadata={"page": i, "source": pdf_path}
                ))
                continue

            # 双栏：先左后右，栏内按 y0 排序
            left_blocks.sort(key=lambda b: b[1])
            right_blocks.sort(key=lambda b: b[1])

            # 预处理：合并章节标题（per-block），断词连字符（跨 block，在拼接后做）
            col_texts = []
            for col_blocks in (left_blocks, right_blocks):
                merged_blocks = [
                    cls._merge_split_section_headers(b[2]) for b in col_blocks
                ]
                col_text = "\n".join(merged_blocks)
                col_text = cls._dehyphenate_block(col_text)  # 跨 block 断词合并
                col_texts.append(col_text)

            text = col_texts[0] + "\n" + col_texts[1]
            documents.append(Document(
                page_content=text,
                metadata={"page": i, "source": pdf_path}
            ))

        fitz_doc.close()
        return documents

    # ── 主流程 ──

    def parse_paper(self, pdf_path: str) -> list[Document]:
        """主流程：PyMuPDF 逐页读取 → 页级清洗 → 拼接全文 → 逐行扫描检测章节 → 输出 section-level Document"""
        raw_docs = self._load_pages_with_pymupdf(pdf_path)

        if not raw_docs:
            logger.warning(f"[DocParser]{pdf_path} 没有提取到任何页面内容")
            return []

        # 逐页清洗
        cleaned_docs = []
        for doc in raw_docs:
            cleaned_text = self.clean_page_text(doc.page_content)
            cleaned_docs.append(Document(page_content=cleaned_text, metadata=doc.metadata))

        full_text = "\n".join(d.page_content for d in cleaned_docs)

        # 用清洗后的 pages 重建 char_to_page
        char_to_page = self._build_char_page_map(cleaned_docs)

        paper_meta = self.extract_metadata(pdf_path, raw_docs, full_text)
        boundaries = self.detect_sections(full_text)
        documents = self._build_section_documents(
            full_text, boundaries, char_to_page, paper_meta
        )

        section_names = " → ".join(
            f"[{d.metadata.get('section','?')}]{d.metadata.get('section_title','?')[:40]}"
            for d in documents
        )
        logger.info(
            f"[DocParser]《{paper_meta.paper_title}》解析完成："
            f"{len(boundaries)} 个章节，{len(documents)} 个 section Document"
        )
        logger.info(f"  章节序列: {section_names}")
        return documents

    # ── PyPDF 字母间空格归一化 ──

    # 大空白间隙阈值：用于检测 PyMuPDF sort=True 下同一行内的分栏边界
    COLUMN_GAP_THRESHOLD = 20  # 20 个连续空格/tab 视为分栏边界

    @classmethod
    def _split_column_line(cls, line: str) -> list[str]:
        """在超大空白间隙处拆分一行，分离分栏内容。返回按左→右排列的子行列表。"""
        parts = re.split(r'\s{' + str(cls.COLUMN_GAP_THRESHOLD) + r',}', line)
        return [p.strip() for p in parts if p.strip()]

    @classmethod
    def _normalize_spaced_line(cls, line: str) -> str:
        """压缩 PyPDF 字母间空格，仅用于匹配，不改 full_text。
        'A P P E N D I X' → 'APPENDIX'，'S UPPLEMENTARY' → 'SUPPLEMENTARY'"""
        result = line

        # Step 1: 移除孤立大写字母间的单空格（词内 artifact）
        # 两侧字母必须都是 isolated single letter（位于词边界），防止跨词误合并
        result = re.sub(r'(?<=\b[A-Z])\s(?=[A-Z]\b)', '', result)

        # Step 2: 合并孤立首字母到后续多字符大写词
        # "S UPPLEMENTARY" → "SUPPLEMENTARY", "A PPENDIX" → "APPENDIX"
        result = re.sub(r'\b([A-Z])\s+([A-Z][A-Za-z]+)', r'\1\2', result)

        # Step 3: 压缩残留多空格为单空格
        result = re.sub(r'\s{2,}', ' ', result)

        return result.strip()

    # ── 逐行扫描章节检测 ──

    def detect_sections(self, text: str) -> list[SectionBoundary]:
        """两遍扫描：第一遍匹配已知 section headers，第二遍（References 之后）检测附录"""
        boundaries: list[SectionBoundary] = []
        lines = text.split('\n')
        char_cursor = 0

        # 预计算每行的起始 char 偏移
        line_offsets: list[int] = []
        for line in lines:
            line_offsets.append(char_cursor)
            char_cursor += len(line) + 1  # +1 for \n

        ref_boundary: SectionBoundary | None = None

        # ── 第一遍：标准章节检测 ──
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue

            # 分栏拆分：PyMuPDF sort=True 会将左右栏内容放在同一行，中间用大空白隔开
            # 章节标题始终在左栏 → 只取第一个子行匹配
            column_parts = self._split_column_line(stripped)
            candidate = column_parts[0] if column_parts else stripped

            # PyPDF 失真修复后再匹配（I NTRODUCTION → INTRODUCTION）
            normalized = self._normalize_spaced_line(candidate).lower()

            # 收集所有匹配，选 header 文本最长的（更具体）
            best_match: tuple[int, str, str] | None = None  # (len, section_type, header)
            for section_type, headers in SECTION_HEADER_PATTERNS.items():
                for header in headers:
                    h = header.lower()
                    # 前缀支持阿拉伯数字（1., 2.1.）和罗马数字（I., II., IX.）
                    pattern = (
                        r'^(?:'
                        r'(?:\d+(?:\.\d+)*\.?\s+)'
                        r'|'
                        r'(?:[ivx]+\.\s+)'
                        r')?'
                        + re.escape(h)
                        + r'(?:\s+.*)?\s*:?\s*$'
                    )
                    m = re.match(pattern, normalized)
                    # Fallback: 去除所有空格后匹配，处理 PyPDF 字母间空格残留
                    # （如 "E VA L U AT I O N" → nospace 后 "evaluation" 可匹配到）
                    no_space_fallback = False
                    if not m:
                        h_nospace = h.replace(' ', '')
                        nnp = re.sub(r'\s+', '', normalized)
                        # 前缀中的 \s+ 改为 \s* 以适配无空格文本
                        prefix_ns = r'^(?:(?:\d+(?:\.\d+)*\.?\s*)|(?:[ivx]+\.\s*))?'
                        pattern_nospace = prefix_ns + re.escape(h_nospace) + r'\s*:?\s*$'
                        m = re.match(pattern_nospace, nnp)
                        no_space_fallback = True
                    if m:
                        if no_space_fallback:
                            # nospace 匹配高度特定，直接接受，不做延续 guard
                            if best_match is None or len(h) > best_match[0]:
                                best_match = (len(h), section_type, header)
                            continue
                        # 标题延续 vs 句子：检查 header 后的文本是否为标题延续
                        header_start = normalized.rfind(h)
                        continuation = normalized[header_start + len(h):].strip()
                        rejected = False
                        if continuation:
                            words = continuation.split()
                            first_word = words[0]

                            title_connectors = {
                                'and', 'or', 'of', 'for', 'to', 'in', 'with', 'on',
                                '&', ',', 'the', 'a', 'an', '–', '—', '-',
                                'using', 'via', 'based', 'from', 'over', 'into',
                            }

                            # Guard 1: 首词以非字母开头 → 引用/编号残片（& 除外，是标题连接词）
                            if not first_word[0].isalpha() and first_word != "&":
                                rejected = True
                            # Guard 2: 包含年份 → 参考文献条目
                            elif re.search(r'\b(19|20)\d{2}\b', continuation):
                                rejected = True
                            # Guard 3: 延续部分仅有连接词，无实义词
                            elif not [
                                w for w in words
                                if w.lower().rstrip('.,;:') not in title_connectors
                            ]:
                                rejected = True
                            # Guard 4: 首词为小写非连接词 → 句子
                            elif first_word[0].islower() and first_word not in title_connectors:
                                # 允许 PyPDF 合并的「连接词+实义词」如 "andproblemstatement"
                                is_merged = any(
                                    first_word.startswith(c) and len(first_word) > len(c)
                                    and first_word[len(c):].isalpha()
                                    for c in title_connectors if len(c) > 1
                                )
                                if not is_merged:
                                    rejected = True
                            # Guard 5: 超过 6 词 → 句子
                            elif len(words) > 6:
                                rejected = True
                            # Guard 6: 包含句中断点（". Word" 或 "? Word"）→ 句子
                            elif re.search(r'[.!?]\s+\w', continuation):
                                rejected = True

                        if not rejected:
                            if best_match is None or len(h) > best_match[0]:
                                best_match = (len(h), section_type, header)

            if best_match is not None:
                _, best_section, best_header = best_match
                # Guard: 短单词标题（method/design/evaluation 等）必须有编号前缀
                # 否则极可能是正文中的词而非章节标题
                PREFIX_FREE_WHITELIST = {
                    'abstract', 'references', 'bibliography',
                    'appendix', 'appendices', 'acknowledgments', 'acknowledgement',
                    '摘要', '参考文献', '附录', '致谢',
                }
                header_words = best_header.split()
                has_prefix = bool(re.match(r'^(?:\d+(?:\.\d+)*\.?\s+)|(?:[ivx]+\.\s+)', normalized))
                if len(header_words) == 1 and not has_prefix and best_header.lower() not in PREFIX_FREE_WHITELIST:
                    best_match = None  # 拒绝无编号前缀的短词标题
            if best_match is not None:
                _, best_section, best_header = best_match
                # 归一化 section_title：使用左栏候选文本（column_parts[0]），而非含右栏残余的整行
                clean_title = self._normalize_spaced_line(candidate)
                b = SectionBoundary(
                    section=best_section,
                    start_char=line_offsets[i],
                    end_char=line_offsets[i] + len(line),
                    title=clean_title,
                )
                boundaries.append(b)
                if best_section == DocSection.REFERENCES:
                    ref_boundary = b

        # ── 1.5 遍：编号回退（捕获关键词未覆盖的编号章节标题） ──
        boundaries = self._numbered_fallback(lines, line_offsets, boundaries)

        # ── 第二遍：附录检测（仅在 References 之后） ──
        if ref_boundary is not None:
            ref_idx = next(
                (i for i, line in enumerate(lines)
                 if line_offsets[i] >= ref_boundary.start_char), 0
            )

            for i in range(ref_idx + 1, len(lines)):
                line = lines[i]
                stripped = line.strip()
                if not stripped:
                    continue

                normalized = self._normalize_spaced_line(stripped)
                normalized_lower = normalized.lower()

                # 显式附录：归一化后匹配 appendix 词条
                app_boundary = self._match_appendix_boundary(
                    normalized, normalized_lower, line, lines, i, line_offsets
                )
                if app_boundary is not None:
                    boundaries.append(app_boundary)
                    continue

                # 隐式附录：单大写字母章节标题（仅在 References 之后，非 References 之前不启用）
                if self._is_implicit_appendix_heading(normalized, normalized_lower):
                    b = SectionBoundary(
                        section=DocSection.APPENDIX,
                        start_char=line_offsets[i],
                        end_char=line_offsets[i] + len(line),
                        title=line.strip(),
                    )
                    boundaries.append(b)

        boundaries.sort(key=lambda b: b.start_char)
        boundaries = self._deduplicate_boundaries(boundaries)

        logger.debug(
            f"[DocParser]检测到{len(boundaries)}个章节边界："
            f"{[b.title for b in boundaries]}"
        )
        return boundaries

    # ── 附录检测辅助 ──

    @classmethod
    def _match_appendix_boundary(
        cls,
        normalized: str,
        normalized_lower: str,
        original_line: str,
        lines: list[str],
        line_idx: int,
        line_offsets: list[int],
    ) -> SectionBoundary | None:
        """检测显式附录标题，支持标题延续行合并到 section_title"""
        app_headers = [h.lower() for h in SECTION_HEADER_PATTERNS.get(DocSection.APPENDIX, [])]
        match_title = None
        for ah in app_headers:
            pat = r'^(?:\d+(?:\.\d+)*\.?\s+)?' + re.escape(ah) + r'(?:\s+.*)?\s*:?\s*$'
            if re.match(pat, normalized_lower):
                match_title = original_line.strip()
                break

        if match_title is None:
            return None

        # 尝试合并标题延续行（如 "S UPPLEMENTARY R ESULTS AND D ISCUSSION"）
        if line_idx + 1 < len(lines):
            next_line = lines[line_idx + 1].strip()
            if next_line and cls._is_title_continuation(next_line):
                next_normalized = cls._normalize_spaced_line(next_line)
                if next_normalized.upper() == next_normalized and len(next_normalized) > 3:
                    match_title = match_title + " — " + next_normalized

        return SectionBoundary(
            section=DocSection.APPENDIX,
            start_char=line_offsets[line_idx],
            end_char=line_offsets[line_idx] + len(original_line),
            title=match_title,
        )

    @staticmethod
    def _is_title_continuation(line: str) -> bool:
        """判断一行是否为前一行的标题延续（全大写或近乎全大写）"""
        stripped = line.strip()
        if not stripped:
            return False
        alpha = [c for c in stripped if c.isalpha()]
        if not alpha:
            return False
        return sum(1 for c in alpha if c.isupper()) / len(alpha) > 0.7

    @staticmethod
    def _is_implicit_appendix_heading(normalized: str, normalized_lower: str) -> bool:
        """检测隐式附录标题（如 'A Processing Time'），带防误判 guards"""
        # 只匹配单大写字母 + 空格 + ≥3 字母单词
        m = re.match(r'^([A-H])\s+([A-Za-z].*)$', normalized)
        if not m:
            return False

        rest = m.group(2)

        # 长度限制
        if len(normalized) > 100:
            return False

        # 后续词必须超过 60% 以大写开头（过滤 "A system for design..." 等参考文献条目）
        words = [w for w in rest.split() if w[0].isalpha()]
        if words:
            caps_ratio = sum(1 for w in words if w[0].isupper()) / len(words)
            if caps_ratio < 0.6:
                return False

        # 不以引用编号 / 列表序号开头
        if re.match(r'^\[\d+\]', normalized_lower):
            return False
        if re.match(r'^\d+\.\s', normalized_lower):
            return False

        # 不包含 URL/DOI/arXiv
        if any(kw in normalized_lower for kw in ('doi', 'http', 'arxiv')):
            return False

        # 不包含明显年份（19xx 或 20xx）
        if re.search(r'\b(19|20)\d{2}\b', normalized):
            return False

        # 行尾不是句号
        if normalized.rstrip().endswith('.'):
            return False

        # 逗号不超过 2 个（防长列举句）
        if normalized.count(',') > 2:
            return False

        return True

    # ── 编号回退检测 ──

    # 章节类型排序（用于位置推断）
    _SECTION_ORDER: list[str] = [
        DocSection.ABSTRACT, DocSection.INTRODUCTION,
        DocSection.RELATED_WORK, DocSection.METHOD,
        DocSection.EXPERIMENT, DocSection.RESULTS,
        DocSection.DISCUSSION, DocSection.CONCLUSION,
        DocSection.ACKNOWLEDGMENT, DocSection.REFERENCES,
        DocSection.APPENDIX,
    ]

    def _classify_numbered_section(
        self, char_pos: int, boundaries: list[SectionBoundary]
    ) -> str:
        """根据位置推断编号章节的类型"""
        # 找前后最近的已知章节
        prev_type = DocSection.ABSTRACT
        next_type = DocSection.REFERENCES
        for b in boundaries:
            if b.start_char < char_pos:
                prev_type = b.section
            if b.start_char > char_pos and next_type == DocSection.REFERENCES:
                next_type = b.section

        prev_idx = self._SECTION_ORDER.index(prev_type) if prev_type in self._SECTION_ORDER else 1
        next_idx = self._SECTION_ORDER.index(next_type) if next_type in self._SECTION_ORDER else 9

        # 优先按前驱分类
        if prev_type in (DocSection.ABSTRACT, DocSection.INTRODUCTION):
            return DocSection.RELATED_WORK
        if prev_type == DocSection.RELATED_WORK:
            return DocSection.METHOD
        if prev_type == DocSection.METHOD:
            if next_type in (DocSection.EXPERIMENT, DocSection.RESULTS):
                return DocSection.METHOD
            return DocSection.METHOD
        if prev_type == DocSection.EXPERIMENT:
            return DocSection.RESULTS
        if prev_type == DocSection.RESULTS:
            return DocSection.DISCUSSION
        if prev_type == DocSection.DISCUSSION:
            if next_type in (DocSection.REFERENCES, DocSection.APPENDIX):
                return DocSection.CONCLUSION
            return DocSection.DISCUSSION
        if prev_type == DocSection.CONCLUSION:
            return DocSection.ACKNOWLEDGMENT
        if prev_type == DocSection.REFERENCES:
            return DocSection.APPENDIX

        return DocSection.UNKNOWN

    def _numbered_fallback(
        self, lines: list[str], line_offsets: list[int],
        boundaries: list[SectionBoundary],
    ) -> list[SectionBoundary]:
        """捕获带章节编号但关键词未匹配的行，按位置启发式归类"""
        # 已被匹配覆盖的行索引集合
        covered: set[int] = set()
        for b in boundaries:
            for i, off in enumerate(line_offsets):
                if b.start_char <= off < b.end_char:
                    covered.add(i)

        fallback: list[SectionBoundary] = []
        for i, line in enumerate(lines):
            if i in covered:
                continue
            stripped = line.strip()
            if not stripped or len(stripped) > 120:
                continue

            # 必须有阿拉伯数字或罗马数字编号前缀，且后续以大写字母开头
            m = re.match(r'^(\d+(?:\.\d+)*\.?)\s+([A-Z][^\n]{2,100})$', stripped)
            if not m:
                m = re.match(r'^([IVX]+\.)\s+([A-Z][^\n]{2,100})$', stripped)
            if not m:
                continue

            num_prefix = m.group(1)
            title_text = m.group(2).strip().rstrip('.:')

            # Guard: 编号为 0 → 非章节
            if re.match(r'^0(?:\.0)*\.?$', num_prefix):
                continue

            # Guard: 标题仅 1 个词 → 非章节（如 "0 Low", "3 Glow"）
            if len(title_text.split()) <= 1:
                continue

            # Guard: 含引用标号 [digits] → 表格/参考文献条目
            if re.search(r'\[\d+(?:,\d+)*\]', title_text):
                continue

            # Guard: 含年份
            if re.search(r'\b(19|20)\d{2}\b', stripped):
                continue

            # Guard: 含句末标点后接空格+大写 → 句子
            if re.search(r'[.!?]\s+\w', title_text):
                continue

            # Guard: 含 URL/DOI
            if re.search(r'https?://|doi\.org', stripped, re.IGNORECASE):
                continue

            # Guard: 标题词数 > 10 → 长句
            if len(title_text.split()) > 10:
                continue

            # Guard: 含括号数字（如 "2 Output (2x2x1)"）→ 图/表标题
            if re.search(r'\([\d\s+x*\-/]+\)', title_text):
                continue

            # Guard: 算法伪代码符号 → 非章节
            if re.search(r'[←∅]|//\s|argmax|argmin|\bCONest\b', stripped):
                continue

            # Guard: 含代码语法 → 非章节
            if re.search(r';(?:\s|$)|=\s*\w+\s*\(|\(\s*\w+\s*,', stripped):
                continue
            # 简单赋值语句（= True/False/NULL/数字）
            if re.search(r'=\s*(?:True|False|NULL|null|None)\b', stripped):
                continue
            # 含点号成员访问 + 赋值（Pi.inv = True, obj.prop = val）
            if re.search(r'\w+\.\w+\s*=', stripped):
                continue

            # Guard: "Function" / "Procedure" 关键字 → 伪代码
            if re.search(r'\b(Function|Procedure)\b', stripped, re.IGNORECASE):
                continue

            # Guard: 编号前缀数值范围校验（阿拉伯数字：首数字 0 或 > 30 则非章节；罗马数字：> 20 则非章节）
            if re.match(r'^\d', num_prefix):
                parts = num_prefix.rstrip('.').split('.')
                first_num = int(parts[0])
                if first_num == 0 or first_num > 30:
                    continue
                # 子编号校验：每个子编号必须是 ≤ 20 的整数，且不含前导零
                bad_sub = False
                for p in parts[1:]:
                    if p == '0' or re.match(r'^0\d', p) or int(p) > 20:
                        bad_sub = True
                        break
                if bad_sub:
                    continue
            else:
                roman_val = {'i': 1, 'v': 5, 'x': 10}
                rn = num_prefix.lower().rstrip('.')
                if len(rn) > 4:
                    continue

            # Guard: 标题过短（< 5 字符）→ 残余/噪音
            if len(title_text) < 5:
                continue

            # Guard: 第二词及之后不能全是小写
            twords = title_text.split()
            if len(twords) >= 3:
                caps = sum(1 for w in twords if w[0].isupper())
                if caps < len(twords) * 0.4:
                    continue

            # Guard: 不在已知边界 30 字符范围内
            too_close = False
            for b in boundaries + fallback:
                if abs(line_offsets[i] - b.start_char) < 30:
                    too_close = True
                    break
            if too_close:
                continue

            section_type = self._classify_numbered_section(line_offsets[i], boundaries)
            fb = SectionBoundary(
                section=section_type,
                start_char=line_offsets[i],
                end_char=line_offsets[i] + len(line),
                title=stripped,
            )
            fallback.append(fb)

        return boundaries + fallback

    def _deduplicate_boundaries(self, boundaries: list[SectionBoundary]) -> list[SectionBoundary]:
        """合并 20 字符内的重复边界，保留更长标题"""
        if not boundaries:
            return []
        result = [boundaries[0]]
        for b in boundaries[1:]:
            last = result[-1]
            if b.start_char - last.start_char < 20:
                if len(b.title) > len(last.title):
                    result[-1] = b
                continue
            result.append(b)
        return result

    # ── 元数据提取 ──

    def extract_metadata(
        self, pdf_path: str, raw_docs: list[Document], full_text: str
    ) -> DocumentMeta:
        """从 PDF 内容和文件名提取论文元数据"""
        meta = DocumentMeta()
        meta.source_file = os.path.basename(pdf_path)

        basename = os.path.splitext(os.path.basename(pdf_path))[0]
        meta.paper_title = basename.replace("_", " ").replace("-", " ").replace("+", " ").strip()

        if raw_docs and hasattr(raw_docs[0], "metadata"):
            pdf_meta = raw_docs[0].metadata
            if pdf_meta.get("title") and pdf_meta["title"].strip():
                meta.paper_title = pdf_meta["title"].strip().replace("+", " ")
            if pdf_meta.get("Author"):
                meta.authors = [a.strip() for a in pdf_meta["Author"].split(";")]

        doi_match = self.DOI_RE.search(full_text[:2000])
        if doi_match:
            meta.doi = doi_match.group()

        year_matches = self.YEAR_RE.findall(full_text[:1000])
        if year_matches:
            years = [int(y) for y in year_matches if 1990 <= int(y) <= 2026]
            if years:
                meta.year = years[0]

        meta.paper_id = meta.doi if meta.doi else basename
        return meta

    # ── Section Document 构建 ──

    def _build_section_documents(
        self,
        full_text: str,
        boundaries: list[SectionBoundary],
        char_to_page: list[tuple[int, int]],
        paper_meta: DocumentMeta,
    ) -> list[Document]:
        """按章节边界生成 section-level Document"""
        char_page_json = json.dumps(char_to_page, ensure_ascii=False)
        documents: list[Document] = []

        # 检测是否存在 Abstract section
        abstract_boundary = None
        for b in boundaries:
            if b.section == DocSection.ABSTRACT:
                abstract_boundary = b
                break

        # 前导区（first boundary 之前的内容）
        if boundaries and boundaries[0].start_char > 0:
            preamble = full_text[:boundaries[0].start_char].strip()
            if len(preamble) > 50:
                if abstract_boundary is not None and boundaries[0] is abstract_boundary:
                    # preamble 紧接 Abstract → 合并到 Abstract 内容中（不单独建 section）
                    # 把 preamble 内容追加到 Abstract section 的 text 中
                    # 由后续循环处理，这里跳过 preamble
                    pass
                else:
                    # 无 Abstract 或首 section 不是 Abstract → 单独建 preamble section
                    doc = self._make_section_doc(
                        preamble, DocSection.ABSTRACT, "Abstract/摘要",
                        0, boundaries[0].start_char, char_to_page, paper_meta, char_page_json,
                    )
                    documents.append(doc)

        # Special handling: if preamble was merged into Abstract, prepend it to Abstract section text
        preamble_merged = False
        if abstract_boundary is not None and boundaries and boundaries[0] is abstract_boundary:
            ab_idx = boundaries.index(abstract_boundary)
            if ab_idx == 0 and boundaries[0].start_char > 0:
                preamble_merged = True

        for i, boundary in enumerate(boundaries):
            global_start = boundary.end_char
            global_end = boundaries[i + 1].start_char if i + 1 < len(boundaries) else len(full_text)
            section_text = full_text[global_start:global_end].strip()

            if boundary is abstract_boundary and preamble_merged:
                preamble = full_text[:boundary.start_char].strip()
                section_text = preamble + "\n\n" + section_text

            if not section_text:
                continue

            doc = self._make_section_doc(
                section_text, boundary.section, boundary.title,
                global_start, global_end, char_to_page, paper_meta, char_page_json,
                section_start_char=boundary.start_char,
                section_index=i,  # 全局章节序号
            )
            documents.append(doc)

        # 无章节边界 → 整篇 unknown
        if not boundaries:
            doc = self._make_section_doc(
                full_text, DocSection.UNKNOWN, "",
                0, len(full_text), char_to_page, paper_meta, char_page_json,
            )
            documents.append(doc)

        return documents

    def _make_section_doc(
        self,
        text: str,
        section: str,
        section_title: str,
        char_start: int,
        char_end: int,
        char_to_page: list[tuple[int, int]],
        paper_meta: DocumentMeta,
        char_page_json: str,
        section_start_char: int = 0,
        section_index: int = 0,
    ) -> Document:
        """构造一个 section-level Document，携带完整元数据"""
        page_start = self._find_page(char_start, char_to_page)
        page_end = self._find_page(max(char_start, char_end - 1), char_to_page)

        meta = DocumentMeta(
            paper_title=paper_meta.paper_title,
            paper_id=paper_meta.paper_id,
            source_file=paper_meta.source_file,
            authors=paper_meta.authors,
            year=paper_meta.year,
            section=section,
            section_title=section_title,
            page_start=page_start,
            page_end=page_end,
            doi=paper_meta.doi,
            keywords=paper_meta.keywords,
        )
        md = meta.to_dict()

        md["char_start"] = char_start
        md["char_end"] = char_end
        md["_char_page_map"] = char_page_json
        md["section_start_char"] = section_start_char
        md["section_index"] = section_index

        return Document(page_content=text, metadata=md)

    # ── 字符偏移 ↔ 页码 ──

    def _build_char_page_map(self, raw_docs: list[Document]) -> list[tuple[int, int]]:
        """构建字符偏移→页码映射：[(start_char, page_num), ...]"""
        char_map = []
        offset = 0
        for doc in raw_docs:
            page_num = doc.metadata.get("page", 0) + 1 if doc.metadata else 1
            char_map.append((offset, page_num))
            offset += len(doc.page_content) + 1  # +1 for newline
        return char_map

    def _find_page(self, char_offset: int, char_to_page: list[tuple[int, int]]) -> int:
        """根据字符偏移查找对应页码"""
        page = 1
        for start, page_num in char_to_page:
            if char_offset >= start:
                page = page_num
        return page

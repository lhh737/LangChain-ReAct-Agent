from dataclasses import dataclass, field
from enum import Enum


class DocSection(str, Enum):
    """论文章节类型"""
    ABSTRACT = "abstract"
    INTRODUCTION = "introduction"
    RELATED_WORK = "related_work"
    METHOD = "method"
    EXPERIMENT = "experiment"
    RESULTS = "results"
    DISCUSSION = "discussion"
    CONCLUSION = "conclusion"
    REFERENCES = "references"
    APPENDIX = "appendix"
    ACKNOWLEDGMENT = "acknowledgment"
    UNKNOWN = "unknown"


# 论文章节标题模式
# 优先级：列表内越靠前的模式优先匹配。同一行匹配多个 section 时，选 header 文本最长的（更具体）
PAPER_SECTION_HEADER_PATTERNS: dict[str, list[str]] = {
    DocSection.ABSTRACT: [
        "abstract", "摘要",
    ],
    DocSection.INTRODUCTION: [
        "introduction", "引言", "绪论", "研究背景",
    ],
    DocSection.RELATED_WORK: [
        "related work", "background and related work",
        "相关工作", "related literature", "literature review",
        "文献综述", "previous work", "前人工作",
        "background", "foundation",
        "preliminary", "preliminaries",
    ],
    DocSection.METHOD: [
        "design", "implementation",
        "method", "methods", "methodology", "proposed method", "approach",
        "framework", "system design", "system overview",
        "problem formulation", "problem statement",
        "design overview", "overview",
        "方法", "研究方法", "技术方案", "模型设计", "model architecture",
        "threat model",
        "motivation", "background and motivation",
        "problem definition", "system model", "architecture",
    ],
    DocSection.EXPERIMENT: [
        "experiment", "experiments", "experimental setup", "experimental settings",
        "实验", "实验设置", "实验设计", "implementation details",
        "evaluation setup", "experimental evaluation", "evaluation",
    ],
    DocSection.RESULTS: [
        "results", "experimental results", "result analysis",
        "实验结果", "结果分析", "performance evaluation",
        "evaluation results", "evaluation result",
    ],
    DocSection.DISCUSSION: [
        "discussion", "discussion and limitation", "discussion & limitation",
        "discussion and limitations", "discussion & limitations",
        "讨论", "分析与讨论", "analysis and discussion",
        "limitation", "limitations",
        "related work and discussion", "discussion and related work",
    ],
    DocSection.CONCLUSION: [
        "conclusion", "conclusions", "conclusion and future work",
        "总结", "结论", "结语", "future work", "未来工作",
    ],
    DocSection.REFERENCES: [
        "references", "参考文献", "bibliography",
    ],
    DocSection.APPENDIX: [
        "appendix", "appendices", "附录",
    ],
    DocSection.ACKNOWLEDGMENT: [
        "acknowledgment", "acknowledgements", "acknowledgement",
        "acknowledgments", "致谢",
    ],
}

SECTION_HEADER_PATTERNS: dict[str, list[str]] = PAPER_SECTION_HEADER_PATTERNS


import hashlib


@dataclass
class DocumentMeta:
    """文档结构化元数据，作为 LangChain Document.metadata 存储
    字段名保持 paper_title / paper_id 兼容存量 ChromaDB 索引"""
    paper_title: str = ""         # 文档标题（兼容字段名，可用于培养方案文件名）
    paper_id: str = ""            # 文档唯一标识（兼容字段名）
    source_file: str = ""         # 原始文件名
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    section: str = DocSection.UNKNOWN
    section_title: str = ""       # 章节原标题文本
    page_start: int | None = None
    page_end: int | None = None
    doi: str | None = None
    keywords: list[str] = field(default_factory=list)
    chunk_index: int = 0
    total_chunks: int = 0
    chunk_id: str = ""            # md5(paper_id:section:global_start:global_end)[:16]

    def __post_init__(self):
        pass

    def to_dict(self) -> dict:
        return {
            "paper_title": self.paper_title or "",
            "paper_id": self.paper_id or "",
            "source_file": self.source_file or "",
            "authors": ", ".join(self.authors) if self.authors else "",
            "year": self.year or 0,
            "section": self.section or DocSection.UNKNOWN,
            "section_title": self.section_title or "",
            "page_start": self.page_start or 0,
            "page_end": self.page_end or 0,
            "doi": self.doi or "",
            "keywords": ", ".join(self.keywords) if self.keywords else "",
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "chunk_id": self.chunk_id or "",
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DocumentMeta":
        authors_raw = d.get("authors", "")
        authors = [a.strip() for a in authors_raw.split(",") if a.strip()] if authors_raw else []
        kw_raw = d.get("keywords", "")
        keywords = [k.strip() for k in kw_raw.split(",") if k.strip()] if kw_raw else []
        year = d.get("year")
        if year == 0 or year == "0":
            year = None
        return cls(
            paper_title=d.get("paper_title", ""),
            paper_id=d.get("paper_id", ""),
            source_file=d.get("source_file", ""),
            authors=authors,
            year=year,
            section=d.get("section", DocSection.UNKNOWN),
            section_title=d.get("section_title", ""),
            page_start=d.get("page_start") or None,
            page_end=d.get("page_end") or None,
            doi=d.get("doi") or None,
            keywords=keywords,
            chunk_index=d.get("chunk_index", 0),
            total_chunks=d.get("total_chunks", 0),
            chunk_id=d.get("chunk_id", ""),
        )


# 向后兼容别名
PaperMetadata = DocumentMeta
PaperSection = DocSection
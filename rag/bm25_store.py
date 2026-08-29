import os
import pickle
import jieba
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

# 学术论文领域自定义词典（防止 jieba 错误切分专业术语）
DOMAIN_TERMS = [
    # 论文缩写/方法名
    "PoisonedRAG", "FlippedRAG", "AgentSentinel", "Appatch",
    "FlatD", "MACO", "PatchAgent", "Codellm", "Devkit",
    "BTD", "Bin-to-DNN", "BGE-M3", "BGE-Reranker",
    # 领域术语
    "检索增强生成", "大语言模型", "深度神经网络",
    "逆向工程", "反编译器", "知识窃取", "对抗样本",
    "代码智能", "程序修复", "漏洞检测", "提示工程",
    "思维链", "上下文精度", "上下文召回", "实体召回",
    # 论文章节
    "相关工作", "实验评估", "消融实验", "基准测试",
    "威胁模型", "攻击方法", "安全防御",
]

_terms_added = False


def _add_domain_terms():
    """向 jieba 添加领域术语（全局一次性操作）"""
    global _terms_added
    if _terms_added:
        return
    for term in DOMAIN_TERMS:
        jieba.add_word(term)
    _terms_added = True
    logger.info(f"[BM25]已添加 {len(DOMAIN_TERMS)} 条领域自定义词典")


class BM25Store:
    """BM25 关键词检索引擎，与 Chroma 向量检索并行运行"""

    def __init__(self, index_path: str = "bm25_index.pkl"):
        self.index_path = get_abs_path(index_path)
        self._documents: list[Document] = []
        self._bm25: BM25Okapi | None = None

    def _tokenize(self, text: str) -> list[str]:
        """中英文混合分词"""
        tokens = list(jieba.cut(text))
        # 过滤空白和单字符
        return [t.strip().lower() for t in tokens if t.strip() and len(t.strip()) > 1]

    def build_index(self, documents: list[Document]) -> int:
        """从 Document 列表构建 BM25 索引，返回文档数量"""
        _add_domain_terms()
        if not documents:
            return 0
        self._documents = documents
        tokenized = [self._tokenize(d.page_content) for d in documents]
        self._bm25 = BM25Okapi(tokenized)
        logger.info(f"[BM25]索引构建完成：{len(documents)} 篇文档")
        return len(documents)

    def search(self, query: str, k: int = 5) -> list[tuple[Document, float]]:
        """检索 top-k 文档，返回 [(Document, score), ...]"""
        if not self._bm25 or not self._documents:
            return []
        tokens = self._tokenize(query)
        scores = self._bm25.get_scores(tokens)
        # 取 top-k
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:k]
        # 归一化 score 到 0-1
        max_score = max(scores) if max(scores) > 0 else 1.0
        return [(self._documents[i], s / max_score) for i, s in ranked if s > 0]

    def save(self):
        """持久化索引到磁盘"""
        data = {
            "documents": self._documents,
            "tokenized": [self._tokenize(d.page_content) for d in self._documents] if self._documents else [],
        }
        with open(self.index_path, "wb") as f:
            pickle.dump(data, f)
        logger.info(f"[BM25]索引已保存到 {self.index_path}")

    def load(self) -> bool:
        """从磁盘加载索引，成功返回 True"""
        _add_domain_terms()
        if not os.path.exists(self.index_path):
            return False
        with open(self.index_path, "rb") as f:
            data = pickle.load(f)
        self._documents = data["documents"]
        tokenized = data.get("tokenized", [])
        if tokenized:
            self._bm25 = BM25Okapi(tokenized)
        logger.info(f"[BM25]索引已从 {self.index_path} 加载：{len(self._documents)} 篇文档")
        return True

    def is_built(self) -> bool:
        return self._bm25 is not None and len(self._documents) > 0

    @staticmethod
    def add_domain_terms():
        """公开接口：确保领域词典已加载"""
        _add_domain_terms()

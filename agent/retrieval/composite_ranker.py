"""复合排序器：5种匹配策略取最高分 + 语义匹配"""
import jieba
import numpy as np
from difflib import SequenceMatcher
from agent.retrieval.academic_client import AcademicPaper


class CompositeRanker:
    def __init__(self):
        self.rankers = [
            ExactMatchRanker(),
            SubstringMatchRanker(),
            TokenOverlapRanker(),
            SequenceMatchRanker(),
            ModelNameInTitleRanker(),
        ]

    def _max_score(self, query: str, papers: list[AcademicPaper],
                   rankers: list) -> list[float]:
        """用指定 ranker 列表，对每个 paper 取最高分"""
        query_lower = query.lower().strip()
        scores = []
        for paper in papers:
            best = 0.0
            for ranker in rankers:
                best = max(best, ranker.score(query_lower, paper))
            scores.append(best)
        return scores

    def rank_identity(self, candidate: str, papers: list[AcademicPaper]) -> list[float]:
        """纯身份匹配得分：仅用字符串匹配 ranker，不含语义匹配。
        用于 Stage 1/2 早停判断。"""
        return self._max_score(candidate, papers, self.rankers)

    def rank(self, query: str, papers: list[AcademicPaper]) -> list[tuple[AcademicPaper, float]]:
        """混合排序：字符串匹配 + 语义匹配。用于最终展示排序。"""
        from model.factory import embed_model
        titles = [p.title for p in papers]
        query_emb = np.array(embed_model.embed_query(query))
        title_embs = embed_model.embed_documents(titles)
        semantic_ranker = SemanticMatchRanker(query_emb, dict(zip(titles, title_embs)))

        all_rankers = self.rankers + [semantic_ranker]
        scores = self._max_score(query, papers, all_rankers)

        scored = list(zip(papers, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored


class ExactMatchRanker:
    def score(self, query: str, paper: AcademicPaper) -> float:
        title = paper.title.lower().strip()
        if title == query:
            return 1.0
        # 忽略大小写和空格
        if title.replace(" ", "") == query.replace(" ", ""):
            return 0.95
        return 0.0


class SubstringMatchRanker:
    def score(self, query: str, paper: AcademicPaper) -> float:
        title = paper.title.lower().strip()
        if query in title:
            return 0.7 + 0.3 * (len(query) / max(len(title), 1))
        if title in query:
            return 0.6 + 0.3 * (len(title) / max(len(query), 1))
        return 0.0


class TokenOverlapRanker:
    def score(self, query: str, paper: AcademicPaper) -> float:
        title = paper.title.lower().strip()
        query_tokens = set(jieba.cut(query))
        title_tokens = set(jieba.cut(title))

        if not query_tokens:
            return 0.0

        overlap = query_tokens & title_tokens
        # Jaccard 相似度
        union = query_tokens | title_tokens
        return len(overlap) / len(union) if union else 0.0


class ModelNameInTitleRanker:
    """query 字符串出现在论文标题中 → 固定 0.9 分"""
    def score(self, query: str, paper: AcademicPaper) -> float:
        title = paper.title.lower().strip()
        q = query.lower().strip()
        if q and q in title:
            return 0.90
        return 0.0


class SequenceMatchRanker:
    def score(self, query: str, paper: AcademicPaper) -> float:
        title = paper.title.lower().strip()
        return SequenceMatcher(None, query, title).ratio()


class SemanticMatchRanker:
    """Embedding 余弦相似度 — 解决字符串匹配对自然语言综述查询失效的问题"""
    def __init__(self, query_emb: np.ndarray, title_embs: dict[str, np.ndarray]):
        self.query_emb = query_emb
        self.title_embs = title_embs

    def score(self, query: str, paper: AcademicPaper) -> float:
        emb = self.title_embs.get(paper.title)
        if emb is None:
            return 0.0
        sim = np.dot(self.query_emb, emb) / (
            np.linalg.norm(self.query_emb) * np.linalg.norm(emb) + 1e-8
        )
        return float(sim)

"""研究趋势与主题聚类分析，复用 BGE-M3 Embeddings + K-Means"""

from collections import Counter
from langchain_core.documents import Document
from model.factory import embed_model
from utils.logger_handler import logger


class TopicClusterer:
    """基于 K-Means 的论文学术主题聚类"""

    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters

    def cluster_papers(self, documents: list[Document]) -> dict:
        """对论文 chunk 聚类，返回 {cluster_id: {label, count, papers}}"""
        if len(documents) < self.n_clusters:
            return {"info": f"文档数量({len(documents)})不足，需要至少{self.n_clusters}篇"}

        from sklearn.cluster import KMeans

        texts = [d.page_content for d in documents]
        embeddings = embed_model.embed_documents(texts)

        km = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        labels = km.fit_predict(embeddings)

        clusters: dict[int, dict] = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = {
                    "label": f"主题{label + 1}",
                    "count": 0,
                    "papers": [],
                    "keywords": [],
                }
            clusters[label]["count"] += 1
            clusters[label]["papers"].append(documents[i])

        # 为每个簇生成关键词标签
        for label, info in clusters.items():
            info["keywords"] = self._extract_cluster_keywords(info["papers"])
            info["label"] = ", ".join(info["keywords"][:3]) if info["keywords"] else f"主题{label + 1}"

        logger.info(f"[TopicClusterer]完成{len(clusters)}个簇的聚类")
        return clusters

    def _extract_cluster_keywords(self, docs: list[Document], top_n: int = 5) -> list[str]:
        """提取簇中高频关键词"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        try:
            vectorizer = TfidfVectorizer(max_features=top_n, stop_words="english")
            tfidf = vectorizer.fit_transform([d.page_content for d in docs])
            return vectorizer.get_feature_names_out().tolist()
        except Exception:
            return []

    def get_topic_distribution(self, documents: list[Document]) -> dict:
        """返回各章节的论文分布"""
        section_counter = Counter()
        for d in documents:
            section = d.metadata.get("section", "unknown")
            section_counter[section] += 1
        return dict(section_counter.most_common())


class TrendAnalyzer:
    """年度趋势分析"""

    def analyze(self, documents: list[Document]) -> dict:
        """按年份分组，分析主题演进"""
        year_groups: dict[int, list[Document]] = {}
        for d in documents:
            year = d.metadata.get("year")
            if year is None:
                continue
            if year not in year_groups:
                year_groups[year] = []
            year_groups[year].append(d)

        trends = {
            "year_counts": {y: len(docs) for y, docs in sorted(year_groups.items())},
            "years": sorted(year_groups.keys()),
        }
        return trends


def get_all_documents_from_chroma() -> list[Document]:
    """从 Chroma 获取所有文档（用于聚类分析）"""
    from rag.vector_store import VectorStoreService
    vs = VectorStoreService()
    collection = vs.vector_store._collection
    result = collection.get()
    docs = []
    for i, content in enumerate(result.get("documents", [])):
        meta = result.get("metadatas", [{}])[i] if result.get("metadatas") else {}
        docs.append(Document(page_content=content, metadata=meta))
    return docs

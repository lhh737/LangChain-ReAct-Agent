

"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
import json
import os
import requests
import jieba
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from model.factory import chat_model
from utils.config_handler import chroma_conf
from utils.logger_handler import logger


class RagSummarizeService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self.prompt_template | self.model | StrOutputParser()
        self._bm25_retriever_cache = None   

    def retriever_docs(self, query: str) -> list[Document]:
        """纯向量检索（兼容旧接口）"""
        retriever = self.vector_store.get_retriever()
        return retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        """纯向量检索 + 总结（兼容旧接口）"""
        context_docs = self.retriever_docs(query)
        context = ""
        for i, doc in enumerate(context_docs, 1):
            context += f"【参考资料{i}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"
        return self.chain.invoke({"input": query, "context": context})

    def _get_bm25_retriever(self, k: int):
        """延迟创建并缓存 BM25 检索器（基于向量库中的所有文档）"""
        if self._bm25_retriever_cache is None:
            raw_docs = self.vector_store.vector_store.get(include=["documents", "metadatas"])
            if not raw_docs.get('documents'):
                return None
            docs = [
                Document(page_content=doc, metadata=meta)
                for doc, meta in zip(raw_docs['documents'], raw_docs['metadatas'])
            ]
            def tokenizer(text: str):
                return list(jieba.cut_for_search(text))
            self._bm25_retriever_cache = BM25Retriever.from_documents(
                documents=docs,
                k=k,
                preprocess_func=tokenizer,
                bm25_variant="plus",
            )
        return self._bm25_retriever_cache

    def _compute_dynamic_weights(self, query: str):
        """
        使用 LLM 评估 Top-1 文档的相关性，返回 (weight_vector, weight_bm25)
        如果失败返回 None，调用方将使用默认权重
        """
        bm25_ret = self._get_bm25_retriever(k=1)
        if bm25_ret is None:
            return None

        vector_ret = self.vector_store.vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 1}
        )
        try:
            top_vector = vector_ret.invoke(query)[0]
            top_bm25 = bm25_ret.invoke(query)[0]
        except (IndexError, Exception) as e:
            logger.warning(f"获取 Top-1 文档失败: {e}")
            return None

        judge_prompt = PromptTemplate.from_template("""你是一个检索质量评估专家。用户的问题是：{query}

请判断以下两篇文档中，哪一篇更能有效回答用户问题，并分配权重（两个权重之和为1）。

文档A（来自语义向量检索）：
内容：{doc_a_content}

文档B（来自关键词BM25检索）：
内容：{doc_b_content}

请严格按照以下 JSON 格式输出：
{{"weight_for_doc_A": 0.6, "weight_for_doc_B": 0.4}}
""")
        chain = judge_prompt | self.model | StrOutputParser()
        try:
            resp = chain.invoke({
                "query": query,
                "doc_a_content": top_vector.page_content[:800],
                "doc_b_content": top_bm25.page_content[:800],
            })
            weights = json.loads(resp)
            wa = float(weights.get("weight_for_doc_A", 0.5))
            wb = float(weights.get("weight_for_doc_B", 0.5))
            total = wa + wb
            if total > 0:
                wa, wb = wa / total, wb / total
            logger.info(f"DAT 动态权重计算成功: 向量={wa:.2f}, BM25={wb:.2f}")
            return (wa, wb)
        except Exception as e:
            logger.error(f"动态权重计算失败: {e}")
            return None

    def _rerank_with_qwen(self, query: str, docs: list[Document], top_n: int = 5) -> list[Document]:
        """
        使用阿里云 Qwen3-Rerank 模型对文档进行重排序。
        :return: 按相关性降序排列的 Document 列表
        """
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            logger.warning("未找到 DASHSCOPE_API_KEY，跳过 rerank，返回原始文档")
            return docs

        url = "https://dashscope.aliyuncs.com/compatible-api/v1/reranks"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        documents_texts = [doc.page_content for doc in docs]
        payload = {
            "model": "qwen3-rerank",
            "query": query,
            "documents": documents_texts,
            "top_n": top_n,
            "return_documents": True
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            results = response.json()

            reranked_docs = []
            for result in results.get("results", []):
                index = result.get("index")
                if index is not None and 0 <= index < len(docs):
                    reranked_docs.append(docs[index])
            logger.info(f"Qwen Rerank 完成，输入 {len(docs)} 个文档，输出 {len(reranked_docs)} 个")
            return reranked_docs
        except Exception as e:
            logger.error(f"Qwen Rerank 调用失败: {e}，返回原始文档")
            return docs

    def rag_summarize_with_hybrid(self, query: str, k_initial: int = None,
                                  use_dat: bool = True, use_reranker: bool = True,
                                  reranker_top_n: int = 5) -> str:
        """
        混合检索（向量 + BM25），支持 DAT 动态权重和可选的精排 (Reranker) 阶段。
        
        :param query: 用户问题
        :param k_initial: 初始召回文档数量（粗排阶段），默认使用 chroma.yml 中的 k 值
        :param use_dat: 是否使用 DAT 动态权重（默认 True）
        :param use_reranker: 是否使用 Qwen3-Reranker 进行精排（默认 True）
        :param reranker_top_n: 精排后保留的文档数量（仅在 use_reranker=True 时生效）
        """

        if k_initial is None:
            k_initial = chroma_conf.get("k", 5)


        if use_reranker and k_initial <= reranker_top_n:
            k_initial = max(reranker_top_n * 2, k_initial)


        if use_dat:
            weights = self._compute_dynamic_weights(query)
            if weights is None:
                weights = (0.6, 0.4)
                logger.info(f"使用默认权重: 向量={weights[0]:.2f}, BM25={weights[1]:.2f}")
            else:
                logger.info(f"使用 DAT 动态权重: 向量={weights[0]:.2f}, BM25={weights[1]:.2f}")
        else:
            weights = (0.6, 0.4)
            logger.info(f"固定权重（未启用 DAT）: 向量={weights[0]:.2f}, BM25={weights[1]:.2f}")


        vector_retriever = self.vector_store.vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": k_initial}
        )


        bm25_retriever = self._get_bm25_retriever(k_initial)
        if bm25_retriever is None:

            docs = vector_retriever.invoke(query)
            logger.warning("BM25 检索器不可用，降级为纯向量检索")
        else:
            ensemble = EnsembleRetriever(
                retrievers=[vector_retriever, bm25_retriever],
                weights=[weights[0], weights[1]],
            )
            docs = ensemble.invoke(query)
            if len(docs) > k_initial:
                docs = docs[:k_initial]


        if use_reranker and docs:
            docs = self._rerank_with_qwen(query, docs, top_n=reranker_top_n)
        elif not use_reranker and len(docs) > k_initial:
            docs = docs[:k_initial]  


        context = ""
        for i, doc in enumerate(docs, 1):
            context += f"【参考资料{i}】: {doc.page_content}\n"
        logger.info(f"最终召回 {len(docs)} 个文档，query={query}")
        return self.chain.invoke({"input": query, "context": context})


if __name__ == '__main__':
    rag = RagSummarizeService()
    # 测试：不使用精排
    print(rag.rag_summarize_with_hybrid("扫地机器人有哪些主要功能？", use_reranker=False))
    # 测试：使用精排
    # print(rag.rag_summarize_with_hybrid("扫地机器人有哪些主要功能？", use_reranker=True))
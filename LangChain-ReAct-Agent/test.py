from rag.rag_service import RagSummarizeService

rag = RagSummarizeService()
result = rag.rag_summarize_with_hybrid("扫地机器人有哪些主要功能？")
print(result)

#扫地机器人有哪些主要功能？（RAG 知识库问答）
#如果机器人无法正常回充，该如何处理？（故障排查）
#请根据用户数据生成一份个性化使用报告（报告生成 + 工具调用）

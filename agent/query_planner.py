"""查询规划模块：候选提取、查询改写、在线查询构建。

这些函数通过 LLM 调用完成语义理解和查询生成，均有 I/O 副作用；
不包含可变的跨请求状态，但依赖传入的 chat_model 实例和 online_pipeline 引用。
"""
import re
from typing import Generator

from model.factory import chat_model
from utils.logger_handler import logger


def extract_candidates(query: str) -> list[str]:
    """从用户问题中 LLM 提取论文名、方法名、系统名"""
    prompt = (
        "从以下用户问题中提取所有论文名、方法名、系统名，每行一个。"
        "如果没有明确名称，输出 NONE。\n"
        f"问题：{query}\n输出："
    )
    raw = ""
    for chunk in chat_model.stream(prompt):
        if chunk.content and isinstance(chunk.content, str):
            raw += chunk.content
    candidates = [t.strip() for t in raw.strip().split("\n") if t.strip() and t.strip().upper() != "NONE"]
    logger.info(f"[Candidates] {candidates}")
    return candidates


def extract_compare_aspects(query: str) -> str:
    """从用户对比问题中提取核心对比维度（英文关键词）"""
    prompt = (
        "从以下用户问题中提取所有对比维度，输出对应的英文学术关键词（空格分隔，不超过 8 个词）。\n"
        "如：攻击目标→attack goal target；攻击手段→attack method technique；威胁模型→threat model\n"
        f"问题：{query}\n关键词："
    )
    aspects = ""
    for chunk in chat_model.stream(prompt):
        if chunk.content and isinstance(chunk.content, str):
            aspects += chunk.content
    result = aspects.strip()
    logger.info(f"[CompareAspects] {result}")
    return result


def rewrite_query(query: str) -> str:
    """LLM 改写查询为英文学术检索关键词"""
    prompt = (
        "以下问题在英文学术论文库中检索不到相关内容，请将问题改写为不同的英文学术检索关键词。"
        "只输出改写后的检索词，不要解释。\n"
        f"原问题：{query}\n改写："
    )
    rewritten = ""
    for chunk in chat_model.stream(prompt):
        if chunk.content and isinstance(chunk.content, str):
            rewritten += chunk.content
    return rewritten.strip()


def build_online_query(query: str, subject: str) -> str:
    """从自然语言问句中提取领域关键词，拼成 '论文名 关键词' 格式用于学术检索"""
    if not subject:
        from rag.rag_service import RagSummarizeService
        return RagSummarizeService()._translate_query(query)
    prompt = (
        "从以下研究问题中提取2-3个最核心的英文学术领域关键词（不含论文名/方法名本身），"
        "用空格分隔。只输出关键词，不要解释。\n"
        f"问题：{query}\n关键词："
    )
    keywords = ""
    for chunk in chat_model.stream(prompt):
        if chunk.content and isinstance(chunk.content, str):
            keywords += chunk.content
    keywords = keywords.strip()
    if keywords:
        return f"{subject} {keywords}"
    return subject


def scored_to_papers_meta(result) -> list[dict]:
    """从 OnlineRetrievalResult 获取前端展示用的论文元数据摘要。
    
    替代旧版基于 online_pipeline.get_last_scored() 的实现。
    """
    try:
        return result.papers_meta()
    except Exception:
        return []


def strip_pipeline_numbering(text: str) -> str:
    """清除在线检索输出中的 [N] 编号前缀"""
    return re.sub(r'^\[\d+\]\s*', '', text, flags=re.MULTILINE)

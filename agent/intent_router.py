"""意图分类器 —— 高置信正则优先 + LLM 兜底 + 多意图冲突交给 LLM"""
import re
from enum import Enum
from model.factory import chat_model
from utils.logger_handler import logger


class Intent(str, Enum):
    QA = "qa"
    COMPARE = "compare"
    REVIEW = "review"


class IntentRouter:
    # 高置信 COMPARE：对比词 + 多主体分隔（前瞻断言，双信号同时满足）
    COMPARE_HIGH_CONFIDENCE = re.compile(
        r'(?=.*\b(?:对比|比较|vs\.?|versus|difference|异同|优劣|区别|哪个更好|'
        r'有什么不同|优缺点|对比分析|comparing|comparison|distinguish)\b)'
        r'(?=.*(?:和|与|vs\.?|versus|对标|相较|比起|相对于))',
        re.IGNORECASE,
    )

    # 高置信 REVIEW：密集综述信号（中英文分开，中文不用 \b）
    REVIEW_ZH = re.compile(
        r'(?:综述|研究现状|研究进展|发展脉络|全面了解|领域发展|归纳|梳理|主流方法|总结)'
    )
    REVIEW_EN = re.compile(
        r'\b(?:survey|systematic\s+review|literature\s+review|'
        r'state\s+of\s+the\s+art|comprehensive\s+review|taxonomy'
        r'|overview|literature\s+survey)\b',
        re.IGNORECASE,
    )

    # 排除模式：匹配到 review/survey 但实际是普通 QA
    REVIEW_FALSE_POSITIVE = re.compile(
        r'(?:这篇|这个|该).{0,10}(?:review|survey|综述|概述).{0,10}'
        r'(?:了什么|的内容|讲了|主要|介绍)',
        re.IGNORECASE,
    )

    def __init__(self):
        self._classify_prompt = (
            "将以下用户问题分类为以下三类之一。只回复一个单词：qa、compare 或 review。\n"
            "- qa: 关于特定论文/方法/概念的具体问题\n"
            "- compare: 比较多个方法/模型/论文\n"
            "- review: 全面了解某个研究领域的发展\n"
            "问题：{query}\n分类："
        )

    def classify(self, query: str) -> Intent:
        is_compare = bool(self.COMPARE_HIGH_CONFIDENCE.search(query))
        is_review = (bool(self.REVIEW_ZH.search(query)) or bool(self.REVIEW_EN.search(query))) \
                    and not bool(self.REVIEW_FALSE_POSITIVE.search(query))

        # 单一高置信命中 → 直接返回
        if is_compare and not is_review:
            logger.info(f"[IntentRouter] 高置信规则: compare")
            return Intent.COMPARE
        if is_review and not is_compare:
            logger.info(f"[IntentRouter] 高置信规则: review")
            return Intent.REVIEW

        # 同时命中或都不命中 → LLM 兜底
        logger.info(f"[IntentRouter] 规则歧义(compare={is_compare}, review={is_review})，走 LLM")
        llm_result = self._llm_classify(query)
        if llm_result:
            return llm_result

        # LLM 失败 → 回退关键词
        return self._keyword_classify(query)

    def _llm_classify(self, query: str) -> Intent | None:
        try:
            response = chat_model.invoke(
                self._classify_prompt.format(query=query),
                temperature=0,
                max_tokens=5,
            )
            text = response.content.strip().lower()
            for intent in Intent:
                if intent.value in text:
                    logger.info(f"[IntentRouter] LLM 分类: {intent.value}")
                    return intent
            return None
        except Exception as e:
            logger.warning(f"[IntentRouter] LLM 分类失败: {e}")
            return None

    def _keyword_classify(self, query: str) -> Intent:
        """关键词兜底"""
        query_lower = query.lower()

        COMPARE_KEYWORDS = [
            "vs", "versus", "compare", "comparison", "difference", "diff",
            "对比", "比较", "区别", "异同", "优劣", "哪个更好", "有什么不同",
            "区别是什么", "优缺点", "对比分析",
        ]
        REVIEW_KEYWORDS = [
            "review", "survey", "overview", "literature", "state of the art",
            "综述", "概述", "概览", "发展脉络", "研究现状", "研究进展",
            "总结", "归纳", "梳理", "全面了解", "领域发展", "主流方法",
            "systematic review", "comprehensive", "taxonomy",
        ]

        compare_score = sum(1 for kw in COMPARE_KEYWORDS if kw in query_lower)
        review_score = sum(1 for kw in REVIEW_KEYWORDS if kw in query_lower)

        if compare_score > review_score:
            logger.info(f"[IntentRouter] 关键词: compare (C={compare_score} R={review_score})")
            return Intent.COMPARE
        elif review_score > compare_score:
            logger.info(f"[IntentRouter] 关键词: review (C={compare_score} R={review_score})")
            return Intent.REVIEW
        elif compare_score > 0 and compare_score == review_score:
            logger.info(f"[IntentRouter] 关键词: compare (平局偏好)")
            return Intent.COMPARE
        else:
            logger.info(f"[IntentRouter] 关键词: qa (默认)")
            return Intent.QA

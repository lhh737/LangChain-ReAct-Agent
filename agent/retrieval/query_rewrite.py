"""在线检索查询改写：连字符↔空格、驼峰拆分、大小写变体"""
import re


class RuleBasedRewriter:
    def rewrite(self, query: str) -> list[str]:
        variants: set[str] = {query}

        # 1. 连字符 ↔ 空格
        if "-" in query:
            variants.add(query.replace("-", " "))
        if " " in query:
            variants.add(query.replace(" ", "-"))

        # 2. 驼峰拆分 (CamelCase → Camel Case)
        camel_parts = re.findall(r'[A-Z][a-z]+|[A-Z]+(?=[A-Z][a-z])|[A-Z]+$|[a-z]+', query)
        if len(camel_parts) > 1:
            variants.add(" ".join(camel_parts))

        # 3. 大小写变体
        variants.add(query.lower())
        variants.add(query.upper())
        variants.add(query.title())

        # 限制最多 5 个变体，优先保留原始 query
        result = [query]
        for v in variants:
            if v != query and len(result) < 5:
                result.append(v)

        return result

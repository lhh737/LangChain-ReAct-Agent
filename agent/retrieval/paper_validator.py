"""论文身份验证：多信号并行交叉验证 — 标识符 + 标题 + 作者 + 年份 + 分数"""
import re
import unicodedata
from difflib import SequenceMatcher
from enum import Enum
from agent.retrieval.academic_client import AcademicPaper


class ConfidenceLevel(Enum):
    EXACT = "exact"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PaperIdentityValidator:
    HIGH_THRESHOLD = 0.90
    MEDIUM_THRESHOLD = 0.70

    def validate(self, target: str, paper: AcademicPaper, match_score: float,
                 candidate_type: str = "unknown") -> tuple[ConfidenceLevel, str]:
        title = paper.title
        reasons: list[str] = []

        # ── Tier 1: 全标识符并行精确匹配（不限于 candidate_type）──
        doi_result = self._check_doi_match(target, paper.doi)
        if doi_result:
            return ConfidenceLevel.EXACT, doi_result

        arxiv_result = self._check_arxiv_match(target, paper.arxiv_id)
        if arxiv_result:
            return ConfidenceLevel.EXACT, arxiv_result

        # ── Tier 2: 从 target 提取元数据信号 ──
        target_authors = self._extract_authors(target)
        target_year = self._extract_year(target)

        # ── Tier 3: 标题匹配（含 acronym 字母验证）──
        title_sim = self._compute_title_sim(target, title, candidate_type)
        acronym_ok = False
        if candidate_type == "acronym":
            acronym_ok = self._verify_acronym(self._strip_metadata(target), title)
            if acronym_ok:
                reasons.append("acronym 字母验证通过")

        # ── Tier 4: 作者 + 年份交叉信号 ──
        author_hit = self._check_author_match(target_authors, paper.authors)
        if author_hit:
            reasons.append(f"作者匹配: {author_hit}")

        year_hit = self._check_year_match(target_year, paper.year)
        if year_hit:
            reasons.append(f"年份匹配: target={target_year} paper={paper.year}")

        # ── Tier 5: 多信号共识决策 ──
        # 标题相似度等级
        if candidate_type == "acronym":
            if acronym_ok and title_sim >= 0.90:
                title_level = "exact" if title_sim >= 0.95 else "high"
            elif acronym_ok and title_sim >= 0.5:
                title_level = "medium"
            else:
                title_level = "low"
        elif candidate_type == "full_title":
            if title_sim >= 0.98:
                title_level = "exact"
            elif title_sim >= 0.90:
                title_level = "high"
            elif title_sim >= 0.75:
                title_level = "medium"
            else:
                title_level = "low"
        else:
            # unknown 类型：用 match_score 作为标题信号
            if match_score >= 0.98:
                title_level = "exact"
            elif match_score >= 0.90:
                title_level = "high"
            elif match_score >= 0.70:
                title_level = "medium"
            else:
                title_level = "low"

        # 共识升级：中等标题 + 作者 + 年份 → HIGH
        if title_level == "medium" and author_hit and year_hit:
            return ConfidenceLevel.HIGH, f"多信号共识: 标题中等等同({title_sim:.3f}) + 作者匹配 + 年份匹配 → HIGH | {'; '.join(reasons)}"

        if title_level == "medium" and (author_hit or year_hit):
            return ConfidenceLevel.MEDIUM, f"标题中等等同({title_sim:.3f}) + 部分信号 | {'; '.join(reasons)}"

        # 高标题 + 任一附加信号 → EXACT
        if title_level == "high" and (author_hit or year_hit):
            return ConfidenceLevel.EXACT, f"标题高相似({title_sim:.3f}) + 附加信号确认 | {'; '.join(reasons)}"

        if title_level == "high" and candidate_type == "acronym" and acronym_ok:
            return ConfidenceLevel.EXACT, f"acronym 验证 + 标题前缀匹配 | {'; '.join(reasons)}"

        # 纯标题判断
        if title_level == "exact":
            return ConfidenceLevel.EXACT, f"标题精确匹配 (sim={title_sim:.3f})"
        if title_level == "high":
            return ConfidenceLevel.HIGH, f"标题高相似 (sim={title_sim:.3f})"
        if title_level == "medium":
            return ConfidenceLevel.MEDIUM, f"标题中等相似 (sim={title_sim:.3f})，建议核实"

        # ── Tier 6: 分数兜底 ──
        if match_score >= 0.95:
            return ConfidenceLevel.EXACT, f"分数精确匹配: {title}"
        if match_score >= self.HIGH_THRESHOLD:
            return ConfidenceLevel.HIGH, f"分数高置信度: {title}"
        if match_score >= self.MEDIUM_THRESHOLD:
            return ConfidenceLevel.MEDIUM, f"分数中等置信度: {title}，建议核实论文标题"

        return ConfidenceLevel.LOW, f"低置信度: {title}，检索词与论文标题差异较大"

    # ── Tier 1 helpers: 全标识符检查 ──

    def _check_doi_match(self, target: str, paper_doi: str | None) -> str | None:
        if not paper_doi or not target:
            return None
        norm_target = self._normalize_doi(target)
        norm_paper = self._normalize_doi(paper_doi)
        if norm_target == norm_paper:
            return f"DOI 精确匹配: {paper_doi}"
        if norm_target in norm_paper or norm_paper in norm_target:
            return f"DOI 包含匹配: {paper_doi}"
        return None

    def _check_arxiv_match(self, target: str, paper_arxiv_id: str | None) -> str | None:
        if not paper_arxiv_id or not target:
            return None
        norm_target = self._normalize_arxiv_id(target)
        norm_paper = self._normalize_arxiv_id(paper_arxiv_id)
        if norm_target == norm_paper:
            return f"arXiv ID 精确匹配: {paper_arxiv_id}"
        # 去掉版本号后比较
        norm_target_nov = re.sub(r'v\d+$', '', norm_target)
        norm_paper_nov = re.sub(r'v\d+$', '', norm_paper)
        if norm_target_nov == norm_paper_nov:
            return f"arXiv ID 匹配（忽略版本号）: {paper_arxiv_id}"
        return None

    # ── Tier 2 helpers: 元数据提取 ──

    @staticmethod
    def _extract_authors(target: str) -> list[str]:
        """从 target 中提取作者姓氏。
        支持模式: 'Title (Author1, Author2 et al., 2020)' / 'Title (Author, 2020)'
        """
        if not target:
            return []
        # 匹配末尾括号内容
        m = re.search(r'\(([^)]+)\)\s*$', target)
        if not m:
            return []
        content = m.group(1)
        # 去掉年份部分
        content = re.sub(r',?\s*\d{4}[a-z]?', '', content)
        # 去掉 et al. / etc.
        content = re.sub(r'\bet\s+al\.?', '', content, flags=re.IGNORECASE)
        # 分割作者名
        authors = []
        for part in re.split(r'[,;&]|\band\b', content):
            part = part.strip().strip('.').strip()
            if not part:
                continue
            # 取姓氏（最后一个词）
            surname = part.split()[-1] if part.split() else part
            surname = surname.strip().lower()
            if len(surname) >= 2:
                authors.append(surname)
        return authors

    @staticmethod
    def _extract_year(target: str) -> int | None:
        """从 target 中提取年份（1900-2030 范围）"""
        if not target:
            return None
        # 优先匹配括号内的年份
        m = re.search(r'\([^)]*(\d{4})[^)]*\)\s*$', target)
        if m:
            year = int(m.group(1))
            if 1900 <= year <= 2030:
                return year
        # 匹配任意位置的 4 位数字
        for m in re.finditer(r'\b(\d{4})\b', target):
            year = int(m.group(1))
            if 1900 <= year <= 2030:
                return year
        return None

    # ── Tier 3 helpers: 标题相似度 ──

    @staticmethod
    def _strip_metadata(target: str) -> str:
        """去掉 target 末尾的括号元数据，如 'BERT (Devlin, 2019)' → 'BERT'"""
        return re.sub(r'\s*\([^)]*\)\s*$', '', target).strip()

    def _compute_title_sim(self, target: str, title: str, candidate_type: str) -> float:
        """计算 target 与 paper.title 的归一化相似度"""
        target_clean = self._strip_metadata(target)

        if candidate_type == "acronym":
            token = target_clean.lower().strip()
            prefix = title.lower().split(":")[0].strip()
            if prefix == token:
                return 1.0
            if prefix.startswith(token) and (
                len(prefix) == len(token) or prefix[len(token)] in (" ", ":", "-")
            ):
                return 0.95
            if re.search(rf'\b{re.escape(token)}\b', title.lower()):
                return 0.90
            return 0.0

        if candidate_type == "full_title":
            norm_target = self._normalize_title(target_clean)
            norm_title = self._normalize_title(title)
            return SequenceMatcher(None, norm_target, norm_title).ratio()

        # unknown: try normalized similarity
        norm_target = self._normalize_title(target_clean)
        norm_title = self._normalize_title(title)
        return SequenceMatcher(None, norm_target, norm_title).ratio()

    @staticmethod
    def _verify_acronym(acronym: str, title: str) -> bool:
        """验证 acronym 与 title 的对应关系。
        1. title 前缀（冒号前）== acronym → 直接通过
        2. title 前缀以 acronym 开头 → 直接通过
        3. 字母必须匹配 title 某词首字母；数字可出现在任意词内。>=60% 匹配率通过。
        """
        acronym_clean = acronym.strip().lower()
        if len(acronym_clean) < 2:
            return False

        # 快速路径：title 前缀直接匹配
        prefix = title.lower().split(":")[0].strip()
        if prefix == acronym_clean:
            return True
        if prefix.startswith(acronym_clean) and (
            len(prefix) == len(acronym_clean) or prefix[len(acronym_clean)] in (" ", ":", "-")
        ):
            return True
        if re.search(rf'\b{re.escape(acronym_clean)}\b', title.lower()):
            return True

        # 慢路径：字母 → 首字母匹配
        stop_words = {'a', 'an', 'the', 'for', 'and', 'of', 'in', 'on', 'to',
                      'with', 'by', 'via', 'or', 'is', 'at', 'from', 'its', 'can', 'has'}
        words = [w for w in re.findall(r'[a-z0-9]+', title.lower()) if w not in stop_words]
        if not words:
            return False

        first_letters = set(w[0] for w in words)
        all_chars = set(''.join(words))

        matched = 0
        for ch in acronym_clean:
            if not ch.isalnum():
                continue
            if ch.isalpha() and ch in first_letters:
                matched += 1
            elif ch.isdigit() and ch in all_chars:
                matched += 1

        # 短 acronym 需要更高匹配率
        threshold = 0.75 if len(acronym_clean) <= 4 else 0.6
        return matched >= len(acronym_clean) * threshold

    # ── Tier 4 helpers: 作者 + 年份信号 ──

    @staticmethod
    def _check_author_match(target_authors: list[str], paper_authors: list[str]) -> str | None:
        """检查 target 提取的作者与 paper.authors 是否有交集。
        返回匹配的作者名，或 None。
        """
        if not target_authors or not paper_authors:
            return None
        paper_surnames = set()
        for a in paper_authors:
            parts = a.strip().split()
            if parts:
                paper_surnames.add(parts[-1].strip().lower())
            # 也加全名小写用于包含匹配
            paper_surnames.add(a.strip().lower())

        matched = []
        for ta in target_authors:
            for ps in paper_surnames:
                if ta == ps or ta in ps or ps in ta:
                    matched.append(ta)
                    break

        return ", ".join(matched[:3]) if matched else None

    @staticmethod
    def _check_year_match(target_year: int | None, paper_year) -> bool:
        """年份容差匹配：±1 年"""
        if target_year is None:
            return False
        try:
            py = int(paper_year) if paper_year else None
        except (ValueError, TypeError):
            return False
        if py is None:
            return False
        return abs(target_year - py) <= 1

    # ── 规范化辅助 ──

    @staticmethod
    def _normalize_title(t: str) -> str:
        t = unicodedata.normalize("NFKC", t).casefold()
        return re.sub(r'\s+', ' ', t).strip()

    @staticmethod
    def _normalize_doi(d: str) -> str:
        d = d.strip().lower()
        for prefix in ("https://doi.org/", "http://doi.org/", "doi:", "doi/"):
            if d.startswith(prefix):
                d = d[len(prefix):]
        return d.strip("/")

    @staticmethod
    def _normalize_arxiv_id(aid: str) -> str:
        aid = aid.strip().lower()
        for prefix in ("arxiv:", "arxiv/"):
            if aid.startswith(prefix):
                aid = aid[len(prefix):]
        return aid.strip()


CONFIDENCE_ICONS = {
    ConfidenceLevel.EXACT: "✅",
    ConfidenceLevel.HIGH: "✅",
    ConfidenceLevel.MEDIUM: "⚠",
    ConfidenceLevel.LOW: "❌",
}

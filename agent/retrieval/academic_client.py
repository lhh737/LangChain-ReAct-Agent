"""多源学术数据聚合客户端：OpenAlex / DBLP / arXiv / Crossref / Semantic Scholar"""
import hashlib
import json
import os
import re
import time
import traceback
from dataclasses import dataclass, field
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

import httpx


@dataclass
class AcademicPaper:
    title: str
    authors: list[str] = field(default_factory=list)
    year: str = ""
    venue: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    citation_count: int = 0
    source: str = ""
    arxiv_id: str = ""
    openalex_id: str = ""
    semantic_scholar_id: str = ""


@dataclass
class SourceQuerySpec:
    """单个数据源的查询规格：端点 + 参数 + 查询模式"""
    source: str
    endpoint: str
    params: dict = field(default_factory=dict)
    mode: str = "search"          # "search" | "identifier" | "bibliographic"
    method: str = "GET"


@dataclass
class SourceSearchResult:
    """单个数据源的检索结果：包含完整状态信息，用于日志、缓存和排错"""
    source: str
    stage: int
    actual_query: str
    papers: list[AcademicPaper] = field(default_factory=list)
    status: str = ""              # "ok" | "empty" | "rate_limited" | "timeout" | "http_error" | "parse_error"
    http_status: int | None = None
    error: str | None = None
    retryable: bool = False
    elapsed: float = 0.0
    partial_parse_failures: int = 0

    @property
    def total_papers(self) -> int:
        return len(self.papers)


@dataclass
@dataclass(frozen=True)
class SearchIntent:
    """检索意图：不可变数据类，封装候选论文名、类型、消歧关键词和兜底查询"""
    candidate: str = ""
    candidate_type: str = "unknown"   # "acronym" | "full_title" | "arxiv_id" | "doi" | "unknown"
    keyword: str = ""                 # Stage 2 消歧关键词（延迟提取）
    fallback_query: str = ""          # 原始研究问题的英文翻译（Stage 3 兜底）
    aspects: str = ""                 # COMPARE 对比维度关键词


class AcademicDataClient:
    CACHE_DIR = get_abs_path("data/cache")
    OK_TTL = 86400       # 有结果：24小时（默认）
    EMPTY_TTL = 300      # 真实空结果：5分钟
    SOURCE_TTL = {       # 分源 TTL（秒），未列出的源使用 OK_TTL
        "arxiv": 86400,
        "crossref": 3600,
        "dblp": 86400,
        "openalex": 3600,
        "semantic_scholar": 3600,
    }

    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)

    # ── Candidate 类型推断 ──

    @staticmethod
    def _infer_candidate_type(candidate: str) -> str:
        """从候选文本推断类型，保守原则：无法确定 → unknown"""
        c = candidate.strip()
        if not c:
            return "unknown"

        # DOI: 10.xxxx/...
        if re.match(r'^10\.\d{4,}/', c):
            return "doi"

        # arXiv ID: 2301.12345 或 arXiv:2301.12345v2
        if re.match(r'^(arXiv:)?\d{4}\.\d{4,5}(v\d+)?$', c, re.IGNORECASE):
            return "arxiv_id"

        # Strict acronym: 全大写 + 可选数字，3-10 字符，不含小写
        if re.match(r'^[A-Z][A-Z0-9]{2,9}$', c):
            return "acronym"

        # Full title: >30 字符且含空格和 ≥4 个词
        if len(c) > 30 and ' ' in c and len(c.split()) >= 4:
            return "full_title"

        return "unknown"

    # ── 缓存（Commit 4: 基于 SourceQuerySpec 键 + 分源 TTL）──

    @staticmethod
    def _spec_cache_key(spec: SourceQuerySpec) -> str:
        """基于 SourceQuerySpec 生成确定性缓存键"""
        canonical = f"{spec.source}|{spec.mode}|{spec.method}|{spec.endpoint}|"
        canonical += json.dumps(spec.params, sort_keys=True, ensure_ascii=True)
        return hashlib.md5(canonical.encode()).hexdigest()

    def _load_spec_cache(self, spec: SourceQuerySpec) -> list[AcademicPaper] | None:
        from agent.retrieval.cache_safety import CacheGuard
        key = self._spec_cache_key(spec)
        cache_file = os.path.join(self.CACHE_DIR, f"{key}.json")
        if not os.path.exists(cache_file):
            return None
        ttl = self.SOURCE_TTL.get(spec.source, self.OK_TTL)
        if time.time() - os.path.getmtime(cache_file) > ttl:
            CacheGuard.remove_expired(key, self.CACHE_DIR)
            return None
        data = CacheGuard.read(key, self.CACHE_DIR)
        if data is None:
            return None
        try:
            return [AcademicPaper(**item) for item in data]
        except Exception:
            return None

    def _save_spec_cache(self, spec: SourceQuerySpec, papers: list[AcademicPaper]):
        if not papers:
            return
        from agent.retrieval.cache_safety import CacheGuard
        key = self._spec_cache_key(spec)
        CacheGuard.write(key, self.CACHE_DIR, [p.__dict__ for p in papers])

    # ── 多级去重 + 元数据合并 ──

    @staticmethod
    def _merge_duplicates(papers: list[AcademicPaper]) -> list[AcademicPaper]:
        """三级去重 + 跨标识符关联 + 标题交叉匹配，保留元数据最全的记录"""
        from agent.retrieval.paper_validator import PaperIdentityValidator

        # 预处理：归一化 arXiv ID（去版本后缀）+ 从 DOI 提取 arXiv ID
        for p in papers:
            if p.arxiv_id:
                p.arxiv_id = re.sub(r'v\d+$', '', p.arxiv_id.strip())
            if p.doi and not p.arxiv_id:
                m = re.search(r'10\.48550/arxiv\.(.+)$', p.doi, re.IGNORECASE)
                if m:
                    p.arxiv_id = m.group(1)

        merged: dict[str, AcademicPaper] = {}
        title_index: dict[str, str] = {}  # 归一化标题 → merged key（交叉匹配）

        for p in papers:
            matched_key = None

            # Level 1: DOI
            if p.doi:
                doi_key = PaperIdentityValidator._normalize_doi(p.doi)
                if doi_key in merged:
                    matched_key = doi_key

            # Level 2: arXiv ID
            if not matched_key and p.arxiv_id:
                aid_key = f"arxiv:{p.arxiv_id.strip().lower()}"
                if aid_key in merged:
                    matched_key = aid_key

            # Level 3: 标题交叉匹配
            if not matched_key:
                title_key = PaperIdentityValidator._normalize_title(p.title)
                if title_key in title_index:
                    matched_key = title_index[title_key]

            if matched_key:
                merged[matched_key] = AcademicDataClient._merge_pair(
                    merged[matched_key], p)
            else:
                # 确定插入键
                if p.doi:
                    key = PaperIdentityValidator._normalize_doi(p.doi)
                elif p.arxiv_id:
                    key = f"arxiv:{p.arxiv_id.strip().lower()}"
                else:
                    key = PaperIdentityValidator._normalize_title(p.title)
                merged[key] = p
                # 注册标题 → 键映射
                tk = PaperIdentityValidator._normalize_title(p.title)
                if tk not in title_index:
                    title_index[tk] = key

        return list(merged.values())

    @staticmethod
    def _merge_pair(a: AcademicPaper, b: AcademicPaper) -> AcademicPaper:
        """合并两条记录，优先保留非空字段（a 为主，b 补充缺失字段）"""
        a_abs_before = len(a.abstract or "")
        b_abs = len(b.abstract or "")
        for field in ["doi", "arxiv_id", "openalex_id", "semantic_scholar_id",
                       "abstract", "url", "venue", "year"]:
            av = getattr(a, field)
            bv = getattr(b, field)
            if not av and bv:
                setattr(a, field, bv)
        a_abs_after = len(a.abstract or "")
        if b_abs > 0 and a_abs_before == 0 and a_abs_after == b_abs:
            logger.info(
                "[AbstractTrace][merge_pair] enriched title=%r abstract %d→%d from source %s",
                a.title[:100], a_abs_before, a_abs_after, b.source,
            )
        if not a.authors and b.authors:
            a.authors = b.authors
        if not a.citation_count and b.citation_count:
            a.citation_count = b.citation_count
        # 保留更多来源信息
        if a.source != b.source:
            a.source = f"{a.source}+{b.source}"
        return a

    # ── 分阶段检索 ──

    def search_stage(self, intent: SearchIntent, stage: int,
                     max_per_source: int = 5, fallback_variant: str = "") -> list[SourceSearchResult]:
        """按阶段执行检索（并行），各源使用 adapter 构建查询。返回所有源的 SourceSearchResult 列表"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from utils.config_handler import agent_conf

        sources = [
            ("arxiv", self._search_arxiv_stage),
            ("crossref", self._search_crossref_stage),
            ("dblp", self._search_dblp_stage),
            ("openalex", self._search_openalex_stage),
            ("semantic_scholar", self._search_semantic_scholar_stage),
        ]

        parallel_cfg = agent_conf.get("retrieval_parallel", {})
        enabled = parallel_cfg.get("enabled", False)
        max_workers = min(parallel_cfg.get("max_workers", 3), len(sources))

        if not enabled or max_workers <= 1:
            # 串行路径
            results = []
            for source_name, source_fn in sources:
                result = self._fetch_source_result(
                    source_name, source_fn, intent, stage, max_per_source, fallback_variant)
                if result is not None:
                    results.append(result)
            return results

        # 并行路径
        indexed: dict[int, SourceSearchResult] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for idx, (name, fn) in enumerate(sources):
                futures[executor.submit(
                    self._fetch_source_result,
                    name, fn, intent, stage, max_per_source, fallback_variant
                )] = idx
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    if result is not None:
                        indexed[idx] = result
                except Exception as e:
                    logger.warning(f"[AcademicClient] {sources[idx][0]} stage{stage}: 线程异常 - {e}")

        # 按原始 sources 索引恢复顺序
        results = [indexed[i] for i in sorted(indexed)]
        return results

    def _fetch_source_result(self, source_name: str, source_fn, intent, stage,
                              max_per_source: int, fallback_variant: str
                              ) -> SourceSearchResult | None:
        """单个源的检索执行器（可被并行调用）"""
        t0 = time.time()
        try:
            spec = source_fn(intent, stage, max_per_source, fallback_variant)
            if spec is None:
                return None
            result = self._do_request(spec, stage)
            result.elapsed = time.time() - t0
            self._log_source_result(result)
            return result
        except Exception as e:
            elapsed = time.time() - t0
            logger.warning(f"[AcademicClient] {source_name} stage{stage}: 异常 ({elapsed:.1f}s) - {e}")
            return SourceSearchResult(
                source=source_name, stage=stage,
                actual_query="", status="http_error",
                error=str(e), elapsed=elapsed,
            )

    # ── 各源 Stage 查询构建器 ──

    @staticmethod
    def _search_arxiv_stage(intent: SearchIntent, stage: int, max_results: int,
                            fallback_variant: str = "") -> SourceQuerySpec | None:
        c = intent.candidate
        k = intent.keyword

        if stage == 1:
            if intent.candidate_type == "arxiv_id":
                aid = c.strip().lower().replace("arxiv:", "")
                return SourceQuerySpec(source="arxiv",
                    endpoint="http://export.arxiv.org/api/query",
                    params={"id_list": aid, "max_results": str(max_results)},
                    mode="identifier")
            if c:
                return SourceQuerySpec(source="arxiv",
                    endpoint="http://export.arxiv.org/api/query",
                    params={"search_query": f'ti:"{c}" OR all:"{c}"',
                            "max_results": str(max_results)},
                    mode="search")
            return None

        if stage == 2 and c and k:
            return SourceQuerySpec(source="arxiv",
                endpoint="http://export.arxiv.org/api/query",
                params={"search_query": f'all:"{c}" AND all:"{k}"',
                        "max_results": str(max_results)},
                mode="search")

        if stage == 3:
            variant = fallback_variant or intent.fallback_query
            if variant:
                terms = [t for t in variant.split() if len(t) > 2]
                if terms:
                    clause = " AND ".join(f'all:"{t}"' for t in terms[:4])
                    return SourceQuerySpec(source="arxiv",
                        endpoint="http://export.arxiv.org/api/query",
                        params={"search_query": clause, "max_results": str(max_results)},
                        mode="search")

        return None

    @staticmethod
    def _clean_abstract(value: object) -> str:
        """清洗摘要：HTML/XML 标签 → 纯文本，规范化空白"""
        import html as _html
        import re as _re

        if not isinstance(value, str):
            return ""
        if not value.strip():
            return ""

        text = _html.unescape(value)
        text = _re.sub(r"<[^>]+>", " ", text)
        text = _re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def _search_crossref_stage(intent: SearchIntent, stage: int, max_results: int,
                               fallback_variant: str = "") -> SourceQuerySpec | None:
        c = intent.candidate

        if stage == 1:
            if intent.candidate_type == "doi":
                return SourceQuerySpec(source="crossref",
                    endpoint=f"https://api.crossref.org/works/{c}",
                    params={}, mode="identifier")
            if intent.candidate_type == "full_title" and c:
                return SourceQuerySpec(source="crossref",
                    endpoint="https://api.crossref.org/works",
                    params={"query.bibliographic": c, "rows": str(max_results)},
                    mode="bibliographic")
            if c:
                return SourceQuerySpec(source="crossref",
                    endpoint="https://api.crossref.org/works",
                    params={"query": c, "rows": str(max_results)},
                    mode="search")
            return None

        if stage == 2 and c and intent.keyword:
            return SourceQuerySpec(source="crossref",
                endpoint="https://api.crossref.org/works",
                params={"query": f"{c} {intent.keyword}", "rows": str(max_results)},
                mode="search")

        if stage == 3:
            variant = fallback_variant or intent.fallback_query
            if variant:
                return SourceQuerySpec(source="crossref",
                    endpoint="https://api.crossref.org/works",
                    params={"query": variant[:200], "rows": str(max_results)},
                    mode="search")

        return None

    @staticmethod
    def _search_dblp_stage(intent: SearchIntent, stage: int, max_results: int,
                           fallback_variant: str = "") -> SourceQuerySpec | None:
        c = intent.candidate
        if not c and not intent.fallback_query:
            return None

        if stage == 1 and c:
            if intent.candidate_type == "acronym":
                q = f"{c}$"
            elif intent.candidate_type == "full_title":
                words = c.split()
                q = " ".join(f"{w}$" for w in words[:6])
            else:
                q = c
            return SourceQuerySpec(source="dblp",
                endpoint="https://dblp.org/search/publ/api",
                params={"q": q, "format": "json", "h": str(max_results)},
                mode="search")

        if stage == 2 and c and intent.keyword:
            q = f"{c}$ {intent.keyword}" if intent.candidate_type == "acronym" else f"{c} {intent.keyword}"
            return SourceQuerySpec(source="dblp",
                endpoint="https://dblp.org/search/publ/api",
                params={"q": q, "format": "json", "h": str(max_results)},
                mode="search")

        if stage == 3:
            variant = fallback_variant or intent.fallback_query
            if variant:
                return SourceQuerySpec(source="dblp",
                    endpoint="https://dblp.org/search/publ/api",
                    params={"q": variant[:200], "format": "json", "h": str(max_results)},
                    mode="search")

        return None

    @staticmethod
    def _search_openalex_stage(intent: SearchIntent, stage: int, max_results: int,
                               fallback_variant: str = "") -> SourceQuerySpec | None:
        c = intent.candidate

        if stage == 1:
            if intent.candidate_type == "doi":
                return SourceQuerySpec(source="openalex",
                    endpoint=f"https://api.openalex.org/works/DOI:{c}",
                    params={}, mode="identifier")
            if c:
                return SourceQuerySpec(source="openalex",
                    endpoint="https://api.openalex.org/works",
                    params={"search": c, "per_page": str(max_results)},
                    mode="search")
            return None

        if stage == 2 and c and intent.keyword:
            return SourceQuerySpec(source="openalex",
                endpoint="https://api.openalex.org/works",
                params={"search": f"{c} {intent.keyword}", "per_page": str(max_results)},
                mode="search")

        if stage == 3:
            variant = fallback_variant or intent.fallback_query
            if variant:
                return SourceQuerySpec(source="openalex",
                    endpoint="https://api.openalex.org/works",
                    params={"search": variant[:200], "per_page": str(max_results)},
                    mode="search")

        return None

    @staticmethod
    def _search_semantic_scholar_stage(intent: SearchIntent, stage: int, max_results: int,
                                       fallback_variant: str = "") -> SourceQuerySpec | None:
        c = intent.candidate
        fields = "title,authors,year,abstract,citationCount,url,externalIds"

        if stage == 1:
            if intent.candidate_type == "doi":
                return SourceQuerySpec(source="semantic_scholar",
                    endpoint=f"https://api.semanticscholar.org/graph/v1/paper/DOI:{c}",
                    params={"fields": fields}, mode="identifier")
            if intent.candidate_type == "arxiv_id":
                aid = c.strip().lower().replace("arxiv:", "")
                return SourceQuerySpec(source="semantic_scholar",
                    endpoint=f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{aid}",
                    params={"fields": fields}, mode="identifier")
            if c:
                if intent.candidate_type == "full_title":
                    return SourceQuerySpec(source="semantic_scholar",
                        endpoint="https://api.semanticscholar.org/graph/v1/paper/search",
                        params={"query": f'"{c}"', "limit": str(max_results), "fields": fields},
                        mode="search")
                return SourceQuerySpec(source="semantic_scholar",
                    endpoint="https://api.semanticscholar.org/graph/v1/paper/search",
                    params={"query": c, "limit": str(max_results), "fields": fields},
                    mode="search")
            return None

        if stage == 2 and c and intent.keyword:
            return SourceQuerySpec(source="semantic_scholar",
                endpoint="https://api.semanticscholar.org/graph/v1/paper/search/bulk",
                params={"query": f'+"{c}" +{intent.keyword}', "limit": str(max_results),
                        "fields": fields},
                mode="search", method="POST")

        if stage == 3:
            variant = fallback_variant or intent.fallback_query
            if variant:
                return SourceQuerySpec(source="semantic_scholar",
                    endpoint="https://api.semanticscholar.org/graph/v1/paper/search",
                    params={"query": variant[:200], "limit": str(max_results), "fields": fields},
                    mode="search")

        return None

    # ── 统一请求处理 ──

    @staticmethod
    def _classify_status(http_status: int | None, exception: Exception | None,
                         papers_count: int) -> tuple[str, bool, str | None]:
        """根据 HTTP 状态码 / 异常 / 结果数量 分类返回状态"""
        if exception is not None:
            exc_name = type(exception).__name__
            if isinstance(exception, httpx.TimeoutException):
                return "timeout", True, f"{exc_name}: {exception}"
            return "http_error", True, f"{exc_name}: {exception}"

        if http_status == 429:
            return "rate_limited", True, "HTTP 429 Too Many Requests"
        if http_status == 403:
            return "http_error", False, "HTTP 403 Forbidden"
        if http_status is not None and http_status >= 500:
            return "http_error", True, f"HTTP {http_status}"
        if http_status is not None and http_status >= 400:
            return "http_error", False, f"HTTP {http_status}"
        if http_status == 200 and papers_count == 0:
            return "empty", False, None
        if http_status == 200:
            return "ok", False, None

        return "http_error", False, f"Unexpected HTTP {http_status}"

    def _do_request(self, spec: SourceQuerySpec, stage: int,
                    timeout: float = 15.0) -> SourceSearchResult:
        """执行单个源请求（含指数退避重试 + Retry-After），优先命中缓存"""
        from agent.retrieval.retry_policy import get_retry_policy

        # 缓存检查
        cached = self._load_spec_cache(spec)
        if cached is not None:
            logger.debug(f"[AcademicClient] {spec.source}: 缓存命中 {len(cached)}条")
            return SourceSearchResult(
                source=spec.source, stage=stage,
                actual_query=str(spec.params),
                papers=cached, status="ok", http_status=304,
            )

        policy = get_retry_policy()
        cfg = policy.for_source(spec.source)
        last_result = None

        for attempt in range(1, cfg.max_retries + 2):  # 1..max_retries+1
            result = SourceSearchResult(
                source=spec.source, stage=stage,
                actual_query=str(spec.params), status="http_error",
            )
            exc = None
            try:
                if spec.method == "GET":
                    resp = httpx.get(spec.endpoint, params=spec.params,
                                     timeout=timeout, follow_redirects=True)
                else:
                    resp = httpx.post(spec.endpoint, json=spec.params,
                                      timeout=timeout, follow_redirects=True)
                result.http_status = resp.status_code
                result.elapsed = resp.elapsed.total_seconds()

                if resp.status_code == 200:
                    try:
                        papers, parse_fails = self._parse_response(spec.source, resp)
                        result.papers = papers
                        result.partial_parse_failures = parse_fails
                        if parse_fails > 0:
                            logger.warning(
                                f"[AcademicClient] {spec.source}: {parse_fails}条解析失败, "
                                f"{len(papers)}条成功"
                            )
                    except Exception as e:
                        result.status, result.retryable, result.error =                             self._classify_status(None, e, 0)
                        result.status = "parse_error"
                        trace = traceback.format_exc()
                        logger.error(f"[AcademicClient] {spec.source}: 整批解析失败 - {e}\n{trace}")
                        return result  # parse_error 不重试

                result.status, result.retryable, result.error =                     self._classify_status(result.http_status, None, len(result.papers))

                # 成功或不可重试 → 立即返回
                if result.status in ("ok", "empty"):
                    valid_empty = (
                        result.status == "ok" and not result.papers
                        and policy.valid_empty_requires_retry
                        and attempt <= cfg.max_retries  # 未经过重试
                    )
                    if not valid_empty:
                        # 缓存
                        if result.status == "ok" and result.papers:
                            self._save_spec_cache(spec, result.papers)
                        return result
                    # valid_empty 且首次 → 继续重试
                    logger.info(f"[AcademicClient] {spec.source}: empty on first try, will retry")
                elif not policy.should_retry(result.status, result.http_status, None, attempt):
                    return result

            except httpx.TimeoutException as e:
                exc = e
                result.elapsed = timeout
                result.status, result.retryable, result.error = self._classify_status(None, e, 0)
            except httpx.HTTPStatusError as e:
                exc = e
                result.http_status = e.response.status_code
                result.elapsed = e.response.elapsed.total_seconds() if e.response else 0
                result.status, result.retryable, result.error = self._classify_status(
                    result.http_status, e, 0)
            except Exception as e:
                exc = e
                result.status, result.retryable, result.error = self._classify_status(None, e, 0)

            if not policy.should_retry(result.status, result.http_status, exc, attempt):
                return result

            # 指数退避等待
            retry_after = None
            if hasattr(result, 'http_status') and result.http_status == 429:
                try:
                    retry_after = policy.parse_retry_after(resp.headers)
                except Exception:
                    pass
            delay = policy.backoff_delay(attempt, spec.source, retry_after)
            logger.warning(
                f"[AcademicClient] {spec.source}: retry {attempt}/{cfg.max_retries} "
                f"after {delay:.1f}s (status={result.status})"
            )
            policy.sleep_fn(delay)
            last_result = result

        return last_result or result

    def _parse_response(self, source: str, resp) -> tuple[list[AcademicPaper], int]:
        """路由到各源的解析器，返回 (papers, parse_failures)"""
        parsers = {
            "arxiv": self._parse_arxiv_response,
            "crossref": self._parse_crossref_response,
            "dblp": self._parse_dblp_response,
            "openalex": self._parse_openalex_response,
            "semantic_scholar": self._parse_semantic_scholar_response,
        }
        parser = parsers.get(source, lambda r: ([], 0))
        return parser(resp)

    def _safe_parse(self, items: list, item_parser) -> tuple[list[AcademicPaper], int]:
        """逐项解析，单条异常不中断整批。返回 (papers, failure_count)"""
        papers = []
        failures = 0
        for item in items:
            try:
                paper = item_parser(item)
                if paper is not None:
                    papers.append(paper)
            except Exception:
                failures += 1
                logger.debug(f"[AcademicClient] 单条解析失败: {traceback.format_exc()[-200:]}")
        return papers, failures

    # ── 各源解析器 ──

    def _parse_arxiv_response(self, resp) -> tuple[list[AcademicPaper], int]:
        import xml.etree.ElementTree as ET
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        try:
            root = ET.fromstring(resp.text)
            entries = root.findall("atom:entry", ns)
        except Exception:
            return [], 0

        def parse_entry(entry) -> AcademicPaper | None:
            title_el = entry.find("atom:title", ns)
            summary_el = entry.find("atom:summary", ns)
            title = title_el.text.strip() if title_el is not None and title_el.text else ""
            if not title:
                return None
            authors = [a.find("atom:name", ns).text or ""
                       for a in entry.findall("atom:author", ns)
                       if a.find("atom:name", ns) is not None]
            arxiv_url = entry.find("atom:id", ns).text if entry.find("atom:id", ns) is not None else ""
            arxiv_id = arxiv_url.split("/abs/")[-1] if "/abs/" in arxiv_url else ""
            return AcademicPaper(
                title=title,
                authors=authors,
                abstract=summary_el.text.strip() if summary_el is not None and summary_el.text else "",
                url=arxiv_url,
                arxiv_id=arxiv_id,
                source="arXiv",
            )

        papers, failures = self._safe_parse(entries, parse_entry)
        return papers, failures

    def _parse_crossref_response(self, resp) -> tuple[list[AcademicPaper], int]:
        try:
            items = resp.json().get("message", {}).get("items", [])
        except Exception:
            return [], 0

        def parse_item(item) -> AcademicPaper | None:
            title = item.get("title", [""])[0] if item.get("title") else ""
            if not title:
                return None
            authors = []
            for a in item.get("author", [])[:5]:
                given = a.get("given", "")
                family = a.get("family", "")
                authors.append(f"{given} {family}".strip())
            year = str(item.get("created", {}).get("date-parts", [[None]])[0][0] or "")
            doi = item.get("DOI", "")
            raw_abstract = item.get("abstract")
            has_field = "abstract" in item
            logger.info(
                "[AbstractTrace][crossref] title=%r has_abstract_field=%s raw_type=%s raw_len=%d raw_repr=%r",
                title[:100],
                has_field,
                type(raw_abstract).__name__,
                len(str(raw_abstract or "")),
                str(raw_abstract or "")[:500],
            )
            abstract = AcademicDataClient._clean_abstract(raw_abstract)
            logger.info(
                "[AbstractTrace][crossref_cleaned] title=%r abstract_len=%d repr=%r",
                title[:100],
                len(abstract),
                abstract[:500],
            )
            return AcademicPaper(
                title=title,
                authors=authors,
                year=year,
                doi=doi,
                venue=", ".join(item.get("container-title", [])) if item.get("container-title") else "",
                url=f"https://doi.org/{doi}" if doi else "",
                abstract=abstract,
                source="Crossref",
            )

        papers, failures = self._safe_parse(items, parse_item)
        return papers, failures

    def _parse_dblp_response(self, resp) -> tuple[list[AcademicPaper], int]:
        try:
            hits = resp.json().get("result", {}).get("hits", {}).get("hit", [])
        except Exception:
            return [], 0

        def parse_hit(hit) -> AcademicPaper | None:
            info = hit.get("info", {})
            title = info.get("title", "")
            if not title:
                return None
            authors = []
            author_data = info.get("authors", {}).get("author")
            if isinstance(author_data, list):
                authors = [a.get("text", "") for a in author_data if a.get("text")]
            elif isinstance(author_data, dict) and author_data.get("text"):
                authors = [author_data["text"]]
            year = str(info.get("year", ""))
            return AcademicPaper(
                title=title,
                authors=authors,
                year=year,
                venue=info.get("venue", ""),
                url=info.get("ee", info.get("url", "")),
                source="DBLP",
            )

        papers, failures = self._safe_parse(hits, parse_hit)
        return papers, failures

    def _parse_openalex_response(self, resp) -> tuple[list[AcademicPaper], int]:
        try:
            results = resp.json().get("results", [])
        except Exception:
            return [], 0

        def parse_item(item) -> AcademicPaper | None:
            title = item.get("title", "")
            if not title:
                return None
            authors = []
            for a in item.get("authorships", [])[:5]:
                auth_name = a.get("author", {}).get("display_name", "")
                if auth_name:
                    authors.append(auth_name)
            inverted = item.get("abstract_inverted_index")
            logger.info(
                "[AbstractTrace][openalex] title=%r has_inverted_index=%s term_count=%d",
                title[:100],
                bool(inverted),
                len(inverted or {}),
            )
            abstract = ""
            if inverted:
                try:
                    max_pos = max(max(v) for v in inverted.values())
                    words = [""] * (max_pos + 1)
                    for word, positions in inverted.items():
                        for pos in positions:
                            words[pos] = word
                    abstract = " ".join(words)
                except Exception:
                    pass
            logger.info(
                "[AbstractTrace][openalex_parsed] title=%r abstract_len=%d repr=%r",
                title[:100],
                len(abstract),
                abstract[:500],
            )
            return AcademicPaper(
                title=title,
                authors=authors,
                year=str(item.get("publication_year", "")),
                doi=item.get("doi", ""),
                venue=item.get("primary_location", {}).get("source", {}).get("display_name", ""),
                citation_count=item.get("cited_by_count", 0),
                url=item.get("primary_location", {}).get("landing_page_url", ""),
                openalex_id=item.get("id", "").split("/")[-1] if item.get("id") else "",
                abstract=abstract,
                source="OpenAlex",
            )

        papers, failures = self._safe_parse(results, parse_item)
        return papers, failures

    def _parse_semantic_scholar_response(self, resp) -> tuple[list[AcademicPaper], int]:
        try:
            data = resp.json()
            # bulk search 返回 dict，relevance search 返回 list
            if isinstance(data, dict):
                items = data.get("data", [])
            elif isinstance(data, list):
                items = data
            else:
                items = []
        except Exception:
            return [], 0

        def parse_item(item) -> AcademicPaper | None:
            title = item.get("title", "")
            if not title:
                return None
            authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
            ss_id = item.get("paperId", "")
            external_ids = item.get("externalIds", {}) or {}
            doi = external_ids.get("DOI", "")
            arxiv_id = external_ids.get("ArXiv", "")
            raw_abstract = item.get("abstract") or ""
            logger.info(
                "[AbstractTrace][semantic_scholar] title=%r abstract_len=%d repr=%r",
                title[:100],
                len(raw_abstract),
                raw_abstract[:500],
            )
            return AcademicPaper(
                title=title,
                authors=authors,
                year=str(item.get("year", "")),
                abstract=raw_abstract,
                citation_count=item.get("citationCount", 0) or 0,
                url=item.get("url", ""),
                doi=doi,
                arxiv_id=arxiv_id,
                semantic_scholar_id=ss_id,
                source="Semantic Scholar",
            )

        papers, failures = self._safe_parse(items, parse_item)
        return papers, failures

    # ── 检索主入口（向后兼容，内部使用多级去重 + 合并）──

    def search(self, query: str, max_results: int = 20) -> list[AcademicPaper]:
        """多源检索，保持向后兼容的 list[AcademicPaper] 接口"""
        synthetic_spec = SourceQuerySpec(source="legacy", endpoint="search",
                                         params={"query": query}, mode="search")
        cached = self._load_spec_cache(synthetic_spec)
        if cached is not None:
            logger.info(f"[AcademicClient]缓存命中: {query}")
            return cached

        all_papers: list[AcademicPaper] = []

        with httpx.Client(timeout=15.0) as client:
            for fn in [
                self._search_arxiv, self._search_crossref,
                self._search_dblp, self._search_openalex,
                self._search_semantic_scholar,
            ]:
                t0 = time.time()
                source_name = fn.__name__.replace("_search_", "")
                try:
                    result = fn(client, query)
                    result.elapsed = time.time() - t0
                    self._log_source_result(result)
                    if result.status == "ok":
                        all_papers.extend(result.papers)
                except Exception as e:
                    elapsed = time.time() - t0
                    logger.warning(
                        f"[AcademicClient] {source_name}: 未预期异常 ({elapsed:.1f}s) - {e}"
                    )

        # 多级去重 + 元数据合并 + 截断
        result = self._merge_duplicates(all_papers)[:max_results]
        self._save_spec_cache(synthetic_spec, result)
        logger.info(f"[AcademicClient]检索完成: query='{query}', 去重后={len(result)}")
        return result

    @staticmethod
    def _log_source_result(result: SourceSearchResult):
        """统一日志格式"""
        status_icon = {"ok": "+", "empty": "-", "rate_limited": "R", "timeout": "T",
                       "http_error": "E", "parse_error": "P"}.get(result.status, "?")
        extra = ""
        if result.partial_parse_failures:
            extra += f" (parse_fail={result.partial_parse_failures})"
        if result.error:
            extra += f" [{result.error[:80]}]"

        if result.status == "ok":
            lines = []
            for i, p in enumerate(result.papers):
                authors = ", ".join(p.authors[:2]) if p.authors else ""
                year = f"({p.year})" if p.year else ""
                title = p.title[:100]
                lines.append(f"  [{i+1}] {title} | {authors} {year}")
            logger.info(
                f"[AcademicClient] {status_icon} {result.source}: {result.total_papers}条, "
                f"{result.elapsed:.1f}s{extra}\n" + "\n".join(lines)
            )
        else:
            logger.info(
                f"[AcademicClient] {status_icon} {result.source}: {result.status}, "
                f"{result.elapsed:.1f}s{extra}"
            )

    # ── 各源搜索方法（Commit 1：内部改为构建 SourceQuerySpec + _do_request）──

    def _search_arxiv(self, client: httpx.Client, query: str) -> SourceSearchResult:
        spec = SourceQuerySpec(
            source="arxiv",
            endpoint="http://export.arxiv.org/api/query",
            params={"search_query": f"all:{query}", "max_results": "5"},
            mode="search",
        )
        result = self._do_request(spec, stage=1)
        return result

    def _search_crossref(self, client: httpx.Client, query: str) -> SourceSearchResult:
        spec = SourceQuerySpec(
            source="crossref",
            endpoint="https://api.crossref.org/works",
            params={"query": query, "rows": "5"},
            mode="search",
        )
        result = self._do_request(spec, stage=1)
        return result

    def _search_dblp(self, client: httpx.Client, query: str) -> SourceSearchResult:
        spec = SourceQuerySpec(
            source="dblp",
            endpoint="https://dblp.org/search/publ/api",
            params={"q": query, "format": "json", "h": "5"},
            mode="search",
        )
        result = self._do_request(spec, stage=1)
        return result

    def _search_openalex(self, client: httpx.Client, query: str) -> SourceSearchResult:
        spec = SourceQuerySpec(
            source="openalex",
            endpoint="https://api.openalex.org/works",
            params={"search": query, "per_page": "5"},
            mode="search",
        )
        result = self._do_request(spec, stage=1)
        return result

    def _search_semantic_scholar(self, client: httpx.Client, query: str) -> SourceSearchResult:
        spec = SourceQuerySpec(
            source="semantic_scholar",
            endpoint="https://api.semanticscholar.org/graph/v1/paper/search",
            params={"query": query, "limit": "5",
                    "fields": "title,authors,year,abstract,citationCount,url,externalIds"},
            mode="search",
        )
        result = self._do_request(spec, stage=1)
        return result

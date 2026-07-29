"""Tests for REVIEW evidence block construction and structured references."""
import pytest

from agent.evidence_budgeter import EvidenceBlock, build_online_blocks, TokenCounter


# ── Test helpers ──

class _FakePaper:
    """Minimal AcademicPaper stand-in for tests."""
    def __init__(self, title, abstract="", doi="", url="", authors=None,
                 year="", source="Crossref", score=0.9):
        self.title = title
        self.abstract = abstract
        self.doi = doi
        self.url = url
        self.authors = authors or []
        self.year = year
        self.source = source
        self.score = score


def _make_scored_results(papers_and_scores):
    """Create scored_results tuple like OnlineRetrievalResult."""
    return tuple((p, s) for p, s in papers_and_scores)


# ── Tests for _build_review_online_blocks ──

class TestBuildReviewOnlineBlocks:
    """Tests for ReactAgent._build_review_online_blocks()."""

    @staticmethod
    def _call_build(scored_results, max_papers=30):
        """Import and call the static method."""
        from agent.react_agent import ReactAgent
        return ReactAgent._build_review_online_blocks(scored_results, max_papers=max_papers)

    def test_one_block_per_paper(self):
        """5 scored papers → 5 independent candidate blocks."""
        papers = [
            _FakePaper(f"Paper {i}", abstract=f"Abstract of paper {i}.", doi=f"10.1000/{i}")
            for i in range(5)
        ]
        scored = _make_scored_results([(p, 0.9 - i * 0.05) for i, p in enumerate(papers)])
        blocks = self._call_build(scored)

        assert len(blocks) == 5
        titles = [b["title"] for b in blocks]
        assert titles == [f"Paper {i}" for i in range(5)]

    def test_does_not_use_formatted_text(self):
        """online_result.text truncation does not affect scored_results entry."""
        papers = [
            _FakePaper(f"Paper {i}", abstract=f"Abstract {i}.", doi=f"10.{i}")
            for i in range(10)
        ]
        scored = _make_scored_results([(p, 0.95 - i * 0.03) for i, p in enumerate(papers)])
        blocks = self._call_build(scored, max_papers=30)

        assert len(blocks) == 10

    def test_skips_paper_without_abstract(self):
        """Papers without abstract/snippet must not become evidence blocks."""
        papers = [
            _FakePaper("Good Paper", abstract="Has abstract.", doi="10.1"),
            _FakePaper("Bad Paper", abstract="", doi="10.2"),
            _FakePaper("Also Bad", abstract="   ", doi="10.3"),
            _FakePaper("Good Paper 2", abstract="Another abstract.", doi="10.4"),
        ]
        scored = _make_scored_results([(p, 0.9) for p in papers])
        blocks = self._call_build(scored)

        assert len(blocks) == 2
        titles = {b["title"] for b in blocks}
        assert titles == {"Good Paper", "Good Paper 2"}

    def test_deduplicates_by_doi(self):
        """Papers with same DOI are deduplicated."""
        papers = [
            _FakePaper("Title A", abstract="Abstract A.", doi="10.1000/SAME"),
            _FakePaper("Title B", abstract="Abstract B.", doi="10.1000/SAME"),
            _FakePaper("Title C", abstract="Abstract C.", doi="10.1000/diff"),
        ]
        scored = _make_scored_results([(p, 0.9) for p in papers])
        blocks = self._call_build(scored)

        assert len(blocks) == 2
        dois = {b["doi"] for b in blocks}
        assert "10.1000/SAME" in dois
        assert "10.1000/diff" in dois

    def test_deduplicates_by_title_when_no_doi(self):
        """Papers with same normalized title (no DOI) are deduplicated."""
        papers = [
            _FakePaper("The Great Paper", abstract="A.", doi=""),
            _FakePaper("the great paper", abstract="B.", doi=""),
            _FakePaper("Other Paper", abstract="C.", doi=""),
        ]
        scored = _make_scored_results([(p, 0.9) for p in papers])
        blocks = self._call_build(scored)

        assert len(blocks) == 2

    def test_respects_max_papers(self):
        """Candidate blocks are capped at max_papers."""
        papers = [
            _FakePaper(f"Paper {i}", abstract=f"Abstract {i}.", doi=f"10.{i}")
            for i in range(50)
        ]
        scored = _make_scored_results([(p, 0.99 - i * 0.01) for i, p in enumerate(papers)])
        blocks = self._call_build(scored, max_papers=20)

        assert len(blocks) == 20

    def test_quality_score_is_preserved(self):
        """AcademicPaper score is correctly mapped to quality_score."""
        p1 = _FakePaper("High", abstract="A.", doi="10.1", score=0.95)
        p2 = _FakePaper("Low", abstract="B.", doi="10.2", score=0.35)
        scored = _make_scored_results([(p1, 0.95), (p2, 0.35)])
        blocks = self._call_build(scored)

        assert blocks[0]["title"] == "High"
        assert blocks[0]["quality_score"] == 0.95
        assert blocks[1]["title"] == "Low"
        assert blocks[1]["quality_score"] == 0.35


# ── Tests for build_online_blocks with metadata ──

class TestBuildOnlineBlocksMetadata:
    """Tests for evidence_budgeter.build_online_blocks metadata passthrough."""

    def test_metadata_fields_preserved(self):
        """Authors, year, doi, url, evidence_type are stored in citation_meta."""
        counter = TokenCounter()
        items = [{
            "title": "Test Paper",
            "source": "Crossref",
            "content": "Test abstract.",
            "quality_score": 0.88,
            "authors": ["Alice", "Bob"],
            "year": "2025",
            "doi": "10.1000/test",
            "url": "https://example.com",
            "evidence_type": "abstract",
        }]
        blocks = build_online_blocks(items, counter)

        assert len(blocks) == 1
        meta = blocks[0].citation_meta
        assert meta["title"] == "Test Paper"
        assert meta["authors"] == ["Alice", "Bob"]
        assert meta["year"] == "2025"
        assert meta["doi"] == "10.1000/test"
        assert meta["url"] == "https://example.com"
        assert meta["evidence_type"] == "abstract"

    def test_quality_score_falls_back_to_score_key(self):
        """When quality_score is missing, score key is used."""
        counter = TokenCounter()
        items = [{
            "title": "Test",
            "source": "Crossref",
            "content": "Abstract.",
            "score": 0.72,
        }]
        blocks = build_online_blocks(items, counter)

        assert blocks[0].quality_score == 0.72

    def test_default_score(self):
        """When neither quality_score nor score is present, default to 0.5."""
        counter = TokenCounter()
        items = [{
            "title": "Test",
            "source": "Crossref",
            "content": "Abstract.",
        }]
        blocks = build_online_blocks(items, counter)

        assert blocks[0].quality_score == 0.5


# ── Tests for EvidenceBlock.render() ──

class TestEvidenceBlockRender:
    """Tests for EvidenceBlock.render() output format."""

    def test_online_render_includes_authors_year_doi(self):
        """Online render includes full metadata header."""
        block = EvidenceBlock(
            evidence_id="online:0",
            source_type="online",
            subject_id="",
            source_order=0,
            quality_score=0.9,
            citation_meta={
                "title": "Great Paper",
                "source": "Crossref",
                "authors": ["Alice", "Bob", "Charlie"],
                "year": "2025",
                "doi": "10.1000/x",
                "url": "https://x.com",
                "evidence_type": "abstract",
            },
            raw_content="This is the evidence text.",
            token_cost=50,
        )
        rendered = block.render(1)

        assert "[1] [在线]《Great Paper》" in rendered
        assert "作者：Alice, Bob, Charlie" in rendered
        assert "年份：2025" in rendered
        assert "来源：Crossref" in rendered
        assert "类型：abstract" in rendered
        assert "DOI：10.1000/x" in rendered
        assert "URL：https://x.com" in rendered
        assert "This is the evidence text." in rendered

    def test_online_render_truncates_authors_at_3(self):
        """Authors list > 3 gets truncated with 等."""
        block = EvidenceBlock(
            evidence_id="online:0",
            source_type="online",
            subject_id="",
            source_order=0,
            quality_score=0.9,
            citation_meta={
                "title": "Test",
                "source": "Crossref",
                "authors": ["A", "B", "C", "D", "E"],
                "year": "",
                "doi": "",
                "url": "",
                "evidence_type": "abstract",
            },
            raw_content="Evidence.",
            token_cost=50,
        )
        rendered = block.render(1)

        assert "作者：A, B, C 等" in rendered

    def test_local_render_unchanged(self):
        """Local evidence block render is not affected."""
        block = EvidenceBlock(
            evidence_id="local:0",
            source_type="local",
            subject_id="",
            source_order=0,
            quality_score=0.5,
            citation_meta={
                "title": "Local Paper",
                "section": "Methods",
                "page_start": "3",
                "page_end": "5",
            },
            raw_content="Local evidence.",
            token_cost=50,
        )
        rendered = block.render(2)

        assert "[2] 来源：《Local Paper》" in rendered
        assert "章节：Methods" in rendered
        assert "pp.3-5" in rendered
        assert "Local evidence." in rendered


# ── Tests for reference numbering consistency ──

class TestReferenceNumberingConsistency:
    """Tests that allocation numbers match across selected_blocks, context, and references."""

    def test_selected_blocks_match_context_numbers(self):
        """The [N] in context matches block.render(N) output."""
        from agent.evidence_budgeter import EvidenceBudgeter

        counter = TokenCounter()
        items = [
            {"title": f"Paper {i}", "source": "Crossref",
             "content": f"Abstract {i}.", "quality_score": 0.9,
             "authors": ["A"], "evidence_type": "abstract"}
            for i in range(3)
        ]
        blocks = build_online_blocks(items, counter)

        budgeter = EvidenceBudgeter()
        allocation = budgeter.allocate(
            system_prompt="You are a reviewer.\n",
            query="test query",
            local_blocks=[],
            online_blocks=blocks,
            online_available=True,
        )

        assert len(allocation.selected_blocks) == 3
        assert len(allocation.references) == 3

        for i, block in enumerate(allocation.selected_blocks):
            rendered = block.render(i + 1)
            assert rendered in allocation.context

        for i, (ref_num, ev_id, _) in enumerate(allocation.reference_map):
            assert ref_num == i + 1
            assert ev_id == allocation.selected_blocks[i].evidence_id

    def test_max_n_matches_selected_count(self):
        """max_n used for citation validation == len(selected_blocks)."""
        from agent.evidence_budgeter import EvidenceBudgeter

        counter = TokenCounter()
        items = [
            {"title": f"Paper {i}", "source": "Crossref",
             "content": f"Abstract {i}.", "quality_score": 0.9,
             "authors": ["A"], "evidence_type": "abstract"}
            for i in range(4)
        ]
        blocks = build_online_blocks(items, counter)

        budgeter = EvidenceBudgeter()
        allocation = budgeter.allocate(
            system_prompt="You are a reviewer.\n",
            query="test query",
            local_blocks=[],
            online_blocks=blocks,
            online_available=True,
        )

        max_n = len(allocation.selected_blocks)
        assert max_n == 4

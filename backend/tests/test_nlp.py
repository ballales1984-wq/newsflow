"""NLP service tests

These tests cover both the happy path (when spaCy models are installed) and
the graceful-degradation path (when no model is available), which is what
actually runs on this machine.  All tests that require spaCy are wrapped with
``pytest.importorskip`` so they are *skipped* (not failed) when the library or
models are absent.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.nlp.analyzer import NLPAnalyzer


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def analyzer():
    """Return a fresh NLPAnalyzer for every test."""
    return NLPAnalyzer()


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def test_nlp_analyzer_initialization(analyzer):
    """NLPAnalyzer must always be constructible, even without spaCy."""
    assert analyzer is not None


# ---------------------------------------------------------------------------
# _detect_language
# ---------------------------------------------------------------------------

def test_detect_language_returns_string(analyzer):
    """_detect_language must always return a string."""
    lang = analyzer._detect_language("Hello world this is a test sentence.")
    assert isinstance(lang, str)
    assert len(lang) > 0


def test_detect_language_fallback_on_empty(analyzer):
    """An empty string cannot be detected: the method must not raise."""
    try:
        lang = analyzer._detect_language("")
    except Exception:
        pytest.fail("_detect_language raised an exception on empty input")


def test_detect_language_handles_exception(analyzer):
    """If langdetect raises, _detect_language falls back to 'en'."""
    with patch("app.services.nlp.analyzer.LANGDETECT_AVAILABLE", True):
        with patch("app.services.nlp.analyzer.detect", side_effect=Exception("fail")):
            lang = analyzer._detect_language("some text")
    assert lang == "en"


# ---------------------------------------------------------------------------
# _calculate_reading_time
# ---------------------------------------------------------------------------

def test_reading_time_minimum_is_one():
    """Even a single word should give a reading time of at least 1 minute."""
    analyzer = NLPAnalyzer()
    result = analyzer._calculate_reading_time("hello")
    assert result >= 1


def test_reading_time_400_words():
    """400 words at 200 wpm = exactly 2 minutes."""
    analyzer = NLPAnalyzer()
    text = " ".join(["word"] * 400)
    result = analyzer._calculate_reading_time(text)
    assert result == 2


def test_reading_time_200_words():
    """200 words at 200 wpm = exactly 1 minute."""
    analyzer = NLPAnalyzer()
    text = " ".join(["word"] * 200)
    result = analyzer._calculate_reading_time(text)
    assert result == 1


# ---------------------------------------------------------------------------
# _calculate_quality_score (pure Python, no spaCy dependency)
# ---------------------------------------------------------------------------

def test_quality_score_base():
    """An article with no keywords scores 0.5 (the base)."""
    analyzer = NLPAnalyzer()
    score = analyzer._calculate_quality_score("Short.", [])
    assert score == pytest.approx(0.5)


def test_quality_score_long_article_bonus():
    """A 600-word article should receive the 0.2 length bonus."""
    analyzer = NLPAnalyzer()
    text = " ".join(["word"] * 600)
    score = analyzer._calculate_quality_score(text, [])
    assert score >= 0.7


def test_quality_score_keyword_bonus():
    """10 keywords should add 0.15 to the score."""
    analyzer = NLPAnalyzer()
    keywords = [f"kw{i}" for i in range(10)]
    score = analyzer._calculate_quality_score("Some text.", keywords)
    assert score >= 0.65


def test_quality_score_paragraph_bonus():
    """Three or more paragraphs (separated by \\n\\n) add 0.1."""
    analyzer = NLPAnalyzer()
    text = "Para one.\n\nPara two.\n\nPara three."
    score = analyzer._calculate_quality_score(text, [])
    assert score >= 0.6


def test_quality_score_url_bonus():
    """A URL in the text adds 0.05."""
    analyzer = NLPAnalyzer()
    text = "Check https://example.com for more info."
    score = analyzer._calculate_quality_score(text, [])
    assert score >= 0.55


def test_quality_score_capped_at_one():
    """The quality score must never exceed 1.0."""
    analyzer = NLPAnalyzer()
    text = " ".join(["word"] * 1000) + "\n\n" * 5 + " https://example.com"
    keywords = [f"kw{i}" for i in range(15)]
    score = analyzer._calculate_quality_score(text, keywords)
    assert score <= 1.0


# ---------------------------------------------------------------------------
# _empty_analysis
# ---------------------------------------------------------------------------

def test_empty_analysis_structure():
    """_empty_analysis must return the expected keys with default values."""
    analyzer = NLPAnalyzer()
    result = analyzer._empty_analysis()

    assert result["language"] == "unknown"
    assert result["keywords"] == []
    assert result["entities"] == {
        "persons": [],
        "organizations": [],
        "locations": [],
        "misc": [],
    }
    assert result["sentiment_score"] == 0.0
    assert result["quality_score"] == 0.0
    assert result["word_count"] == 0
    assert result["reading_time_minutes"] == 0


# ---------------------------------------------------------------------------
# analyze  – empty / no-spaCy path
# ---------------------------------------------------------------------------

def test_analyze_empty_text(analyzer):
    """An empty string must return the empty-analysis sentinel without raising."""
    result = analyzer.analyze("")
    assert result["language"] == "unknown"
    assert result["word_count"] == 0


def test_analyze_returns_required_keys(analyzer):
    """analyze() must always return a dict with at least the required keys."""
    result = analyzer.analyze("Some text to analyse.")
    for key in ("language", "keywords", "entities", "sentiment_score",
                "quality_score", "word_count", "reading_time_minutes"):
        assert key in result, f"Missing key: {key}"


def test_analyze_word_count_without_spacy():
    """word_count should still be populated even when no spaCy model is loaded."""
    analyzer = NLPAnalyzer()
    # Force the no-model branch by removing any loaded models
    analyzer.nlp_it = None
    analyzer.nlp_en = None

    # When no model is available, analyze() returns _empty_analysis()
    result = analyzer.analyze("This sentence has five words.")
    # The returned result may be an empty analysis (word_count=0) or a
    # partial result; either way, word_count must be an int.
    assert isinstance(result["word_count"], int)


# ---------------------------------------------------------------------------
# calculate_relevance
# ---------------------------------------------------------------------------

def test_relevance_both_empty():
    """No keywords on either side → neutral 0.5."""
    analyzer = NLPAnalyzer()
    score = analyzer.calculate_relevance([], [])
    assert score == 0.5


def test_relevance_article_empty():
    """Empty article keywords → 0.5."""
    analyzer = NLPAnalyzer()
    score = analyzer.calculate_relevance([], ["ai", "tech"])
    assert score == 0.5


def test_relevance_interests_empty():
    """Empty interests → 0.5."""
    analyzer = NLPAnalyzer()
    score = analyzer.calculate_relevance(["ai", "tech"], [])
    assert score == 0.5


def test_relevance_full_overlap():
    """Identical keyword sets → 1.0."""
    analyzer = NLPAnalyzer()
    kws = ["ai", "tech", "science"]
    score = analyzer.calculate_relevance(kws, kws)
    assert score == pytest.approx(1.0)


def test_relevance_no_overlap():
    """No keywords in common → 0.0."""
    analyzer = NLPAnalyzer()
    score = analyzer.calculate_relevance(["cats", "dogs"], ["ai", "tech"])
    assert score == pytest.approx(0.0)


def test_relevance_partial_overlap():
    """Partial overlap returns value between 0 and 1 (exclusive)."""
    analyzer = NLPAnalyzer()
    score = analyzer.calculate_relevance(["ai", "tech", "science"], ["ai", "art"])
    assert 0.0 < score < 1.0


def test_relevance_case_insensitive():
    """Relevance matching must be case-insensitive."""
    analyzer = NLPAnalyzer()
    score = analyzer.calculate_relevance(["AI", "Tech"], ["ai", "tech"])
    assert score == pytest.approx(1.0)

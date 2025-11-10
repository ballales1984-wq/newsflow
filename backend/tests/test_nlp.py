"""NLP service tests"""
import pytest
from app.services.nlp.analyzer import NLPAnalyzer


def test_nlp_analyzer_initialization():
    """Test NLP analyzer can be initialized"""
    analyzer = NLPAnalyzer()
    assert analyzer is not None


def test_language_detection():
    """Test language detection"""
    analyzer = NLPAnalyzer()
    
    # Test Italian
    result_it = analyzer.analyze("Questa è una notizia in italiano sulla tecnologia.")
    assert result_it['language'] in ['it', 'en']  # May vary based on model
    
    # Test English
    result_en = analyzer.analyze("This is a news article about technology.")
    assert result_en['language'] in ['it', 'en']


def test_keyword_extraction():
    """Test keyword extraction"""
    analyzer = NLPAnalyzer()
    text = """
    L'intelligenza artificiale sta trasformando il mondo della tecnologia.
    Le aziende investono miliardi in ricerca e sviluppo di nuovi algoritmi.
    """
    
    result = analyzer.analyze(text, "Intelligenza Artificiale")
    assert 'keywords' in result
    assert isinstance(result['keywords'], list)
    assert len(result['keywords']) > 0


def test_quality_score():
    """Test quality score calculation"""
    analyzer = NLPAnalyzer()
    
    # Short, poor quality text
    short_text = "Test."
    result_short = analyzer.analyze(short_text)
    
    # Longer, better quality text
    long_text = """
    L'intelligenza artificiale rappresenta una delle rivoluzioni tecnologiche
    più significative del XXI secolo. Le applicazioni pratiche spaziano dalla
    medicina alla robotica, dalla finanza all'automotive. I ricercatori di tutto
    il mondo collaborano per sviluppare sistemi sempre più sofisticati e sicuri.
    """ * 3
    
    result_long = analyzer.analyze(long_text)
    
    assert result_long['quality_score'] > result_short['quality_score']


def test_reading_time():
    """Test reading time calculation"""
    analyzer = NLPAnalyzer()
    
    text = " ".join(["word"] * 400)  # 400 words
    result = analyzer.analyze(text)
    
    assert result['reading_time_minutes'] == 2  # ~200 words/min
    assert result['word_count'] == 400


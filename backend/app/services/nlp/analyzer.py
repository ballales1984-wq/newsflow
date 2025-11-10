import spacy
from typing import Dict, List, Any, Optional
from collections import Counter
import re
import logging
from langdetect import detect, LangDetectException

logger = logging.getLogger(__name__)


class NLPAnalyzer:
    """NLP analyzer for article content"""
    
    def __init__(self):
        """Initialize NLP models"""
        try:
            self.nlp_it = spacy.load("it_core_news_lg")
            logger.info("Loaded Italian spaCy model")
        except:
            logger.warning("Italian spaCy model not available")
            self.nlp_it = None
        
        try:
            self.nlp_en = spacy.load("en_core_web_lg")
            logger.info("Loaded English spaCy model")
        except:
            logger.warning("English spaCy model not available")
            self.nlp_en = None
    
    def analyze(self, text: str, title: str = "") -> Dict[str, Any]:
        """
        Perform comprehensive NLP analysis on text
        
        Args:
            text: Article content
            title: Article title
            
        Returns:
            Dictionary with analysis results
        """
        if not text:
            return self._empty_analysis()
        
        # Detect language
        language = self._detect_language(text)
        
        # Select appropriate model
        nlp = self.nlp_it if language == "it" else self.nlp_en
        if not nlp:
            return self._empty_analysis()
        
        # Process text
        full_text = f"{title} {text}" if title else text
        doc = nlp(full_text[:1000000])  # Limit to 1M chars
        
        # Extract information
        keywords = self._extract_keywords(doc, top_n=15)
        entities = self._extract_entities(doc)
        sentiment_score = self._calculate_sentiment(doc)
        quality_score = self._calculate_quality_score(text, keywords)
        
        return {
            'language': language,
            'keywords': keywords,
            'entities': entities,
            'sentiment_score': sentiment_score,
            'quality_score': quality_score,
            'word_count': len(text.split()),
            'reading_time_minutes': self._calculate_reading_time(text),
        }
    
    def _detect_language(self, text: str) -> str:
        """Detect text language"""
        try:
            lang = detect(text[:1000])
            return lang
        except LangDetectException:
            return "en"
    
    def _extract_keywords(self, doc, top_n: int = 15) -> List[str]:
        """Extract keywords using POS tagging and frequency"""
        # Filter for nouns, proper nouns, and adjectives
        words = [
            token.lemma_.lower()
            for token in doc
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ']
            and not token.is_stop
            and not token.is_punct
            and len(token.text) > 3
        ]
        
        # Count frequencies
        counter = Counter(words)
        keywords = [word for word, count in counter.most_common(top_n)]
        
        return keywords
    
    def _extract_entities(self, doc) -> Dict[str, List[str]]:
        """Extract named entities"""
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'misc': []
        }
        
        for ent in doc.ents:
            entity_text = ent.text.strip()
            if len(entity_text) < 2:
                continue
            
            if ent.label_ in ['PERSON', 'PER']:
                entities['persons'].append(entity_text)
            elif ent.label_ in ['ORG']:
                entities['organizations'].append(entity_text)
            elif ent.label_ in ['GPE', 'LOC', 'LOCATION']:
                entities['locations'].append(entity_text)
            else:
                entities['misc'].append(entity_text)
        
        # Remove duplicates and limit
        for key in entities:
            entities[key] = list(set(entities[key]))[:10]
        
        return entities
    
    def _calculate_sentiment(self, doc) -> float:
        """
        Calculate sentiment score
        Simple implementation - can be enhanced with transformers
        """
        # Placeholder - implement with sentiment model
        # For now, return neutral
        return 0.0
    
    def _calculate_quality_score(self, text: str, keywords: List[str]) -> float:
        """
        Calculate content quality score based on various factors
        
        Returns:
            Score between 0 and 1
        """
        score = 0.5  # Base score
        
        # Length factor (prefer 500-5000 words)
        word_count = len(text.split())
        if 500 <= word_count <= 5000:
            score += 0.2
        elif 200 <= word_count < 500:
            score += 0.1
        
        # Keyword diversity
        if len(keywords) >= 10:
            score += 0.15
        elif len(keywords) >= 5:
            score += 0.1
        
        # Has proper structure (paragraphs)
        paragraphs = text.split('\n\n')
        if len(paragraphs) >= 3:
            score += 0.1
        
        # Contains URLs/links (sign of references)
        if re.search(r'https?://', text):
            score += 0.05
        
        return min(score, 1.0)
    
    def _calculate_reading_time(self, text: str) -> int:
        """Calculate estimated reading time in minutes (avg 200 words/min)"""
        word_count = len(text.split())
        return max(1, round(word_count / 200))
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis result"""
        return {
            'language': 'unknown',
            'keywords': [],
            'entities': {'persons': [], 'organizations': [], 'locations': [], 'misc': []},
            'sentiment_score': 0.0,
            'quality_score': 0.0,
            'word_count': 0,
            'reading_time_minutes': 0,
        }
    
    def calculate_relevance(
        self,
        article_keywords: List[str],
        user_interests: List[str]
    ) -> float:
        """
        Calculate relevance score between article and user interests
        
        Args:
            article_keywords: Keywords from article
            user_interests: User's interest keywords
            
        Returns:
            Relevance score between 0 and 1
        """
        if not article_keywords or not user_interests:
            return 0.5
        
        # Calculate overlap
        article_set = set(k.lower() for k in article_keywords)
        interest_set = set(k.lower() for k in user_interests)
        
        overlap = len(article_set.intersection(interest_set))
        max_possible = min(len(article_set), len(interest_set))
        
        if max_possible == 0:
            return 0.5
        
        return overlap / max_possible


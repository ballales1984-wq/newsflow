"""
NLP package.

Provides the article analysis pipeline (language detection, keyword and
entity extraction, sentiment and quality scoring) and the zero-shot
category classifier. Both degrade gracefully when their optional model
dependencies (spaCy, transformers) are not installed.
"""

from .analyzer import NLPAnalyzer
from .classifier import ArticleClassifier

__all__ = ["NLPAnalyzer", "ArticleClassifier"]


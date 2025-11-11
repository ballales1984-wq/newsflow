from typing import List, Optional
import logging

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

logger = logging.getLogger(__name__)


class ArticleClassifier:
    """Classifier for article categorization using transformers"""
    
    def __init__(self):
        """Initialize classification model"""
        self.classifier = None
        
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not available, classification disabled")
            return
            
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # CPU, use 0 for GPU
            )
            logger.info("Loaded classification model")
        except Exception as e:
            logger.error(f"Error loading classification model: {e}")
    
    def classify(
        self,
        text: str,
        candidate_labels: Optional[List[str]] = None
    ) -> dict:
        """
        Classify article into categories
        
        Args:
            text: Article text (title + summary)
            candidate_labels: List of possible categories
            
        Returns:
            Dictionary with labels and scores
        """
        if not self.classifier:
            return {'labels': [], 'scores': []}
        
        if not candidate_labels:
            candidate_labels = self._get_default_categories()
        
        try:
            # Limit text length
            text = text[:512]
            
            result = self.classifier(
                text,
                candidate_labels,
                multi_label=False
            )
            
            return {
                'labels': result['labels'],
                'scores': result['scores']
            }
            
        except Exception as e:
            logger.error(f"Error classifying text: {e}")
            return {'labels': [], 'scores': []}
    
    def get_best_category(
        self,
        text: str,
        candidate_labels: Optional[List[str]] = None,
        threshold: float = 0.5
    ) -> Optional[str]:
        """
        Get the best matching category
        
        Args:
            text: Article text
            candidate_labels: List of possible categories
            threshold: Minimum confidence threshold
            
        Returns:
            Best category label or None
        """
        result = self.classify(text, candidate_labels)
        
        if not result['labels'] or not result['scores']:
            return None
        
        best_label = result['labels'][0]
        best_score = result['scores'][0]
        
        if best_score >= threshold:
            return best_label
        
        return None
    
    def _get_default_categories(self) -> List[str]:
        """Get default category labels"""
        return [
            'Technology',
            'Science',
            'Philosophy',
            'Innovation',
            'Cybersecurity',
            'Artificial Intelligence',
            'Culture',
            'Ethics',
            'Politics',
            'Society',
            'Environment',
            'Education',
            'Business',
            'Health',
            'Arts'
        ]
    
    def classify_multiple(
        self,
        texts: List[str],
        candidate_labels: Optional[List[str]] = None
    ) -> List[dict]:
        """
        Classify multiple texts
        
        Args:
            texts: List of article texts
            candidate_labels: List of possible categories
            
        Returns:
            List of classification results
        """
        results = []
        for text in texts:
            result = self.classify(text, candidate_labels)
            results.append(result)
        return results


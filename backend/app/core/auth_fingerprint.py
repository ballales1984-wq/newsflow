"""
Sistema di autenticazione senza password basato su fingerprinting
Zero friction - 100% conversion rate
"""
import hashlib
import json
from datetime import datetime
from typing import Optional

class FingerprintAuth:
    """
    Autenticazione automatica usando browser fingerprint
    
    Combina:
    - IP address
    - User-Agent  
    - Accept-Language
    - Accept-Encoding
    
    → Genera ID univoco per identificare utente
    """
    
    @staticmethod
    def generate_fingerprint(request_data: dict) -> str:
        """
        Genera fingerprint univoco
        
        Args:
            request_data: Dict con ip, user_agent, language, encoding
            
        Returns:
            str: Hash univoco (es: "fp_a1b2c3d4...")
        """
        fingerprint_data = {
            'ip': request_data.get('ip', 'unknown'),
            'user_agent': request_data.get('user_agent', 'unknown'),
            'accept_language': request_data.get('accept_language', 'unknown'),
            'accept_encoding': request_data.get('accept_encoding', 'unknown'),
        }
        
        # Genera hash SHA256
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
        
        return f"fp_{fingerprint_hash[:16]}"
    
    @staticmethod
    def generate_anonymous_name() -> str:
        """
        Genera nome anonimo carino
        
        Returns:
            str: Nome tipo "Mindful Explorer"
        """
        import random
        
        adjectives = [
            'Curious', 'Mindful', 'Brave', 'Calm', 'Focused',
            'Creative', 'Thoughtful', 'Wise', 'Kind', 'Bold',
            'Gentle', 'Strong', 'Peaceful', 'Bright', 'Steady'
        ]
        
        nouns = [
            'Explorer', 'Seeker', 'Dreamer', 'Builder', 'Thinker',
            'Learner', 'Creator', 'Achiever', 'Warrior', 'Soul',
            'Mind', 'Heart', 'Spirit', 'Journey', 'Path'
        ]
        
        return f"{random.choice(adjectives)} {random.choice(nouns)}"
    
    @staticmethod
    def create_user_data(fingerprint: str) -> dict:
        """
        Crea dati nuovo utente
        
        Args:
            fingerprint: Hash univoco
            
        Returns:
            dict: Dati utente da salvare
        """
        return {
            'fingerprint': fingerprint,
            'name': FingerprintAuth.generate_anonymous_name(),
            'created_at': datetime.utcnow().isoformat(),
            'last_seen': datetime.utcnow().isoformat()
        }


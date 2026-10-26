"""
Passwordless authentication system based on fingerprinting
Zero friction - 100% conversion rate
"""
# Passwordless, anonymous identity: instead of asking the visitor to register,
# the four request characteristics below are hashed into a stable device id.
# The identifier exists to keep the saved articles and preferences of an
# anonymous reader together across requests; it is not a credential.
import hashlib
import json
from datetime import datetime
from typing import Optional

class FingerprintAuth:
    """
    Automatic authentication using browser fingerprinting
    
    Combines:
    - IP address
    - User-Agent  
    - Accept-Language
    - Accept-Encoding
    
    → Generates unique ID to identify user
    """
    # The fingerprint is entirely client derived: the caller passes the values
    # in and nothing here checks them against the server's own view of the
    # request. Anyone able to reproduce the same four values gets the same
    # fingerprint, so it must not be treated as an authentication factor: the
    # IP changes on mobile networks, VPNs or CGNAT and the headers can be
    # spoofed at will.
    
    @staticmethod
    def generate_fingerprint(request_data: dict) -> str:
        """
        Genera fingerprint univoco
        
        Args:
            request_data: Dict con ip, user_agent, language, encoding
            
        Returns:
            str: Hash univoco (es: "fp_a1b2c3d4...")
        """
        # Missing values collapse to the literal "unknown": two clients that
        # omit different fields end up with different fingerprints, while a
        # client that omits all four shares one fingerprint with every other
        # such client.
        fingerprint_data = {
            'ip': request_data.get('ip', 'unknown'),
            'user_agent': request_data.get('user_agent', 'unknown'),
            'accept_language': request_data.get('accept_language', 'unknown'),
            'accept_encoding': request_data.get('accept_encoding', 'unknown'),
        }
        
        # Genera hash SHA256
        # sort_keys=True makes the JSON canonical, so the same values always
        # produce the same digest regardless of the dict ordering. Hashing keeps
        # the stored identifier opaque and fixed length, and avoids persisting
        # the raw IP and User-Agent strings.
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        fingerprint_hash = hashlib.sha256(fingerprint_string.encode()).hexdigest()
        
        # Only the first 16 hex characters (64 bits) of the digest are kept:
        # short enough to be used in keys and URLs, wide enough to make an
        # accidental collision negligible at this scale.
        return f"fp_{fingerprint_hash[:16]}"
    
    @staticmethod
    def generate_anonymous_name() -> str:
        """
        Genera nome anonimo carino
        
        Returns:
            str: Nome tipo "Mindful Explorer"
        """
        # The import is local so the module is only loaded when a name is
        # actually needed. random (and not secrets) is enough here: the name is
        # a cosmetic label, never an identifier and never a token.
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
        # The timestamps are ISO-8601 strings of naive UTC and not datetime
        # objects, so the caller has to convert them before writing them into a
        # DateTime column.
        return {
            'fingerprint': fingerprint,
            'name': FingerprintAuth.generate_anonymous_name(),
            'created_at': datetime.utcnow().isoformat(),
            'last_seen': datetime.utcnow().isoformat()
        }


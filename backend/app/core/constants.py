"""Shared constants, schemas, and helpers used across NewsFlow backends (main.py, main_simple.py, endpoints).
Single source of truth for categories, keyword mappings, and pagination helpers.
"""

from typing import List, Dict, Any, Optional
import html
import re


# Official 14 Categories in NewsFlow
DEFAULT_CATEGORIES: List[Dict[str, Any]] = [
    {"id": 1, "name": "Technology", "slug": "technology", "icon": "computer", "color": "#2196F3"},
    {"id": 2, "name": "Science", "slug": "science", "icon": "science", "color": "#4CAF50"},
    {"id": 3, "name": "Philosophy", "slug": "philosophy", "icon": "psychology", "color": "#9C27B0"},
    {"id": 4, "name": "Cybersecurity", "slug": "cybersecurity", "icon": "security", "color": "#F44336"},
    {"id": 5, "name": "AI", "slug": "ai", "icon": "smart_toy", "color": "#FF9800"},
    {"id": 6, "name": "Innovation", "slug": "innovation", "icon": "lightbulb", "color": "#FFEB3B"},
    {"id": 7, "name": "Culture", "slug": "culture", "icon": "palette", "color": "#E91E63"},
    {"id": 8, "name": "Ethics", "slug": "ethics", "icon": "balance", "color": "#607D8B"},
    {"id": 9, "name": "Sport", "slug": "sport", "icon": "sports_soccer", "color": "#FF5722"},
    {"id": 10, "name": "Nature", "slug": "nature", "icon": "park", "color": "#4CAF50"},
    {"id": 11, "name": "Business", "slug": "business", "icon": "business_center", "color": "#1976D2"},
    {"id": 12, "name": "Health", "slug": "health", "icon": "health_and_safety", "color": "#E91E63"},
    {"id": 13, "name": "Politics", "slug": "politics", "icon": "gavel", "color": "#9C27B0"},
    {"id": 14, "name": "Entertainment", "slug": "entertainment", "icon": "movie", "color": "#FF9800"},
]


# Keyword mapping for category matching in RSS and search filters
CATEGORY_KEYWORDS: Dict[int, List[str]] = {
    1: [
        "tech", "technology", "tecnologia", "software", "hardware", "app",
        "digital", "gadget", "device", "smartphone", "computer", "microsoft",
        "apple", "google", "meta"
    ],
    2: [
        "science", "scienza", "research", "ricerca", "study", "studio",
        "physics", "fisica", "space", "spazio", "astronomy", "astronomia",
        "nasa", "esa", "biology", "biologia"
    ],
    3: [
        "philosophy", "filosofia", "thought", "pensiero", "mind", "mente",
        "consciousness", "coscienza", "existential", "epistemology", "metaphysics"
    ],
    4: [
        "cybersecurity", "security", "sicurezza", "hacker", "malware",
        "ransomware", "breach", "vulnerability", "vulnerabilità", "exploit",
        "privacy", "attack", "attacco", "firewall", "phishing"
    ],
    5: [
        "ai", "artificial intelligence", "intelligenza artificiale",
        "machine learning", "deep learning", "neural", "llm", "chatgpt",
        "openai", "claude", "gemini", "copilot", "deepmind"
    ],
    6: [
        "innovation", "innovazione", "future", "futuro", "startup",
        "emerging", "trend", "breakthrough", "discovery", "scoperta", "invenzione"
    ],
    7: [
        "culture", "cultura", "art", "arte", "literature", "letteratura",
        "history", "storia", "society", "società", "humanities", "museum", "museo"
    ],
    8: [
        "ethics", "etica", "moral", "morale", "responsibility", "responsabilità",
        "fairness", "bias", "regulation", "regolamentazione", "governance"
    ],
    9: [
        "sport", "calcio", "football", "tennis", "formula 1", "motogp",
        "basket", "atletica", "olimpiadi", "champions league", "serie a"
    ],
    10: [
        "nature", "natura", "ambiente", "clima", "climate", "sostenibilità",
        "sustainability", "animali", "wildlife", "foresta", "oceano"
    ],
    11: [
        "business", "economia", "finanza", "market", "mercato", "company",
        "azienda", "investimenti", "startup", "borsa", "pil", "inflazione"
    ],
    12: [
        "health", "salute", "medical", "medico", "hospital", "ospedale",
        "medicine", "sanità", "ricerca medica", "farmaci", "benessere"
    ],
    13: [
        "politics", "politica", "government", "governo", "election",
        "elezioni", "parliament", "parlamento", "legge", "ministro", "ue", "esteri"
    ],
    14: [
        "entertainment", "intrattenimento", "movie", "film", "cinema",
        "music", "musica", "tv", "show", "serie tv", "spettacolo", "celebrità"
    ],
}


def clean_html(text: Optional[str]) -> str:
    """Rimuove tutti i tag HTML e decodifica entità HTML dal testo"""
    if not text:
        return ""

    # Rimuove tutti i tag HTML
    text = re.sub(r"<[^>]+>", "", text)

    # Decodifica entità HTML
    try:
        text = html.unescape(text)
    except Exception:
        text = (
            text.replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&#39;", "'")
            .replace("&apos;", "'")
            .replace("&#8217;", "'")
            .replace("&#8216;", "'")
            .replace("&#8220;", '"')
            .replace("&#8221;", '"')
            .replace("&#8230;", "...")
            .replace("&mdash;", "—")
            .replace("&ndash;", "–")
        )

    # Rimuove spazi multipli
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_pagination(items: list, total: int, skip: int, limit: int) -> Dict[str, Any]:
    """Standardizza il formato di risposta paginata su tutti gli endpoint"""
    return {
        "items": items,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "size": len(items),
        "pages": (total + limit - 1) // limit if limit > 0 else 1,
    }

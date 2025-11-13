"""Test caricamento articoli dal backend"""
import sys
sys.path.insert(0, '.')

from app.main_simple import _load_articles

articles = _load_articles()
print(f"✅ Articoli caricati: {len(articles)}")
print(f"\nPrime 3 titoli:")
for i, a in enumerate(articles[:3], 1):
    print(f"{i}. {a.get('title', 'N/A')[:70]}")


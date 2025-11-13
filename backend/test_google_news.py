"""Test script per verificare il collector Google News"""
import sys
import os

# Aggiungi il path del backend
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.services.collectors.google_news_collector import GoogleNewsCollector
    
    print("🔍 Test del Google News Collector...")
    print("=" * 50)
    
    collector = GoogleNewsCollector()
    
    # Test 1: Raccolta da topic TECHNOLOGY
    print("\n📋 Test 1: Raccolta da topic TECHNOLOGY")
    try:
        articles = collector.collect(
            query=None,
            language='it',
            country='IT',
            max_articles=3,
            topic='TECHNOLOGY'
        )
        print(f"✅ Raccolti {len(articles)} articoli")
        if articles:
            print(f"\nPrimo articolo:")
            print(f"  Titolo: {articles[0].get('title', 'N/A')[:80]}")
            print(f"  Autore: {articles[0].get('author', 'N/A')}")
            print(f"  URL: {articles[0].get('url', 'N/A')[:80]}")
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Raccolta da query
    print("\n🔍 Test 2: Raccolta da query 'intelligenza artificiale'")
    try:
        articles = collector.collect(
            query='intelligenza artificiale',
            language='it',
            country='IT',
            max_articles=3
        )
        print(f"✅ Raccolti {len(articles)} articoli")
        if articles:
            print(f"\nPrimo articolo:")
            print(f"  Titolo: {articles[0].get('title', 'N/A')[:80]}")
            print(f"  Autore: {articles[0].get('author', 'N/A')}")
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✅ Test completato!")
    
except ImportError as e:
    print(f"❌ Errore di importazione: {e}")
    import traceback
    traceback.print_exc()


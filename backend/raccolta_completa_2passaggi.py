"""Script completo per raccolta notizie in 2 passaggi:
   1. Raccolta notizie (veloce)
   2. Generazione spiegazioni AI (può richiedere tempo)
"""
import sys
import os
import io
import time

# Fix encoding per Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Aggiungi il path del backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imposta variabili d'ambiente se necessario
os.environ.setdefault("DATABASE_URL", "sqlite:///./newsflow.db")
os.environ.setdefault("SECRET_KEY", "dev-key")

print("=" * 70)
print("RACCOLTA COMPLETA NEWSFLOW - 2 PASSAGGI")
print("=" * 70)

try:
    from app.main_simple import trigger_news_collection, trigger_explanations_generation
    
    # PASSAGGIO 1: Raccolta notizie
    print("\n" + "=" * 70)
    print("PASSAGGIO 1: Raccolta notizie da tutte le fonti...")
    print("=" * 70)
    
    result1 = trigger_news_collection()
    
    if isinstance(result1, dict) and result1.get('success'):
        print(f"\n✅ PASSAGGIO 1 COMPLETATO!")
        print(f"   - Articoli raccolti: {result1.get('total_articles', 0)}")
        print(f"   - Aggiornato alle: {result1.get('updated_at', 'N/A')}")
        
        # PASSAGGIO 2: Generazione spiegazioni AI
        print("\n" + "=" * 70)
        print("PASSAGGIO 2: Generazione spiegazioni AI...")
        print("=" * 70)
        print("(Questo passaggio può richiedere tempo)")
        
        result2 = trigger_explanations_generation()
        
        if isinstance(result2, dict) and result2.get('success'):
            print(f"\n✅ PASSAGGIO 2 COMPLETATO!")
            print(f"   - Spiegazioni generate: {result2.get('explanations_generated', 0)}")
            print(f"   - Totale articoli: {result2.get('total_articles', 0)}")
            print(f"   - Aggiornato alle: {result2.get('updated_at', 'N/A')}")
        else:
            print(f"\n⚠️  PASSAGGIO 2 con errori:")
            if isinstance(result2, dict):
                print(f"   - Errore: {result2.get('error', 'Unknown')}")
            else:
                print(f"   - Risultato: {result2}")
        
        print("\n" + "=" * 70)
        print("✅ RACCOLTA COMPLETA TERMINATA!")
        print("=" * 70)
        print(f"📊 Riepilogo:")
        print(f"   - Articoli raccolti: {result1.get('total_articles', 0)}")
        print(f"   - Spiegazioni generate: {result2.get('explanations_generated', 0) if isinstance(result2, dict) else 0}")
        print("\n✨ NewsFlow completamente aggiornato!")
        
    else:
        print(f"\n❌ ERRORE nel PASSAGGIO 1:")
        if isinstance(result1, dict):
            print(f"   - Errore: {result1.get('error', 'Unknown')}")
        else:
            print(f"   - Risultato: {result1}")
        print("\n⚠️  Impossibile procedere con il PASSAGGIO 2")
        sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Errore durante la raccolta completa: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


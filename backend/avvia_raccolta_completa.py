"""Script per avviare la raccolta completa delle notizie con tutte le nuove fonti"""
import sys
import os
import io

# Fix encoding per Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Aggiungi il path del backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imposta variabili d'ambiente se necessario
os.environ.setdefault("DATABASE_URL", "sqlite:///./newsflow.db")
os.environ.setdefault("SECRET_KEY", "dev-key")

print("Avvio raccolta completa notizie con tutte le fonti...")
print("=" * 70)

try:
    # Importa la funzione di raccolta dall'endpoint
    from app.main_simple import trigger_news_collection
    
    # Avvia la raccolta
    result = trigger_news_collection()
    
    print("\n" + "=" * 70)
    print("✅ RACCOLTA COMPLETATA!")
    print("=" * 70)
    
    if isinstance(result, dict):
        print(f"📊 Risultato:")
        print(f"   - Successo: {result.get('success', False)}")
        print(f"   - Messaggio: {result.get('message', 'N/A')}")
        print(f"   - Totale articoli: {result.get('total_articles', 0)}")
        print(f"   - Spiegazioni generate: {result.get('explanations_generated', 0)}")
        print(f"   - Aggiornato alle: {result.get('updated_at', 'N/A')}")
    else:
        print(f"📊 Risultato: {result}")
    
    print("\n✨ NewsFlow aggiornato con successo!")
    
except Exception as e:
    print(f"\n❌ Errore durante la raccolta: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


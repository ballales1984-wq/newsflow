"""Script per generare spiegazioni AI per articoli esistenti (secondo passaggio)"""
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

print("Generazione spiegazioni AI per articoli esistenti...")
print("=" * 70)

try:
    # Importa la funzione di generazione spiegazioni
    from app.main_simple import trigger_explanations_generation
    
    # Avvia la generazione
    result = trigger_explanations_generation()
    
    print("\n" + "=" * 70)
    print("Generazione spiegazioni completata!")
    print("=" * 70)
    
    if isinstance(result, dict):
        print(f"Risultato:")
        print(f"   - Successo: {result.get('success', False)}")
        print(f"   - Messaggio: {result.get('message', 'N/A')}")
        print(f"   - Spiegazioni generate: {result.get('explanations_generated', 0)}")
        print(f"   - Totale articoli: {result.get('total_articles', 0)}")
        print(f"   - Aggiornato alle: {result.get('updated_at', 'N/A')}")
        if result.get('error'):
            print(f"   - Errore: {result.get('error')}")
    else:
        print(f"Risultato: {result}")
    
    print("\nNewsFlow aggiornato con spiegazioni AI!")
    
except Exception as e:
    print(f"\nErrore durante la generazione: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


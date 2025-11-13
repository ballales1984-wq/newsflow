"""Script per generare spiegazioni AI con limite di articoli per evitare timeout"""
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

print("Generazione spiegazioni AI (limite 50 articoli per volta)...")
print("=" * 70)

try:
    from app.main_simple import trigger_explanations_generation
    
    result = trigger_explanations_generation()
    
    print("\n" + "=" * 70)
    if isinstance(result, dict) and result.get('success'):
        print("✅ Completato!")
        print(f"   - Spiegazioni generate: {result.get('explanations_generated', 0)}")
        print(f"   - Totale articoli: {result.get('total_articles', 0)}")
        if result.get('explanations_generated', 0) < result.get('articles_with_explanations', 0):
            remaining = result.get('articles_with_explanations', 0) - result.get('explanations_generated', 0)
            print(f"   - Articoli rimanenti: {remaining} (esegui di nuovo per continuare)")
    else:
        print("⚠️  Completato con errori:")
        if isinstance(result, dict):
            print(f"   - Errore: {result.get('error', 'Unknown')}")
    
except Exception as e:
    print(f"\n❌ Errore: {e}")
    import traceback
    traceback.print_exc()


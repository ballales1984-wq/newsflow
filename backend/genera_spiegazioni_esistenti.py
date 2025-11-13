"""
Script per generare spiegazioni AI per articoli esistenti
Esegui questo script una volta per generare spiegazioni per tutti gli articoli già presenti
"""
import json
import os
from app.ai_explainer import generate_explanation

def generate_explanations_for_existing_articles():
    """Genera spiegazioni AI per tutti gli articoli esistenti"""
    
    # Carica articoli esistenti
    json_file = 'final_news_italian.json'
    
    if not os.path.exists(json_file):
        print(f"❌ File {json_file} non trovato!")
        return
    
    print(f"📥 Caricamento articoli da {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get('items', [])
    print(f"✅ Caricati {len(articles)} articoli")
    
    # Genera spiegazioni
    print(f"\n🤖 Generazione spiegazioni AI per {len(articles)} articoli...")
    print("   (Questo può richiedere diversi minuti)\n")
    
    explanations_generated = 0
    explanations_skipped = 0
    
    for i, article in enumerate(articles):
        try:
            # Controlla se già ha spiegazioni
            has_explanations = (
                article.get('explanation_quick') or 
                article.get('explanation_standard') or 
                article.get('explanation_deep')
            )
            
            if has_explanations:
                explanations_skipped += 1
                if (i + 1) % 20 == 0:
                    print(f"   ⏭️  {i+1}/{len(articles)} (spiegazioni già presenti)...")
                continue
            
            # Genera spiegazioni
            print(f"   [{i+1}/{len(articles)}] {article.get('title', '')[:60]}...")
            
            article['explanation_quick'] = generate_explanation(article, 'quick')
            article['explanation_standard'] = generate_explanation(article, 'standard')
            article['explanation_deep'] = generate_explanation(article, 'deep')
            
            explanations_generated += 1
            
            # Salva ogni 10 articoli (backup incrementale)
            if (i + 1) % 10 == 0:
                data['items'] = articles
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"   💾 Backup salvato ({i+1}/{len(articles)})...")
            
        except Exception as e:
            print(f"   ⚠️  Errore articolo {i+1}: {e}")
            continue
    
    # Salva finale
    print(f"\n💾 Salvataggio finale...")
    data['items'] = articles
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅✅✅ COMPLETATO!")
    print(f"   Articoli processati: {len(articles)}")
    print(f"   Spiegazioni generate: {explanations_generated}")
    print(f"   Spiegazioni già presenti: {explanations_skipped}")
    print(f"\n💡 Le spiegazioni sono ora nel JSON e saranno caricate istantaneamente!")

if __name__ == "__main__":
    generate_explanations_for_existing_articles()


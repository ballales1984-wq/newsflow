"""Modulo shared per aggiornare il digest automaticamente quando cambiano le notizie"""
import json
import os
from datetime import datetime

# Percorsi dove salvare il digest
DIGEST_PATHS = [
    'frontend/src/assets/digest.json',
    'api/digest.json',
    'backend/digest.json'
]

# Categorie per la classificazione automatica
CATEGORIES = {
    "💻 Tecnologia": ["technology", "tech", "computer", "software", "app", "quantum", "hardware", "coding"],
    "🤖 Intelligenza Artificiale": ["ai", "artificial intelligence", "chatgpt", "gpt", "machine learning", "llm", "deepmind", "ia", "neural", "model"],
    "🔒 Cybersecurity": ["security", "cyber", "breach", "hack", "malware", "exploit", "vulnerability", "attack", "sicurezza"],
    "🔬 Scienza": ["science", "research", "discovery", "study", "physics", "biology", "esplosione", "ricerca", "scoperta"],
    "💼 Business": ["business", "economy", "market", "company", "startup", "finance", "economia", "azienda", "investimenti"],
    "🌍 Politica": ["politics", "government", "election", "parliament", "biden", "trump", "politica", "elezioni", "governo"],
    "🎬 Intrattenimento": ["film", "movie", "music", "entertainment", "celebrity", "oscar", "cinema", "musica", "serie"],
    "🏥 Salute": ["health", "medical", "vaccine", "disease", "doctor", "salute", "medicina", "medico", "ospedale"],
    "🌍 Ambiente": ["environment", "climate", "green", "eco", "nature", "ambiente", "clima", "riscaldamento"],
}

def categorize_article(article):
    """Assegna una categoria in base a title e summary"""
    title = (article.get('title', '') + ' ' + article.get('summary', '')).lower()
    
    for category, keywords in CATEGORIES.items():
        if any(kw in title for kw in keywords):
            return category
    
    return "💻 Tecnologia"  # fallback

def update_digest_from_articles(articles_file='final_news_italian.json', max_articles_per_category=5):
    """
    Aggiorna il digest con gli articoli attuali.
    Viene chiamato automaticamente quando vengono caricate nuove notizie.
    
    Args:
        articles_file: path del file JSON con gli articoli
        max_articles_per_category: max articoli per categoria nel digest
    
    Returns:
        bool: True se aggiornamento riuscito, False altrimenti
    """
    try:
        # Carica gli articoli
        articles = []
        
        # Prova diverse locazioni del file
        possible_paths = [
            articles_file,
            os.path.join('backend', articles_file),
            os.path.join('api', articles_file),
            os.path.join(os.getcwd(), articles_file)
        ]
        
        articles_loaded = False
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    articles = data.get('items', [])
                    articles_loaded = True
                    print(f"📰 Caricati {len(articles)} articoli da: {path}")
                    break
        
        if not articles_loaded:
            print(f"⚠️  File articoli non trovato: {articles_file}")
            return False
        
        if not articles:
            print("⚠️  Nessun articolo disponibile per il digest")
            return False
        
        # Raggruppa articoli per categoria
        categorized = {}
        for article in articles[:100]:  # Prendi i primi 100
            cat = categorize_article(article)
            if cat not in categorized:
                categorized[cat] = []
            
            # Crea una versione condensata dell'articolo per il digest
            article_digest = {
                "title": article.get('title', '')[:120],
                "description": article.get('summary', '')[:200] if article.get('summary') else article.get('description', '')[:200]
            }
            
            categorized[cat].append(article_digest)
        
        # Costruisci il digest
        digest = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "digest": []
        }
        
        for category, category_articles in sorted(categorized.items()):
            digest["digest"].append({
                "category": category,
                "articles": category_articles[:max_articles_per_category]
            })
        
        # Salva il digest in tutti i path
        saved_count = 0
        for path in DIGEST_PATHS:
            try:
                # Crea directory se non esiste
                os.makedirs(os.path.dirname(path), exist_ok=True)
                
                # Aggiorna il percorso se siamo nella directory backend
                if os.getcwd().endswith('backend'):
                    adjusted_path = path.replace('frontend/', '../frontend/')
                    adjusted_path = adjusted_path.replace('api/', '../api/')
                else:
                    adjusted_path = path
                
                with open(adjusted_path, 'w', encoding='utf-8') as f:
                    json.dump(digest, f, ensure_ascii=False, indent=2)
                
                print(f"   ✅ Digest salvato in: {adjusted_path}")
                saved_count += 1
            except Exception as e:
                print(f"   ⚠️  Errore salvataggio {path}: {e}")
        
        if saved_count > 0:
            print(f"\n✅ Digest aggiornato automaticamente!")
            print(f"   Data: {digest['date']}")
            print(f"   Categorie: {len(digest['digest'])}")
            for cat_obj in digest['digest']:
                print(f"   - {cat_obj['category']}: {len(cat_obj['articles'])} articoli")
            return True
        else:
            print("⚠️  Nessun digest salvato")
            return False
            
    except Exception as e:
        print(f"❌ Errore nell'aggiornamento digest: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test: esegui direttamente per aggiornare digest
    update_digest_from_articles()

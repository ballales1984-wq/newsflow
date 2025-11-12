"""Script per aggiornare le notizie - VELOCE"""
import json
import os
from datetime import datetime

print("🔄 Aggiornando notizie...")
print("=" * 50)

# Carica le nuove notizie raccolte
if os.path.exists('all_sources_news.json'):
    with open('all_sources_news.json', 'r', encoding='utf-8') as f:
        new_data = json.load(f)
        new_articles = new_data.get('items', [])
    
    print(f"📰 Trovate {len(new_articles)} nuove notizie")
    
    # Aggiorna final_news_italian.json
    output_data = {
        "items": new_articles,
        "total": len(new_articles),
        "page": 1,
        "size": len(new_articles),
        "pages": 1,
        "updated_at": datetime.now().isoformat()
    }
    
    with open('final_news_italian.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Aggiornato: final_news_italian.json")
    print(f"📊 Totale notizie: {len(new_articles)}")
    print(f"🕐 Aggiornato alle: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🎉 Notizie aggiornate! Riavvia il backend per vedere le nuove notizie.")
    
else:
    print("❌ File all_sources_news.json non trovato!")
    print("💡 Esegui prima: python collect_all_sources.py")


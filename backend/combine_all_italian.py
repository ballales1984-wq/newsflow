"""Combina notizie italiane + internazionali tradotte"""
import json

print("🔗 Combinando tutte le notizie in italiano...")

# Carica italiane
with open('italian_priority_news.json', 'r', encoding='utf-8') as f:
    italian_data = json.load(f)
    italian_news = italian_data.get('items', [])

# Carica tradotte
with open('world_news_translated.json', 'r', encoding='utf-8') as f:
    translated_data = json.load(f)
    translated_news = translated_data.get('items', [])

# Combina: prima italiane, poi tradotte
all_news = italian_news + translated_news

# Ri-numera gli ID
for i, article in enumerate(all_news, 1):
    article['id'] = i

print(f"🇮🇹 Notizie italiane: {len(italian_news)}")
print(f"🌍 Notizie tradotte: {len(translated_news)}")
print(f"📊 TOTALE: {len(all_news)} notizie")
print(f"\n✅ Tutte in ITALIANO!")

# Salva
with open('final_news_italian.json', 'w', encoding='utf-8') as f:
    json.dump({
        "items": all_news,
        "total": len(all_news),
        "page": 1,
        "size": 100,
        "pages": 1
    }, f, indent=2, ensure_ascii=False)

print(f"\n💾 Salvate in: final_news_italian.json")
print(f"🎉 Pronto per l'app!")


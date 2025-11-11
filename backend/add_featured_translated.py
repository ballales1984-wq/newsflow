"""Aggiunge notizie tradotte come featured per avere un mix"""
import json

print("📰 Aggiungendo notizie tradotte come featured...")

# Carica
with open('final_news_italian.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    articles = data['items']

# IDs delle notizie tradotte da rendere featured (prime 3 tradotte)
translated_to_feature = []

for article in articles:
    if article.get('original_language') == 'en' and len(translated_to_feature) < 3:
        translated_to_feature.append(article['id'])
        article['is_featured'] = True
        print(f"✅ Featured: {article['title'][:60]}... (ID: {article['id']})")

print(f"\n📊 Aggiunte {len(translated_to_feature)} notizie tradotte come featured")

# Salva
with open('final_news_italian.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("💾 Salvato!")
print("\n🌍 Ora le featured includeranno notizie dal mondo!")


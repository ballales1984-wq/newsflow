import json
import os

# Controlla video disponibili
print("🔍 CONTROLLO VIDEO E IMMAGINI")
print("")

video_dir = "youtube_videos"
if os.path.exists(video_dir):
    videos = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    if videos:
        print("✅ Video disponibili:")
        for video in videos:
            video_path = os.path.join(video_dir, video)
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            print(f"   - {video} ({size_mb:.2f} MB)")
        
        if "newsflow_live_4h.mp4" in videos:
            print("\n✅ Video TG 4h trovato!")
        else:
            print("\n⚠️  Video TG 4h NON trovato")
    else:
        print("❌ Nessun video trovato")
else:
    print("❌ Cartella youtube_videos non trovata")

print("")

# Controlla notizie con immagini
if os.path.exists("final_news_italian.json"):
    with open("final_news_italian.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        articles = data.get('items', [])
        
        articles_with_images = [a for a in articles if a.get('image_url')]
        
        print("📊 STATISTICHE NOTIZIE:")
        print(f"   Totale notizie: {len(articles)}")
        print(f"   Notizie con immagini: {len(articles_with_images)}")
        print(f"   Percentuale: {len(articles_with_images)/len(articles)*100:.1f}%")
        
        if articles_with_images:
            print("\n✅ Esempi notizie con immagini:")
            for i, article in enumerate(articles_with_images[:5]):
                title = article.get('title', '')[:60]
                image_url = article.get('image_url', '')[:80]
                print(f"   {i+1}. {title}...")
                print(f"      Immagine: {image_url}...")
        else:
            print("\n⚠️  Nessuna notizia con immagini trovata!")
else:
    print("❌ File final_news_italian.json non trovato")

print("")
print("💡 Il generatore video include già le immagini delle notizie!")
print("   Se una notizia ha image_url, viene scaricata e usata come sfondo")


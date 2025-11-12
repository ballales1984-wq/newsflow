"""
Generatore video corti da 2 minuti per YouTube Live ogni 20 minuti
Seleziona solo notizie con immagini e usa voce narrante femminile
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from youtube_video_generator import YouTubeVideoGenerator

def filter_articles_with_images(articles: List[Dict]) -> List[Dict]:
    """Filtra solo articoli che hanno immagini"""
    filtered = []
    for article in articles:
        image_url = article.get('image_url')
        if image_url and image_url.strip():
            # Verifica che l'URL sia valido
            if image_url.startswith('http'):
                filtered.append(article)
    return filtered

def create_short_video_2min(articles: List[Dict], output_dir: str = "youtube_videos") -> Optional[str]:
    """
    Crea video corto da 2 minuti con solo notizie che hanno immagini
    
    Args:
        articles: Lista di articoli
        output_dir: Directory di output
    
    Returns:
        Percorso del video creato
    """
    # Filtra solo articoli con immagini
    articles_with_images = filter_articles_with_images(articles)
    
    if not articles_with_images:
        print("❌ Nessun articolo con immagini trovato!")
        return None
    
    print(f"📸 Trovati {len(articles_with_images)} articoli con immagini")
    print(f"   Su {len(articles)} articoli totali")
    
    # Crea generatore video
    generator = YouTubeVideoGenerator(articles_with_images, output_dir=output_dir)
    
    # Crea video da 2 minuti
    # Stima: ~4-5 articoli per 2 minuti (ogni articolo ~25-30 secondi)
    target_duration_minutes = 2
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"newsflow_2min_{timestamp}.mp4"
    
    try:
        video_path = generator.create_video(
            target_duration_minutes=target_duration_minutes,
            output_filename=output_filename,
            only_with_images=True  # Solo notizie con immagini
        )
        
        if video_path:
            print(f"✅ Video corto creato: {video_path}")
            print(f"   Durata target: {target_duration_minutes} minuti")
            print(f"   Articoli usati: {len(articles_with_images)}")
        
        return video_path
    finally:
        generator.cleanup()


def create_scheduled_short_videos_every_20min():
    """
    Crea video corti programmati ogni 20 minuti per tutta la giornata
    """
    import schedule
    import time
    
    def create_and_upload_video():
        """Crea e carica video corto"""
        print(f"🎬 Creo video corto alle {datetime.now().strftime('%H:%M')}...")
        
        # Carica articoli dal file JSON
        backend_path = os.path.dirname(os.path.abspath(__file__))
        news_file = os.path.join(backend_path, 'final_news_italian.json')
        
        if not os.path.exists(news_file):
            print(f"❌ File notizie non trovato: {news_file}")
            return
        
        with open(news_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('items', [])
        
        # Crea video corto
        video_path = create_short_video_2min(articles)
        
        if video_path:
            print(f"✅ Video pronto: {video_path}")
            # Qui puoi aggiungere upload automatico su YouTube se necessario
            # upload_to_youtube(video_path)
    
    # Programma ogni 20 minuti (00:00, 00:20, 00:40, 01:00, ...)
    for hour in range(24):
        for minute in [0, 20, 40]:
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(create_and_upload_video)
    
    print(f"✅ Programmazione completata: video ogni 20 minuti")
    print(f"   Totale: 72 video al giorno")
    
    # Esegui scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)  # Controlla ogni minuto


if __name__ == "__main__":
    # Test
    backend_path = os.path.dirname(os.path.abspath(__file__))
    news_file = os.path.join(backend_path, 'final_news_italian.json')
    
    if os.path.exists(news_file):
        with open(news_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('items', [])
        
        video_path = create_short_video_2min(articles)
        if video_path:
            print(f"✅ Test completato: {video_path}")
    else:
        print(f"❌ File non trovato: {news_file}")


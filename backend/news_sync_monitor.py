"""
Sistema di sincronizzazione automatica per video YouTube Live
Monitora le notizie e rigenera il video quando vengono aggiornate
"""
import os
import json
import time
from datetime import datetime
from typing import Optional
import hashlib

class NewsSyncMonitor:
    """Monitora le notizie e rigenera il video quando vengono aggiornate"""
    
    def __init__(self, news_file: str = "final_news_italian.json", video_file: str = None):
        self.news_file = news_file
        self.video_file = video_file or "youtube_videos/newsflow_live_4h.mp4"
        self.last_hash = None
        self.last_update_time = None
        
    def get_news_hash(self) -> Optional[str]:
        """Calcola hash delle notizie per rilevare cambiamenti"""
        if not os.path.exists(self.news_file):
            return None
        
        try:
            with open(self.news_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Crea hash basato su contenuto e timestamp
                content = json.dumps(data, sort_keys=True)
                return hashlib.md5(content.encode()).hexdigest()
        except Exception as e:
            print(f"Errore lettura notizie: {e}")
            return None
    
    def check_news_updated(self) -> bool:
        """Controlla se le notizie sono state aggiornate"""
        current_hash = self.get_news_hash()
        
        if current_hash is None:
            return False
        
        if self.last_hash is None:
            # Prima volta, salva hash
            self.last_hash = current_hash
            self.last_update_time = datetime.now()
            return False
        
        if current_hash != self.last_hash:
            # Notizie aggiornate!
            self.last_hash = current_hash
            self.last_update_time = datetime.now()
            return True
        
        return False
    
    def get_news_update_time(self) -> Optional[datetime]:
        """Ottiene timestamp dell'ultimo aggiornamento delle notizie"""
        if not os.path.exists(self.news_file):
            return None
        
        try:
            with open(self.news_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                updated_at = data.get('updated_at')
                if updated_at:
                    return datetime.fromisoformat(updated_at)
        except:
            pass
        
        # Fallback: usa modificazione file
        try:
            mtime = os.path.getmtime(self.news_file)
            return datetime.fromtimestamp(mtime)
        except:
            return None
    
    def should_regenerate_video(self, check_interval_minutes: int = 5) -> bool:
        """Controlla se il video deve essere rigenerato"""
        # Controlla se le notizie sono state aggiornate
        if self.check_news_updated():
            print(f"Notizie aggiornate! Hash cambiato.")
            return True
        
        # Controlla se il video esiste
        if not os.path.exists(self.video_file):
            print(f"Video non trovato: {self.video_file}")
            return True
        
        # Controlla se il video è più vecchio delle notizie
        video_mtime = os.path.getmtime(self.video_file)
        video_time = datetime.fromtimestamp(video_mtime)
        news_update_time = self.get_news_update_time()
        
        if news_update_time and news_update_time > video_time:
            print(f"Notizie più recenti del video!")
            return True
        
        return False


def create_4h_live_video(articles: list, output_path: str = "youtube_videos/newsflow_live_4h.mp4") -> Optional[str]:
    """Crea un video di 4 ore per YouTube Live"""
    try:
        from youtube_video_generator import YouTubeVideoGenerator
        
        generator = YouTubeVideoGenerator(articles, output_dir="youtube_videos")
        
        try:
            print(f"Creo video TG di 4 ore (240 minuti)...")
            video_path = generator.create_live_video(duration_minutes=240, output_filename=os.path.basename(output_path))
            
            if video_path and os.path.exists(video_path):
                # Sposta/rinomina se necessario
                if video_path != output_path:
                    import shutil
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    shutil.move(video_path, output_path)
                
                return output_path
            
            return None
        finally:
            try:
                generator.cleanup()
            except:
                pass
                
    except Exception as e:
        print(f"Errore creazione video: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Test
    monitor = NewsSyncMonitor()
    print(f"Hash iniziale: {monitor.get_news_hash()}")
    print(f"Notizie aggiornate: {monitor.check_news_updated()}")


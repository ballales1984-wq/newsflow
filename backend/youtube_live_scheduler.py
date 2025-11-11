"""
Sistema di programmazione YouTube Live con auto-streaming
Crea video programmati per orari specifici e fa live streaming automatico
"""
import os
import json
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import subprocess

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False


class YouTubeLiveScheduler:
    """Sistema di scheduling per YouTube Live"""
    
    def __init__(self, articles: List[Dict], youtube_credentials_path: str = None):
        self.articles = articles
        self.youtube_credentials_path = youtube_credentials_path
        self.scheduled_streams = []
        
    def create_programmed_video(self, time_slot: str, duration_minutes: int = 30) -> Optional[str]:
        """
        Crea video programmato per uno slot temporale
        
        Args:
            time_slot: 'morning', 'afternoon', 'evening', 'night'
            duration_minutes: Durata del video
        """
        from youtube_video_generator import YouTubeVideoGenerator
        
        # Filtra articoli per slot temporale (es. notizie più recenti per mattina)
        filtered_articles = self._filter_articles_by_time_slot(self.articles, time_slot)
        
        generator = YouTubeVideoGenerator(filtered_articles)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"newsflow_{time_slot}_{timestamp}.mp4"
        
        try:
            video_path = generator.create_video(
                target_duration_minutes=duration_minutes,
                output_filename=output_filename
            )
            return video_path
        finally:
            generator.cleanup()
    
    def _filter_articles_by_time_slot(self, articles: List[Dict], time_slot: str) -> List[Dict]:
        """Filtra articoli per slot temporale"""
        # Ordina per data pubblicazione (più recenti prima)
        sorted_articles = sorted(
            articles,
            key=lambda x: x.get('published_at', ''),
            reverse=True
        )
        
        # Per ora restituisce tutti, ma puoi filtrare per categoria/tipo
        return sorted_articles
    
    def schedule_live_stream(self, hour: int, minute: int = 0, duration_minutes: int = 30):
        """
        Programma un live stream per un orario specifico
        
        Args:
            hour: Ora (0-23)
            minute: Minuto (0-59)
            duration_minutes: Durata del live
        """
        def job():
            print(f"🎥 Avvio live stream alle {hour:02d}:{minute:02d}")
            time_slot = self._get_time_slot(hour)
            video_path = self.create_programmed_video(time_slot, duration_minutes)
            
            if video_path:
                self.start_youtube_live(video_path, time_slot)
        
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job)
        self.scheduled_streams.append({
            "hour": hour,
            "minute": minute,
            "duration": duration_minutes
        })
        print(f"✅ Live programmato alle {hour:02d}:{minute:02d}")
    
    def _get_time_slot(self, hour: int) -> str:
        """Determina slot temporale dall'ora"""
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def start_youtube_live(self, video_path: str, time_slot: str):
        """Avvia live streaming su YouTube"""
        if not YOUTUBE_API_AVAILABLE:
            print("❌ YouTube API non disponibile per live streaming")
            return False
        
        # Implementazione richiede YouTube Live API configurata
        print(f"📡 Avvio live streaming: {video_path}")
        print("   ⚠️  Richiede configurazione YouTube Live API")
        return False
    
    def run_scheduler(self):
        """Esegue il scheduler continuamente"""
        print("🔄 Scheduler YouTube Live avviato...")
        print(f"📅 Live programmati: {len(self.scheduled_streams)}")
        for stream in self.scheduled_streams:
            print(f"   - {stream['hour']:02d}:{stream['minute']:02d} ({stream['duration']} min)")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Controlla ogni minuto


def create_daily_schedule():
    """Crea programmazione giornaliera standard"""
    # Esempio: Live ogni 4 ore
    schedule_times = [
        (8, 0, 30),   # Mattina: 8:00 - 30 min
        (12, 0, 30),  # Pranzo: 12:00 - 30 min
        (18, 0, 30),  # Sera: 18:00 - 30 min
        (22, 0, 60),  # Notte: 22:00 - 60 min
    ]
    return schedule_times


if __name__ == "__main__":
    import sys
    
    # Carica programmazione da file
    scheduler = YouTubeLiveScheduler()
    
    if not scheduler.scheduled_streams:
        print("⚠️  Nessuna programmazione trovata!")
        print("   Esegui PROGRAMMA_YOUTUBE_LIVE.ps1 per crearne una")
        sys.exit(1)
    
    # Programma tutti i live trovati nel file
    for stream in scheduler.scheduled_streams:
        scheduler.schedule_live_stream(
            stream['hour'],
            stream['minute'],
            stream['duration_minutes']
        )
    
    # Avvia scheduler
    try:
        scheduler.run_scheduler()
    except KeyboardInterrupt:
        print("\n\n⏹️  Scheduler fermato dall'utente")
        sys.exit(0)


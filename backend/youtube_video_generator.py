"""
Generatore automatico di video YouTube per NewsFlow
Crea video con notizie, immagini e voce narrante
"""
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import tempfile

try:
    from moviepy.editor import (
        VideoFileClip, ImageClip, TextClip, CompositeVideoClip,
        concatenate_videoclips, AudioFileClip
    )
    MOVIEPY_AVAILABLE = True
except ImportError as e:
    MOVIEPY_AVAILABLE = False
    VideoFileClip = None
    ImageClip = None
    TextClip = None
    CompositeVideoClip = None
    concatenate_videoclips = None
    AudioFileClip = None
    print(f"⚠️  moviepy non installato: {e}. Installa con: pip install moviepy")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️  gTTS non installato. Installa con: pip install gtts")

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("⚠️  YouTube API non installato. Installa con: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")


class YouTubeVideoGenerator:
    """Genera video YouTube automatici dalle notizie"""
    
    def __init__(self, articles: List[Dict], output_dir: str = "youtube_videos"):
        self.articles = articles
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.temp_files = []
        
    def download_image(self, image_url: str) -> Optional[str]:
        """Scarica immagine da URL"""
        if not image_url:
            return None
        
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, suffix='.jpg', dir=self.output_dir
                )
                temp_file.write(response.content)
                temp_file.close()
                self.temp_files.append(temp_file.name)
                return temp_file.name
        except Exception as e:
            print(f"⚠️  Errore download immagine {image_url}: {e}")
        return None
    
    def text_to_speech(self, text: str, lang: str = 'it') -> Optional[str]:
        """Converte testo in audio usando gTTS"""
        if not GTTS_AVAILABLE:
            return None
        
        try:
            # Limita testo per evitare errori
            text = text[:500] if len(text) > 500 else text
            
            tts = gTTS(text=text, lang=lang, slow=False)
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, suffix='.mp3', dir=self.output_dir
            )
            tts.save(temp_file.name)
            temp_file.close()
            self.temp_files.append(temp_file.name)
            return temp_file.name
        except Exception as e:
            print(f"⚠️  Errore TTS: {e}")
            return None
    
    def create_news_segment(self, article: Dict, duration: int = 10):
        """Crea un segmento video per una notizia"""
        if not MOVIEPY_AVAILABLE or VideoFileClip is None:
            return None
        
        try:
            clips = []
            
            # 1. Immagine di sfondo (se disponibile)
            image_path = self.download_image(article.get('image_url'))
            if image_path:
                img_clip = ImageClip(image_path, duration=duration)
                # Ridimensiona per adattare al formato YouTube (1920x1080)
                img_clip = img_clip.resize(height=1080)
                # Centra l'immagine
                img_clip = img_clip.set_position(('center', 'center'))
                clips.append(img_clip)
            else:
                # Sfondo nero se non c'è immagine
                img_clip = ImageClip('black.jpg', duration=duration) if os.path.exists('black.jpg') else None
                if not img_clip:
                    # Crea sfondo nero temporaneo
                    from PIL import Image
                    black_img = Image.new('RGB', (1920, 1080), color='black')
                    black_path = os.path.join(self.output_dir, 'black_temp.jpg')
                    black_img.save(black_path)
                    img_clip = ImageClip(black_path, duration=duration)
                    self.temp_files.append(black_path)
                clips.append(img_clip)
            
            # 2. Titolo come testo sovrapposto
            title = article.get('title', 'Notizia')[:100]  # Limita lunghezza
            title_clip = TextClip(
                title,
                fontsize=60,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(1600, None),
                align='center'
            ).set_position(('center', 100)).set_duration(duration)
            clips.append(title_clip)
            
            # 3. Summary come testo
            summary = article.get('summary', article.get('content', ''))[:300]
            if summary:
                summary_clip = TextClip(
                    summary,
                    fontsize=40,
                    color='white',
                    font='Arial',
                    method='caption',
                    size=(1600, 400),
                    align='center'
                ).set_position(('center', 300)).set_duration(duration)
                clips.append(summary_clip)
            
            # 4. Audio narrante (se disponibile)
            audio_text = f"{title}. {summary[:200]}"
            audio_path = self.text_to_speech(audio_text, lang='it')
            if audio_path:
                try:
                    audio_clip = AudioFileClip(audio_path)
                    # Adatta durata video all'audio
                    if audio_clip.duration > duration:
                        duration = min(audio_clip.duration + 2, 30)  # Max 30 secondi
                        for clip in clips:
                            clip.duration = duration
                    clips[0] = clips[0].set_audio(audio_clip)
                except Exception as e:
                    print(f"⚠️  Errore aggiunta audio: {e}")
            
            # Combina tutti i clip
            final_clip = CompositeVideoClip(clips, size=(1920, 1080))
            return final_clip
            
        except Exception as e:
            print(f"⚠️  Errore creazione segmento: {e}")
            return None
    
    def create_video(self, max_articles: int = 5, output_filename: str = None) -> Optional[str]:
        """Crea video completo con più notizie"""
        if not MOVIEPY_AVAILABLE:
            print("❌ moviepy non disponibile. Installa con: pip install moviepy")
            return None
        
        try:
            # Seleziona le notizie migliori (featured o più recenti)
            selected_articles = sorted(
                self.articles[:max_articles],
                key=lambda x: (x.get('is_featured', False), x.get('quality_score', 0)),
                reverse=True
            )[:max_articles]
            
            print(f"📹 Creo video con {len(selected_articles)} notizie...")
            
            segments = []
            for i, article in enumerate(selected_articles):
                print(f"   {i+1}/{len(selected_articles)}: {article.get('title', '')[:50]}...")
                segment = self.create_news_segment(article, duration=12)
                if segment:
                    segments.append(segment)
            
            if not segments:
                print("❌ Nessun segmento creato!")
                return None
            
            # Unisci tutti i segmenti
            print("🔗 Unisco i segmenti...")
            final_video = concatenate_videoclips(segments, method="compose")
            
            # Genera nome file
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"newsflow_{timestamp}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Salva video
            print(f"💾 Salvo video: {output_path}")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=os.path.join(self.output_dir, 'temp_audio.m4a'),
                remove_temp=True
            )
            
            # Chiudi i clip per liberare memoria
            final_video.close()
            for segment in segments:
                segment.close()
            
            print(f"✅ Video creato: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Errore creazione video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def upload_to_youtube(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str] = None,
        category_id: str = "25",  # News & Politics
        privacy_status: str = "public"
    ) -> Optional[str]:
        """Carica video su YouTube"""
        if not YOUTUBE_API_AVAILABLE:
            print("❌ YouTube API non disponibile")
            return None
        
        # Le credenziali devono essere configurate separatamente
        # Vedi: https://developers.google.com/youtube/v3/guides/uploading_a_video
        print("📤 Upload su YouTube richiede configurazione API...")
        print("   Vedi: https://developers.google.com/youtube/v3/guides/uploading_a_video")
        return None
    
    def cleanup(self):
        """Pulisce file temporanei"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass


def create_youtube_video_from_articles(articles: List[Dict], max_articles: int = 5) -> Optional[str]:
    """Funzione helper per creare video da articoli"""
    generator = YouTubeVideoGenerator(articles)
    try:
        video_path = generator.create_video(max_articles=max_articles)
        return video_path
    finally:
        generator.cleanup()


if __name__ == "__main__":
    # Test
    test_articles = [
        {
            "title": "Test Notizia 1",
            "summary": "Questa è una notizia di test per verificare il generatore video.",
            "image_url": "https://via.placeholder.com/1920x1080",
            "is_featured": True,
            "quality_score": 0.9
        }
    ]
    
    generator = YouTubeVideoGenerator(test_articles)
    video_path = generator.create_video(max_articles=1)
    if video_path:
        print(f"✅ Video di test creato: {video_path}")
    generator.cleanup()


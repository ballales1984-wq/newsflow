"""
Versione semplificata del generatore video - solo immagini e audio
Per testare che moviepy funzioni correttamente
"""
import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import tempfile

try:
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  moviepy non installato")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


def create_simple_video(articles: List[Dict], output_path: str = "test_video.mp4", duration_per_article: int = 10):
    """Crea video semplice con solo immagini e audio"""
    if not MOVIEPY_AVAILABLE:
        return None
    
    try:
        os.makedirs("youtube_videos", exist_ok=True)
        clips = []
        
        for i, article in enumerate(articles[:3]):  # Max 3 per test
            print(f"Creo clip {i+1}: {article.get('title', '')[:50]}...")
            
            # Scarica immagine
            image_url = article.get('image_url')
            if image_url:
                try:
                    response = requests.get(image_url, timeout=10)
                    if response.status_code == 200:
                        img_path = f"youtube_videos/temp_img_{i}.jpg"
                        with open(img_path, 'wb') as f:
                            f.write(response.content)
                        
                        # Crea clip immagine
                        img_clip = ImageClip(img_path, duration=duration_per_article)
                        img_clip = img_clip.resize(height=1080)
                        
                        # Aggiungi audio se disponibile
                        title = article.get('title', '')
                        if GTTS_AVAILABLE and title:
                            try:
                                tts = gTTS(text=title[:100], lang='it', slow=False)
                                audio_path = f"youtube_videos/temp_audio_{i}.mp3"
                                tts.save(audio_path)
                                audio = AudioFileClip(audio_path)
                                img_clip = img_clip.set_audio(audio)
                            except:
                                pass
                        
                        clips.append(img_clip)
                except Exception as e:
                    print(f"Errore articolo {i}: {e}")
                    continue
        
        if not clips:
            print("Nessun clip creato!")
            return None
        
        # Unisci clip
        final = concatenate_videoclips(clips)
        final.write_videofile(output_path, fps=24, codec='libx264')
        final.close()
        
        print(f"✅ Video creato: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # Test con articoli dal backend
    try:
        response = requests.get('http://localhost:8000/api/v1/articles')
        if response.status_code == 200:
            data = response.json()
            articles = data.get('items', [])[:2]
            video_path = create_simple_video(articles)
            if video_path:
                print(f"\n✅ Test riuscito! Video: {video_path}")
    except Exception as e:
        print(f"Errore: {e}")


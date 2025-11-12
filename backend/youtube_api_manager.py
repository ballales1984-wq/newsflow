"""
YouTube API Manager - Upload automatico e Live Streaming
Gestisce upload video e creazione live automaticamente
"""
import os
import json
from typing import Optional, Dict
from datetime import datetime

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    print("⚠️  YouTube API non installato. Installa con: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")


class YouTubeAPIManager:
    """Gestisce upload e live streaming automatici su YouTube"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']
    
    def __init__(self, credentials_file: str = "youtube_credentials.json", token_file: str = "youtube_token.json"):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.youtube = None
        self.credentials = None
        
    def authenticate(self) -> bool:
        """Autentica con YouTube API"""
        if not YOUTUBE_API_AVAILABLE:
            print("❌ YouTube API non disponibile")
            return False
        
        # Carica credenziali esistenti
        if os.path.exists(self.token_file):
            try:
                self.credentials = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
            except Exception as e:
                print(f"⚠️  Errore caricamento token: {e}")
        
        # Se non ci sono credenziali valide, richiedi autenticazione
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.credentials.refresh(Request())
                except Exception as e:
                    print(f"⚠️  Errore refresh token: {e}")
                    self.credentials = None
            
            if not self.credentials:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ File credenziali non trovato: {self.credentials_file}")
                    print("   Scarica da: https://console.cloud.google.com/apis/credentials")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            # Salva token per prossime volte
            with open(self.token_file, 'w') as token:
                token.write(self.credentials.to_json())
        
        # Crea servizio YouTube
        try:
            self.youtube = build('youtube', 'v3', credentials=self.credentials)
            return True
        except Exception as e:
            print(f"❌ Errore creazione servizio YouTube: {e}")
            return False
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: list = None,
        category_id: str = "25",  # News & Politics
        privacy_status: str = "public"
    ) -> Optional[str]:
        """
        Carica video su YouTube
        
        Returns:
            Video ID se successo, None altrimenti
        """
        if not self.youtube:
            if not self.authenticate():
                return None
        
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status
                }
            }
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            print(f"📤 Upload video: {title}...")
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"   Progresso: {progress}%")
            
            video_id = response['id']
            print(f"✅ Video caricato! ID: {video_id}")
            print(f"   URL: https://www.youtube.com/watch?v={video_id}")
            return video_id
            
        except Exception as e:
            print(f"❌ Errore upload video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_live_broadcast(
        self,
        title: str,
        description: str = "",
        scheduled_start_time: datetime = None,
        privacy_status: str = "public"
    ) -> Optional[Dict]:
        """
        Crea una live broadcast programmata
        
        Returns:
            Dict con broadcast_id e stream_id
        """
        if not self.youtube:
            if not self.authenticate():
                return None
        
        try:
            # Crea broadcast
            broadcast_body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'scheduledStartTime': scheduled_start_time.isoformat() if scheduled_start_time else None
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                },
                'contentDetails': {
                    'enableDvr': True,
                    'enableEmbed': True,
                    'recordFromStart': True,
                    'enableLowLatency': False
                }
            }
            
            print(f"📺 Creo live broadcast: {title}...")
            broadcast_response = self.youtube.liveBroadcasts().insert(
                part='snippet,status,contentDetails',
                body=broadcast_body
            ).execute()
            
            broadcast_id = broadcast_response['id']
            print(f"✅ Broadcast creato! ID: {broadcast_id}")
            
            # Crea stream (serve per trasmettere)
            # Per ora restituiamo solo broadcast_id
            # Lo stream va configurato separatamente con stream key
            
            return {
                'broadcast_id': broadcast_id,
                'title': title,
                'scheduled_start_time': scheduled_start_time.isoformat() if scheduled_start_time else None
            }
            
        except Exception as e:
            print(f"❌ Errore creazione broadcast: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def start_broadcast(self, broadcast_id: str) -> bool:
        """Avvia una broadcast"""
        if not self.youtube:
            if not self.authenticate():
                return False
        
        try:
            self.youtube.liveBroadcasts().transition(
                broadcastStatus='live',
                id=broadcast_id,
                part='status'
            ).execute()
            print(f"✅ Broadcast {broadcast_id} avviata!")
            return True
        except Exception as e:
            print(f"❌ Errore avvio broadcast: {e}")
            return False
    
    def stop_broadcast(self, broadcast_id: str) -> bool:
        """Ferma una broadcast"""
        if not self.youtube:
            if not self.authenticate():
                return False
        
        try:
            self.youtube.liveBroadcasts().transition(
                broadcastStatus='complete',
                id=broadcast_id,
                part='status'
            ).execute()
            print(f"✅ Broadcast {broadcast_id} fermata!")
            return True
        except Exception as e:
            print(f"❌ Errore stop broadcast: {e}")
            return False


if __name__ == "__main__":
    # Test
    manager = YouTubeAPIManager()
    if manager.authenticate():
        print("✅ Autenticazione riuscita!")
    else:
        print("❌ Autenticazione fallita!")


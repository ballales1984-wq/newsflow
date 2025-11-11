# 🎬 Sistema Generazione Video YouTube - NewsFlow

## 📋 Panoramica

Sistema automatico per creare video YouTube dalle notizie di NewsFlow:
- ✅ Crea video con immagini e testo
- ✅ Aggiunge voce narrante (Text-to-Speech)
- ✅ Formato YouTube (1920x1080)
- ✅ Pronto per upload su YouTube

## 🚀 Installazione

### 1. Installa Dipendenze Python

```bash
cd backend
pip install moviepy gtts pillow google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Oppure usa requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Verifica Installazione

```bash
python -c "import moviepy; import gtts; print('✅ Tutto installato!')"
```

## 📹 Come Usare

### Metodo 1: Script PowerShell (Consigliato)

1. **Doppio clic su:** `CREA_VIDEO_YOUTUBE.ps1`
2. Il video verrà creato in: `backend/youtube_videos/`
3. Carica manualmente su YouTube

### Metodo 2: API Endpoint

```bash
# Crea video con 5 notizie (default)
curl -X POST http://localhost:8000/api/admin/create-youtube-video

# Crea video con 10 notizie
curl -X POST "http://localhost:8000/api/admin/create-youtube-video?max_articles=10"
```

### Metodo 3: Python Diretto

```python
from youtube_video_generator import create_youtube_video_from_articles

articles = [...]  # Le tue notizie
video_path = create_youtube_video_from_articles(articles, max_articles=5)
print(f"Video creato: {video_path}")
```

## 🎥 Caratteristiche Video

- **Formato:** 1920x1080 (Full HD)
- **FPS:** 24
- **Codec:** H.264 (mp4)
- **Audio:** AAC
- **Durata:** ~12 secondi per notizia
- **Contenuto:**
  - Immagine di sfondo (se disponibile)
  - Titolo in grande
  - Summary/testo della notizia
  - Voce narrante (TTS italiano)

## 📤 Upload su YouTube (Opzionale)

### Setup YouTube API

1. Vai su: https://console.cloud.google.com/
2. Crea un progetto
3. Abilita YouTube Data API v3
4. Crea credenziali OAuth 2.0
5. Scarica `client_secrets.json`
6. Posiziona il file in `backend/`

### Configurazione

Modifica `youtube_video_generator.py` e aggiungi:

```python
YOUTUBE_CLIENT_SECRETS_FILE = "backend/client_secrets.json"
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
```

### Upload Automatico

Il metodo `upload_to_youtube()` è già implementato ma richiede configurazione API.

## 🛠️ Troubleshooting

### Errore: "moviepy non installato"
```bash
pip install moviepy
```

### Errore: "gtts non installato"
```bash
pip install gtts
```

### Errore: "Pillow non installato"
```bash
pip install Pillow
```

### Video troppo grande
- Riduci `max_articles` (es. 3 invece di 5)
- Comprimi il video dopo la creazione

### Audio non funziona
- Verifica connessione internet (gTTS richiede internet)
- Controlla che il testo non sia vuoto

## 📝 Note

- Il primo video richiede più tempo (download dipendenze)
- Le immagini vengono scaricate automaticamente
- I file temporanei vengono puliti automaticamente
- Il video viene salvato in `backend/youtube_videos/`

## 🎯 Prossimi Miglioramenti

- [ ] Upload automatico su YouTube
- [ ] Template video personalizzabili
- [ ] Musica di sottofondo
- [ ] Transizioni tra notizie
- [ ] Logo NewsFlow nel video
- [ ] Sottotitoli automatici


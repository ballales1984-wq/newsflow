# 🔄 Setup Aggiornamento Automatico Articoli

## 📋 Sistema di Aggiornamento

Il sistema è configurato per aggiornare automaticamente gli articoli:

- ⏰ **Raccolta articoli**: ogni 4 ore (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
- 📊 **Aggiornamento punteggi**: ogni 8 ore
- 🗑️ **Pulizia vecchi articoli**: ogni giorno alle 3:00 AM

## 🚀 Requisiti

### Opzione A: Deploy su Render/Railway (CONSIGLIATO)

Render e Railway offrono Redis gratuito:

1. **Render**:
   - Redis gratuito incluso
   - Worker Celery automatico
   - Setup con `render.yaml`

2. **Railway**:
   - Redis plugin gratuito
   - Auto-deploy da GitHub

### Opzione B: Locale con Docker

```bash
# 1. Avvia Redis con Docker
docker run -d -p 6379:6379 redis:alpine

# 2. Installa dipendenze
cd backend
pip install celery redis

# 3. Avvia Celery Worker
celery -A app.core.celery_app worker --loglevel=info

# 4. Avvia Celery Beat (scheduler)
celery -A app.core.celery_app beat --loglevel=info
```

### Opzione C: Redis locale (Windows)

```bash
# Installa Redis tramite Memurai (Redis per Windows)
choco install memurai

# Oppure usa WSL2 con Redis
wsl --install
wsl
sudo apt update && sudo apt install redis-server
sudo service redis-server start
```

## ⚙️ Configurazione

### 1. Variabili d'ambiente

Aggiungi al `.env`:

```env
# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 2. Per Deploy su Render

Il file `render.yaml` già include:

```yaml
services:
  # Backend API
  - type: web
    name: newsflow-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    
  # Celery Worker (per task in background)
  - type: worker
    name: newsflow-worker
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "celery -A app.core.celery_app worker --loglevel=info"
    
  # Celery Beat (scheduler)
  - type: worker
    name: newsflow-beat
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "celery -A app.core.celery_app beat --loglevel=info"

  # Redis
  - type: redis
    name: newsflow-redis
    plan: free
```

## 📊 Monitoraggio

### Verificare che funzioni

```bash
# Controlla i worker attivi
celery -A app.core.celery_app inspect active

# Vedi le task schedulate
celery -A app.core.celery_app inspect scheduled

# Statistiche
celery -A app.core.celery_app inspect stats
```

### Log delle task

Le task scrivono log in:
- Console del worker
- File `logs/celery.log` (se configurato)

## 🔧 Test Manuale

Per testare la raccolta immediatamente:

```bash
# Raccolta veloce (5 fonti)
python backend/collect_news_now.py

# Raccolta completa (tutte le fonti)
python backend/collect_all_sources.py
```

## 📦 Deploy su Vercel (Solo Frontend)

Vercel supporta solo frontend. Per il backend usa Render/Railway:

1. **Frontend su Vercel** → newsflow-three.vercel.app
2. **Backend + Celery su Render** → newsflow-api.onrender.com
3. **Redis su Render** → Incluso gratuitamente

## 🎯 Prossimi Passi

1. ✅ Configurazione Celery completata (ogni 4 ore)
2. ⏳ Deploy backend su Render con Redis
3. ⏳ Attivazione Celery Worker e Beat
4. ⏳ Aggiunta fonti RSS per nuove categorie (Sport, Nature, Business, ecc.)

## 🆘 Troubleshooting

**Worker non parte:**
```bash
# Verifica che Redis sia raggiungibile
redis-cli ping
# Dovrebbe rispondere: PONG
```

**Task non si eseguono:**
```bash
# Verifica che Beat sia attivo
ps aux | grep celery

# Restart dei servizi
pkill -f celery
celery -A app.core.celery_app worker &
celery -A app.core.celery_app beat &
```

**Errori di connessione a Redis:**
- Controlla che `REDIS_URL` sia corretto
- Verifica firewall/porte
- Su Render, usa l'URL interno del servizio Redis

---

**Note**: Il sistema attuale usa `main_simple.py` con JSON statici. Per attivare l'aggiornamento automatico, passa a `main.py` con database + Celery.


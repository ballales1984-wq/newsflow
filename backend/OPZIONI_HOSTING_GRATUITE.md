# 🚀 Piattaforme Gratuite per Backend FastAPI

## 1. **Render** ⭐ (CONSIGLIATO - già usato nel progetto)
- **URL già configurato**: `https://newsflow-backend-v2.onrender.com`
- **Piano gratuito**: 
  - 750 ore/mese (circa 24/7 per 1 mese)
  - Sleep mode dopo 15 minuti di inattività
  - Wake-up automatico (30-60 secondi)
- **Vantaggi**:
  - ✅ Facile da configurare
  - ✅ Deploy automatico da GitHub
  - ✅ Supporta Python/FastAPI nativamente
  - ✅ HTTPS incluso
  - ✅ Già configurato nel progetto
- **Svantaggi**:
  - ⚠️ Sleep mode (ma c'è già un keep-alive configurato)
  - ⚠️ Limite 750 ore/mese

**Setup**: Collega GitHub → Render → Deploy automatico

---

## 2. **Railway** 🚂
- **Piano gratuito**: 
  - $5 di credito/mese
  - Nessun sleep mode
  - Deploy continuo
- **Vantaggi**:
  - ✅ Nessun sleep mode
  - ✅ Deploy molto veloce
  - ✅ Supporta Python/FastAPI
  - ✅ Database incluso (PostgreSQL gratuito)
- **Svantaggi**:
  - ⚠️ Limite di credito (ma $5/mese è generoso)
  - ⚠️ Potrebbe costare se traffico alto

**Setup**: `railway up` o GitHub integration

---

## 3. **Fly.io** ✈️
- **Piano gratuito**: 
  - 3 VM condivise gratuite
  - 160GB di traffico/mese
  - Nessun sleep mode
- **Vantaggi**:
  - ✅ Molto generoso
  - ✅ Deploy globale (edge computing)
  - ✅ Nessun sleep mode
  - ✅ Supporta Python/FastAPI
- **Svantaggi**:
  - ⚠️ Setup leggermente più complesso
  - ⚠️ Richiede Dockerfile

**Setup**: `flyctl launch` con Dockerfile

---

## 4. **PythonAnywhere** 🐍
- **Piano gratuito**: 
  - 1 web app Python
  - 512MB storage
  - Limitato a domini *.pythonanywhere.com
- **Vantaggi**:
  - ✅ Specifico per Python
  - ✅ Facile da usare
  - ✅ Console Python integrata
- **Svantaggi**:
  - ⚠️ Limitato (solo 1 app)
  - ⚠️ Domini limitati
  - ⚠️ Non ideale per produzione

---

## 5. **Replit** 🔄
- **Piano gratuito**: 
  - Hosting illimitato
  - Sleep mode dopo inattività
- **Vantaggi**:
  - ✅ Facile da usare
  - ✅ Editor integrato
  - ✅ Deploy con un click
- **Svantaggi**:
  - ⚠️ Sleep mode
  - ⚠️ Performance limitate

---

## 🎯 RACCOMANDAZIONE

### **Opzione 1: Render** (già configurato)
- ✅ Il progetto ha già un URL Render configurato
- ✅ C'è già un keep-alive configurato (workflows/keep-alive.yml)
- ✅ Facile da attivare

### **Opzione 2: Railway** (migliore per sempre-online)
- ✅ Nessun sleep mode
- ✅ $5/mese di credito gratuito
- ✅ Più affidabile per produzione

### **Opzione 3: Fly.io** (più generoso)
- ✅ Molto generoso con risorse
- ✅ Nessun sleep mode
- ✅ Deploy globale

---

## 📋 QUICK START - Render (già configurato)

1. Vai su https://render.com
2. Connetti account GitHub
3. Crea nuovo "Web Service"
4. Seleziona repository `newsflow`
5. Configurazione:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT`
   - **Environment**: `PYTHON_VERSION=3.12`
6. Deploy!

Il keep-alive è già configurato in `.github/workflows/keep-alive.yml`

---

## 📋 QUICK START - Railway

1. Vai su https://railway.app
2. Connetti GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Seleziona repository
5. Railway rileva automaticamente Python
6. Configura variabili d'ambiente se necessario
7. Deploy automatico!

---

## 📋 QUICK START - Fly.io

1. Installa `flyctl`: https://fly.io/docs/getting-started/installing-flyctl/
2. `flyctl auth login`
3. `flyctl launch` (nella directory backend)
4. Crea `Dockerfile` se non esiste
5. Deploy automatico!

---

## ⚖️ CONFRONTO RAPIDO

| Piattaforma | Sleep Mode | Limite Gratuito | Facilità | Raccomandato |
|------------|------------|-----------------|----------|--------------|
| **Render** | ⚠️ Sì (15min) | 750h/mese | ⭐⭐⭐⭐⭐ | ✅ Già configurato |
| **Railway** | ✅ No | $5/mese | ⭐⭐⭐⭐ | ✅ Migliore |
| **Fly.io** | ✅ No | 3 VM + 160GB | ⭐⭐⭐ | ✅ Generoso |
| **PythonAnywhere** | ⚠️ Sì | 1 app | ⭐⭐⭐⭐ | ⚠️ Limitato |
| **Replit** | ⚠️ Sì | Illimitato | ⭐⭐⭐⭐⭐ | ⚠️ Performance |

---

## 🎯 DECISIONE FINALE

**Per questo progetto, consiglio Railway o Render:**

1. **Render** - Se vuoi qualcosa di già configurato e funzionante
2. **Railway** - Se vuoi sempre-online senza sleep mode

Entrambi sono gratuiti e perfetti per un backend FastAPI!


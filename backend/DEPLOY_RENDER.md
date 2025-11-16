# 🚀 Deploy Backend su Render (GRATUITO)

## ✅ Vantaggi Render
- **Gratuito**: 750 ore/mese (circa 24/7 per 1 mese)
- **Già configurato**: URL `https://newsflow-backend-v2.onrender.com` già presente
- **Keep-alive**: GitHub Actions già configurato per mantenere sveglio
- **HTTPS incluso**: Certificato SSL automatico
- **Deploy automatico**: Da GitHub

## 📋 Setup Render (5 minuti)

### 1. Crea account Render
- Vai su https://render.com
- Registrati con GitHub (consigliato)

### 2. Crea nuovo Web Service
1. Dashboard → **New** → **Web Service**
2. Connetti repository GitHub `newsflow`
3. Seleziona branch `main`

### 3. Configurazione
```
Name: newsflow-backend-v2
Region: Frankfurt (o più vicino a te)
Branch: main
Root Directory: backend
```

### 4. Build & Start Commands
```
Build Command:
cd backend && pip install -r requirements.txt

Start Command:
python -m uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT
```

### 5. Environment Variables
```
PYTHON_VERSION=3.12
CORS_ORIGINS=https://newsflow-orcin.vercel.app,http://localhost:4200
```

### 6. Deploy!
- Clicca **Create Web Service**
- Attendi 5-10 minuti per il primo deploy
- URL sarà: `https://newsflow-backend-v2.onrender.com`

## 🔄 Keep-Alive (già configurato)
Il file `.github/workflows/keep-alive.yml` pinga il backend ogni 15 minuti per evitare sleep mode.

## 📝 Aggiorna Frontend
Dopo il deploy, aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://newsflow-backend-v2.onrender.com/api/v1'
```

## ⚠️ Note Importanti
- **Sleep mode**: Dopo 15 minuti di inattività, Render mette in sleep
- **Wake-up**: 30-60 secondi al primo accesso dopo sleep
- **Limite**: 750 ore/mese (circa 24/7 per 1 mese)
- **Keep-alive**: GitHub Actions mantiene sveglio automaticamente

## 🎯 Risultato
✅ Backend sempre online (grazie al keep-alive)
✅ Gratuito
✅ HTTPS incluso
✅ Deploy automatico da GitHub
✅ Puoi spegnere il PC!


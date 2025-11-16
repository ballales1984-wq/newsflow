# 🚂 Deploy Backend su Railway (GRATUITO - $5/mese credito)

## ✅ Vantaggi Railway
- **Gratuito**: $5 di credito/mese (molto generoso)
- **Nessun sleep mode**: Backend sempre online
- **Deploy automatico**: Da GitHub
- **HTTPS incluso**: Certificato SSL automatico
- **Database incluso**: PostgreSQL gratuito (opzionale)
- **Più affidabile**: Ideale per produzione

## 📋 Setup Railway (5 minuti)

### 1. Crea account Railway
- Vai su https://railway.app
- Clicca **Start a New Project**
- Connetti con **GitHub** (consigliato)

### 2. Deploy da GitHub
1. Dashboard → **New Project**
2. Seleziona **Deploy from GitHub repo**
3. Autorizza Railway ad accedere a GitHub
4. Seleziona repository `newsflow`
5. Railway rileva automaticamente Python! 🎉

### 3. Configurazione Automatica
Railway rileva automaticamente:
- ✅ Python runtime
- ✅ Requirements.txt
- ✅ Porta (usa variabile `PORT`)

### 4. Configurazione Manuale (se necessario)
Se Railway non rileva automaticamente:

**Settings → Deploy:**
```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main_simple:app --host 0.0.0.0 --port $PORT
```

### 5. Environment Variables
**Settings → Variables:**
```
CORS_ORIGINS=https://newsflow-orcin.vercel.app,http://localhost:4200
PYTHON_VERSION=3.12
```

### 6. Genera Domain
1. **Settings** → **Networking**
2. Clicca **Generate Domain**
3. Ottieni URL tipo: `newsflow-backend-production.up.railway.app`
4. Copia l'URL!

### 7. Deploy!
- Railway fa deploy automatico ad ogni push su GitHub
- Attendi 2-3 minuti per il primo deploy
- Controlla i log in tempo reale

## 📝 Aggiorna Frontend
Dopo il deploy, aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://TUO-PROGETTO.up.railway.app/api/v1'
```

## 🔄 Deploy Automatico
Railway fa deploy automatico ad ogni push su `main` branch!

## 💰 Costi
- **Gratuito**: $5 di credito/mese
- **Uso tipico**: Backend FastAPI usa ~$2-3/mese
- **Monitoraggio**: Dashboard mostra uso in tempo reale
- **Avvisi**: Email quando credito < $1

## ⚠️ Note Importanti
- **Nessun sleep mode**: Backend sempre online! ✅
- **Credito**: Monitora uso nel dashboard
- **HTTPS**: Incluso automaticamente
- **Logs**: Disponibili in tempo reale nel dashboard

## 🎯 Risultato
✅ Backend sempre online (nessun sleep mode!)
✅ Gratuito ($5/mese credito)
✅ HTTPS incluso
✅ Deploy automatico da GitHub
✅ Puoi spegnere il PC!
✅ Più affidabile di Render

## 🆚 Confronto con Render
| Feature | Render | Railway |
|---------|--------|---------|
| Sleep Mode | ⚠️ Sì (15min) | ✅ No |
| Credito Gratuito | 750h/mese | $5/mese |
| Affidabilità | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Setup | Facile | Facilissimo |
| Database | ❌ | ✅ PostgreSQL gratuito |

## 🚀 Quick Start (1 comando)
```bash
# Installa Railway CLI (opzionale)
npm i -g @railway/cli

# Login
railway login

# Deploy (nella directory backend)
cd backend
railway up
```

Ma il modo più facile è usare il dashboard web! 🎉


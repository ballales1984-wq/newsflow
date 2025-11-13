# 🤖 Integrazione AI per Approfondimenti

## ✅ Cosa è stato implementato

### 1. Servizio AI (`backend/app/ai_explainer.py`)
- **ChatGPT (OpenAI)**: Supporto completo per spiegazioni AI
- **DeepSeek**: Alternativa economica con buona qualità
- **Fallback automatico**: Se le API non sono disponibili, usa spiegazioni statiche migliorate

### 2. Endpoint API (`/api/v1/articles/explain`)
- **POST** `/api/v1/articles/explain`
- Genera spiegazioni AI per articoli
- Supporta 3 tipi: `quick`, `standard`, `deep`

### 3. Frontend aggiornato
- Chiamate API per spiegazioni AI
- Indicatori di caricamento
- Badge "Powered by AI"
- Cache delle spiegazioni (non ricarica se già generate)

---

## 🔧 Configurazione API Keys

### Opzione 1: Variabili d'ambiente (consigliato)

Nel file `backend/AVVIA_TUTTO_AUTO.bat` o script di avvio, aggiungi:

```batch
set OPENAI_API_KEY=sk-tua-chiave-openai
set DEEPSEEK_API_KEY=sk-tua-chiave-deepseek
```

### Opzione 2: File `.env` (se supportato)

Crea `backend/.env`:
```
OPENAI_API_KEY=sk-tua-chiave-openai
DEEPSEEK_API_KEY=sk-tua-chiave-deepseek
```

### Opzione 3: PowerShell (temporaneo)

```powershell
$env:OPENAI_API_KEY = "sk-tua-chiave-openai"
$env:DEEPSEEK_API_KEY = "sk-tua-chiave-deepseek"
```

---

## 📝 Come ottenere le API Keys

### OpenAI (ChatGPT)
1. Vai su: https://platform.openai.com/api-keys
2. Crea un account o accedi
3. Clicca "Create new secret key"
4. Copia la chiave (inizia con `sk-`)

**Costi**: ~$0.15 per 1M token (modello `gpt-4o-mini`)

### DeepSeek
1. Vai su: https://platform.deepseek.com/api_keys
2. Crea un account o accedi
3. Clicca "Create API Key"
4. Copia la chiave (inizia con `sk-`)

**Costi**: ~$0.14 per 1M token (modello `deepseek-chat`)

---

## 🎯 Come funziona

1. **Utente clicca "Spiegami questa notizia"**
2. **Frontend chiama API** `/api/v1/articles/explain`
3. **Backend prova ChatGPT** (se API key disponibile)
4. **Se fallisce, prova DeepSeek** (se API key disponibile)
5. **Se entrambi falliscono, usa spiegazione statica migliorata**

### Tipi di spiegazione:
- **Quick (30s)**: Breve, max 150 parole
- **Standard (3min)**: Dettagliata, max 400 parole
- **Deep (approfondito)**: Analisi completa, max 800 parole

---

## 💡 Vantaggi

✅ **Spiegazioni uniche**: Ogni articolo ha spiegazioni diverse generate dall'AI
✅ **Più approfondite**: Le spiegazioni AI sono più dettagliate e contestualizzate
✅ **Fallback sicuro**: Se le API non sono disponibili, funziona comunque
✅ **Cache intelligente**: Le spiegazioni vengono cachate per evitare chiamate duplicate

---

## 🚀 Test

1. Avvia il backend
2. Apri il sito
3. Clicca "Spiegami questa notizia" su un articolo
4. Vedi l'indicatore di caricamento
5. La spiegazione AI appare con badge "Powered by ChatGPT" o "Powered by DeepSeek"

---

## ⚠️ Note importanti

- **Costi**: Ogni spiegazione costa pochi centesimi. Monitora l'uso!
- **Rate limits**: Le API hanno limiti di chiamate al minuto
- **Privacy**: Le API keys devono essere mantenute segrete
- **Fallback**: Se non configuri le API keys, funziona comunque con spiegazioni statiche

---

## 🔒 Sicurezza

**NON COMMITTARE LE API KEYS NEL CODICE!**

Usa sempre variabili d'ambiente o file `.env` (non tracciato da git).


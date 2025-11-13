# 🆓 Setup AI Gratuite per Approfondimenti

## ✅ Servizi AI Gratuiti Supportati

### 1. 🏠 Ollama (LOCALE - COMPLETAMENTE GRATUITO) ⭐ CONSIGLIATO

**Vantaggi:**
- ✅ Completamente gratuito
- ✅ Funziona offline
- ✅ Nessun limite di chiamate
- ✅ Privacy totale (dati non lasciano il tuo PC)
- ✅ Velocità elevata (locale)

**Setup:**

1. **Scarica Ollama:**
   ```
   https://ollama.ai/download
   ```

2. **Installa un modello (scegli uno):**
   ```bash
   ollama pull llama3.2
   # oppure
   ollama pull mistral
   # oppure
   ollama pull phi3
   ```

3. **Avvia Ollama:**
   - Windows: Si avvia automaticamente dopo l'installazione
   - Verifica: http://localhost:11434

4. **Configura backend (opzionale):**
   ```powershell
   $env:OLLAMA_URL = "http://localhost:11434"
   ```

**✅ Pronto!** Il backend userà automaticamente Ollama se disponibile.

---

### 2. 🤗 Hugging Face Inference API (GRATUITA)

**Vantaggi:**
- ✅ API gratuita (con account)
- ✅ Buona qualità
- ✅ Nessuna installazione locale

**Setup:**

1. **Crea account gratuito:**
   ```
   https://huggingface.co/join
   ```

2. **Ottieni API Token:**
   - Vai su: https://huggingface.co/settings/tokens
   - Clicca "New token"
   - Copia il token (inizia con `hf_`)

3. **Configura backend:**
   ```powershell
   $env:HUGGINGFACE_API_KEY = "hf_tuo-token"
   ```

**✅ Pronto!** Il backend userà Hugging Face se Ollama non è disponibile.

---

### 3. 🚀 DeepSeek (TIER GRATUITO)

**Vantaggi:**
- ✅ Tier gratuito disponibile
- ✅ Alta qualità
- ✅ Buone performance

**Setup:**

1. **Crea account:**
   ```
   https://platform.deepseek.com/signup
   ```

2. **Ottieni API Key:**
   - Vai su: https://platform.deepseek.com/api_keys
   - Clicca "Create API Key"
   - Copia la chiave (inizia con `sk-`)

3. **Configura backend:**
   ```powershell
   $env:DEEPSEEK_API_KEY = "sk-tua-chiave"
   ```

**✅ Pronto!** Il backend userà DeepSeek se Ollama e Hugging Face non sono disponibili.

---

### 4. 💬 ChatGPT (OPZIONALE - NON GRATUITO)

**Nota:** ChatGPT richiede API key a pagamento. Usalo solo se hai già un account OpenAI.

**Setup:**

1. **Ottieni API Key:**
   ```
   https://platform.openai.com/api-keys
   ```

2. **Configura backend:**
   ```powershell
   $env:OPENAI_API_KEY = "sk-tua-chiave"
   ```

---

## 🎯 Ordine di Priorità

Il sistema prova i servizi in questo ordine:

1. **Ollama** (locale, gratuito) ⭐ PRIMA SCELTA
2. **Hugging Face** (API gratuita) ⭐ SECONDA SCELTA
3. **DeepSeek** (tier gratuito) ⭐ TERZA SCELTA
4. **ChatGPT** (solo se API key disponibile)
5. **Spiegazione statica** (fallback se nessun AI disponibile)

---

## 🚀 Setup Rapido (Consigliato)

### Opzione 1: Solo Ollama (Più Semplice)

```powershell
# 1. Installa Ollama da https://ollama.ai/download
# 2. Installa modello:
ollama pull llama3.2

# 3. Avvia backend normalmente
# Ollama verrà rilevato automaticamente!
```

### Opzione 2: Ollama + Hugging Face (Backup)

```powershell
# 1. Setup Ollama (vedi sopra)
# 2. Ottieni token Hugging Face (gratuito)
# 3. Configura:
$env:HUGGINGFACE_API_KEY = "hf_tuo-token"

# 4. Avvia backend
# Se Ollama non è disponibile, userà Hugging Face
```

---

## 📝 Configurazione Permanente

Per rendere la configurazione permanente, aggiungi nel file `backend/AVVIA_TUTTO_AUTO.bat`:

```batch
REM Configurazione AI Gratuite
set HUGGINGFACE_API_KEY=hf_tuo-token
set DEEPSEEK_API_KEY=sk-tua-chiave
set OLLAMA_URL=http://localhost:11434
```

---

## ✅ Verifica Setup

Dopo aver configurato, verifica quale servizio viene usato:

1. Apri il sito
2. Clicca "Spiegami questa notizia" su un articolo
3. Guarda il badge in basso: dovrebbe dire "Powered by Ollama (Gratuito)" o altro

---

## 💡 Consigli

- **Per uso locale**: Usa **Ollama** (completamente gratuito, nessun limite)
- **Per backup online**: Aggiungi **Hugging Face** (gratuito con account)
- **Per massima qualità**: Aggiungi **DeepSeek** (tier gratuito)

---

## 🆘 Troubleshooting

### Ollama non funziona?
- Verifica che Ollama sia avviato: http://localhost:11434
- Verifica che almeno un modello sia installato: `ollama list`
- Installa un modello: `ollama pull llama3.2`

### Hugging Face non funziona?
- Verifica che il token sia corretto
- Alcuni modelli potrebbero essere in caricamento (prova più volte)

### Nessun servizio funziona?
- Il sistema userà automaticamente spiegazioni statiche migliorate
- Funziona comunque, ma senza AI

---

## 🎉 Fatto!

Ora hai un sistema AI completamente gratuito per generare spiegazioni approfondite!


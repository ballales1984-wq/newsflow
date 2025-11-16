# 🤖 Setup Automatico PythonAnywhere via API

## ✅ Vantaggi
- **Completamente automatico**: Un solo script!
- **Nessuna interazione web**: Tutto da terminale
- **Ripetibile**: Puoi rifare il deploy quando vuoi

## 🚀 Setup (2 minuti)

### STEP 1: Ottieni API Token
1. Vai su https://www.pythonanywhere.com/account/#api_token
2. Clicca **Create a new API token**
3. **Copia il token** (lo vedrai solo una volta!)

### STEP 2: Configura Script
Apri `backend/setup_pythonanywhere_api.py` e modifica:
```python
TOKEN = 'IL_TUO_TOKEN_QUI'  # Incolla il token qui
```

### STEP 3: Installa Dipendenze
```bash
pip install requests
```

### STEP 4: Esegui Script
```bash
cd backend
python setup_pythonanywhere_api.py
```

Lo script:
1. ✅ Verifica token
2. ✅ Ti chiede di clonare repo (una volta)
3. ✅ Crea file WSGI
4. ✅ Crea webapp
5. ✅ Configura webapp
6. ✅ Reload automatico

## 📋 Cosa Fa lo Script

1. **Verifica Token**: Controlla che l'API token funzioni
2. **Clona Repository**: Ti guida a clonare (una volta)
3. **Crea WSGI**: Crea automaticamente `wsgi.py`
4. **Crea Webapp**: Crea webapp se non esiste
5. **Configura**: Imposta source directory e Python version
6. **Reload**: Ricarica webapp automaticamente

## 🔄 Deploy Futuri

Dopo il primo setup, per aggiornare:
```bash
# Pull nuovo codice
cd ~/newsflow && git pull

# Reload webapp
python setup_pythonanywhere_api.py
# (lo script rileva webapp esistente e fa solo reload)
```

Oppure usa direttamente l'API:
```python
import requests
response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/braccobaldo/webapps/braccobaldo.pythonanywhere.com/reload/',
    headers={'Authorization': 'Token TUO_TOKEN'}
)
```

## 🎯 Risultato
✅ Backend deployato automaticamente!
✅ Nessuna interazione web necessaria!
✅ Script riutilizzabile!

## 📝 Nota
Lo script richiede che tu cloni il repository una volta manualmente nella console Bash di PythonAnywhere. Dopo quello, tutto è automatico!


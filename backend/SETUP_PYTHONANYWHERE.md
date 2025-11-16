# 🐍 Setup PythonAnywhere - Istruzioni Step-by-Step

## 📋 Checklist Pre-Deploy

### File Pronti:
- ✅ `backend/wsgi.py` - File WSGI per PythonAnywhere
- ✅ `backend/requirements.txt` - Dipendenze Python
- ✅ `backend/app/main_simple.py` - App FastAPI
- ✅ `backend/final_news_italian.json` - File JSON notizie

## 🚀 Setup PythonAnywhere (15 minuti)

### STEP 1: Crea Account
1. Vai su https://www.pythonanywhere.com
2. Clicca **Beginner account** (gratuito)
3. Registrati con email
4. Verifica email

### STEP 2: Apri Console Bash
1. Dashboard → **Consoles** tab
2. Clicca **Bash** (nuova console)
3. Attendi che si apra

### STEP 3: Clona Repository
Nella console Bash:
```bash
cd ~
git clone https://github.com/ballales1984-wq/newsflow.git
cd newsflow/backend
ls -la
```

### STEP 4: Installa Dipendenze
```bash
# Verifica versione Python
python3.10 --version

# Installa dipendenze
pip3.10 install --user fastapi uvicorn mangum pydantic python-multipart python-slugify

# Se requirements.txt esiste:
pip3.10 install --user -r requirements.txt
```

### STEP 5: Crea Web App
1. Dashboard → **Web** tab
2. Clicca **Add a new web app**
3. Scegli **Flask** (useremo FastAPI comunque)
4. Python version: **Python 3.10**
5. Path: `/home/TUO_USERNAME/newsflow` (sostituisci TUO_USERNAME)

### STEP 6: Configura WSGI
1. Dashboard → **Web** tab
2. Clicca su **WSGI configuration file**
3. **Sostituisci tutto** con questo codice:

```python
import sys
import os

# Aggiungi path backend
path = '/home/TUO_USERNAME/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Imposta working directory
os.chdir(path)

# Importa app FastAPI
from app.main_simple import app

# Wrapper WSGI per FastAPI
application = app
```

**IMPORTANTE**: Sostituisci `TUO_USERNAME` con il tuo username PythonAnywhere!

### STEP 7: Configura Static Files (opzionale)
Dashboard → **Web** → **Static files**:
- URL: `/static`
- Directory: `/home/TUO_USERNAME/newsflow/backend/static` (se esiste)

### STEP 8: Reload Web App
1. Dashboard → **Web** tab
2. Clicca **Reload** (pulsante verde)
3. Attendi 10-20 secondi

### STEP 9: Verifica
1. Dashboard → **Web** tab
2. Clicca sul tuo URL: `https://TUO_USERNAME.pythonanywhere.com`
3. Dovresti vedere la risposta dell'API

### STEP 10: Test API
Apri nel browser:
```
https://TUO_USERNAME.pythonanywhere.com/api/v1/articles?limit=1
```

Dovresti vedere JSON con gli articoli!

## 🔧 Troubleshooting

### Errore: "No module named 'app'"
- Verifica che il path in WSGI sia corretto
- Controlla che `app/main_simple.py` esista

### Errore: "Import error"
- Installa tutte le dipendenze: `pip3.10 install --user -r requirements.txt`
- Verifica che PythonAnywhere abbia Python 3.10

### Errore 500
- Controlla **Error log** in Dashboard → **Web** tab
- Verifica che i file JSON siano nella directory corretta

### File JSON non trovato
- Assicurati che `final_news_italian.json` sia in `backend/`
- Verifica path nel codice: `app/main_simple.py`

## 📝 Aggiorna Frontend
Dopo deploy riuscito, aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://TUO_USERNAME.pythonanywhere.com/api/v1'
```

## 🔄 Aggiornamenti Futuri
Per aggiornare il codice:
```bash
# Nella console Bash
cd ~/newsflow
git pull
# Poi reload web app dal dashboard
```

## ✅ Checklist Finale
- [ ] Account PythonAnywhere creato
- [ ] Repository clonato
- [ ] Dipendenze installate
- [ ] Web app creata
- [ ] WSGI configurato
- [ ] Web app ricaricata
- [ ] API testata
- [ ] Frontend aggiornato con nuovo URL

## 🎉 Risultato
✅ Backend sempre online su PythonAnywhere!
✅ Gratuito per sempre!
✅ Nessuna carta di credito!
✅ Puoi spegnere il PC!


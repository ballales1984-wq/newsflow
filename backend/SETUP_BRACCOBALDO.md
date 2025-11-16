# 🐍 Setup PythonAnywhere per braccobaldo

## ✅ Account Trovato
Username: **braccobaldo**
URL: https://www.pythonanywhere.com/user/braccobaldo/

## 🚀 Setup Veloce (5 minuti)

### STEP 1: Console Bash
1. Vai su https://www.pythonanywhere.com/user/braccobaldo/
2. Clicca **Consoles** tab
3. Clicca **Bash** (nuova console)
4. Attendi che si apra

### STEP 2: Clona e Installa (Copia tutto questo)
Nella console Bash, incolla e premi Enter:

```bash
cd ~ && git clone https://github.com/ballales1984-wq/newsflow.git && cd newsflow/backend && pip3.10 install --user fastapi uvicorn pydantic pydantic-settings python-multipart python-slugify mangum && echo "✅ Setup completato!" && pwd
```

### STEP 3: Crea Web App
1. Vai su **Web** tab
2. Clicca **Add a new web app**
3. Scegli **Flask**, Python 3.10
4. Path: `/home/braccobaldo/newsflow`

### STEP 4: Configura WSGI
1. **Web** tab → Clicca su **WSGI configuration file**
2. **Sostituisci tutto** con questo codice:

```python
import sys
import os

# Path backend
path = '/home/braccobaldo/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)

# Working directory
os.chdir(path)

# Importa app FastAPI
from app.main_simple import app

# Wrapper WSGI
application = app
```

3. Clicca **Save**

### STEP 5: Reload e Test
1. **Web** tab → Clicca **Reload** (pulsante verde)
2. Attendi 10-20 secondi
3. Clicca sul tuo URL: **https://braccobaldo.pythonanywhere.com**
4. Test API: **https://braccobaldo.pythonanywhere.com/api/v1/articles?limit=1**

## ✅ Fatto!
Il backend è online su: **https://braccobaldo.pythonanywhere.com**

## 📝 Aggiorna Frontend
Aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://braccobaldo.pythonanywhere.com/api/v1'
```

## 🔧 Troubleshooting

**Errore 500?**
- Controlla **Error log** in Web tab
- Verifica che il path sia corretto: `/home/braccobaldo/newsflow/backend`

**Module not found?**
- Esegui nella console: `pip3.10 install --user -r requirements.txt`

**File JSON non trovato?**
- Verifica che `final_news_italian.json` sia in `backend/`

## 🎉 Risultato
✅ Backend sempre online!
✅ Gratuito per sempre!
✅ Puoi spegnere il PC!


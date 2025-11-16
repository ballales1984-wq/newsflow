# 🚀 Quick Setup PythonAnywhere (5 minuti)

## ⚡ Setup Veloce

### 1. Crea Account (1 minuto)
- Vai su https://www.pythonanywhere.com
- Clicca **Beginner account** (gratuito)
- Registrati con email
- Verifica email

### 2. Esegui Script Automatico (2 minuti)
1. Dashboard → **Consoles** → **Bash**
2. Copia e incolla questo comando:

```bash
cd ~ && git clone https://github.com/ballales1984-wq/newsflow.git && cd newsflow/backend && pip3.10 install --user fastapi uvicorn pydantic pydantic-settings python-multipart python-slugify mangum && echo "✅ Setup completato! Path: $(pwd)" && echo "Username: $(whoami)"
```

3. **Copia il path e username** che vengono mostrati!

### 3. Crea Web App (1 minuto)
1. Dashboard → **Web** tab
2. Clicca **Add a new web app**
3. Scegli **Flask**, Python 3.10
4. Path: `/home/TUO_USERNAME/newsflow` (usa il path copiato prima)

### 4. Configura WSGI (1 minuto)
1. Dashboard → **Web** → **WSGI configuration file**
2. **Sostituisci tutto** con questo (cambia TUO_USERNAME!):

```python
import sys
import os

username = 'TUO_USERNAME'  # <-- CAMBIA QUESTO con il tuo username!
path = f'/home/{username}/newsflow/backend'
if path not in sys.path:
    sys.path.insert(0, path)
os.chdir(path)

from app.main_simple import app
application = app
```

3. Clicca **Save**

### 5. Reload e Test (30 secondi)
1. Dashboard → **Web** → Clicca **Reload** (verde)
2. Attendi 10 secondi
3. Clicca sul tuo URL: `https://TUO_USERNAME.pythonanywhere.com`
4. Test API: `https://TUO_USERNAME.pythonanywhere.com/api/v1/articles?limit=1`

## ✅ Fatto!
Il backend è online! Aggiorna il frontend con il nuovo URL.

## 🔧 Troubleshooting

**Errore 500?**
- Controlla **Error log** in Dashboard → **Web**
- Verifica che username sia corretto in WSGI
- Verifica che path sia corretto

**Module not found?**
- Esegui: `pip3.10 install --user -r requirements.txt` nella console

**File JSON non trovato?**
- Verifica che `final_news_italian.json` sia in `backend/`

## 📝 Aggiorna Frontend
Dopo deploy, aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://TUO_USERNAME.pythonanywhere.com/api/v1'
```


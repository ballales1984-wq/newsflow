# 🐍 Deploy Backend su PythonAnywhere (100% GRATUITO - Nessuna carta!)

## ✅ Vantaggi PythonAnywhere
- **100% GRATUITO**: Nessuna carta di credito richiesta
- **Sempre online**: Nessun sleep mode
- **Facile da usare**: Console Python integrata
- **HTTPS incluso**: Certificato SSL automatico
- **Database incluso**: MySQL gratuito

## ⚠️ Limitazioni Piano Gratuito
- **1 web app**: Solo un'applicazione
- **Domini**: Solo `*.pythonanywhere.com`
- **Storage**: 512MB
- **CPU**: Limitato (ma sufficiente per FastAPI)

## 📋 Setup PythonAnywhere (10 minuti)

### 1. Crea Account
- Vai su https://www.pythonanywhere.com
- Clicca **Beginner account** (gratuito)
- Registrati con email

### 2. Crea Web App
1. Dashboard → **Web** tab
2. Clicca **Add a new web app**
3. Scegli **Flask** (useremo FastAPI comunque)
4. Python version: **Python 3.10** (o disponibile)
5. Path: `/home/TUO_USERNAME/newsflow`

### 3. Upload Codice
**Opzione A: Git (consigliato)**
```bash
# Nella console Bash di PythonAnywhere
cd ~
git clone https://github.com/ballales1984-wq/newsflow.git
cd newsflow/backend
```

**Opzione B: Upload manuale**
- Dashboard → **Files** tab
- Upload file backend

### 4. Installa Dipendenze
Nella **Console Bash**:
```bash
cd ~/newsflow/backend
pip3.10 install --user -r requirements.txt
```

### 5. Configura WSGI
Dashboard → **Web** → **WSGI configuration file**

Sostituisci tutto con:
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

### 6. Configura Static Files
Dashboard → **Web** → **Static files**:
- URL: `/static`
- Directory: `/home/TUO_USERNAME/newsflow/backend/static`

### 7. Reload Web App
Dashboard → **Web** → Clicca **Reload**

### 8. Ottieni URL
URL sarà: `https://TUO_USERNAME.pythonanywhere.com`

## 📝 Aggiorna Frontend
Dopo il deploy, aggiorna `frontend/src/environments/environment.prod.ts`:
```typescript
apiUrl: 'https://TUO_USERNAME.pythonanywhere.com/api/v1'
```

## 🔄 Deploy Automatico
PythonAnywhere non ha deploy automatico da GitHub, ma puoi:
1. Usare **Tasks** per pull automatico
2. O fare pull manuale quando necessario

## 💰 Costi
- **Gratuito**: Per sempre!
- **Nessuna carta di credito**: Mai richiesta
- **Limiti**: 1 app, 512MB storage

## ⚠️ Note Importanti
- **Sempre online**: Nessun sleep mode! ✅
- **Domini**: Solo `*.pythonanywhere.com`
- **HTTPS**: Incluso automaticamente
- **Logs**: Dashboard → **Web** → **Error log**

## 🎯 Risultato
✅ Backend sempre online (nessun sleep mode!)
✅ 100% GRATUITO (nessuna carta di credito!)
✅ HTTPS incluso
✅ Puoi spegnere il PC!

## 🆚 Confronto
| Feature | Render | Railway | Fly.io | PythonAnywhere |
|---------|--------|---------|--------|-----------------|
| Gratuito | ⚠️ 750h/mese | ⚠️ $5 credito | ⚠️ Richiede carta | ✅ 100% gratis |
| Carta di credito | ❌ No | ✅ Sì | ✅ Sì | ❌ No |
| Sleep Mode | ⚠️ Sì | ✅ No | ✅ No | ✅ No |
| Setup | Facile | Facilissimo | Medio | Facile |
| Domini | ✅ Custom | ✅ Custom | ✅ Custom | ⚠️ Solo *.pythonanywhere.com |

## 🎉 Vantaggi PythonAnywhere
✅ **VERAMENTE GRATUITO** (nessuna carta!)
✅ Nessun sleep mode
✅ Sempre online
✅ Facile da usare
✅ Console Python integrata


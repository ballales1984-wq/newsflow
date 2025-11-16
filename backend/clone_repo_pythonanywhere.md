# 📋 Clona Repository su PythonAnywhere

## ⚡ Comandi da Eseguire

Vai su: **https://www.pythonanywhere.com/user/braccobaldo/**

1. Clicca **Consoles** tab
2. Clicca **Bash** (nuova console)
3. Incolla e esegui questi comandi:

```bash
cd ~
git clone https://github.com/ballales1984-wq/newsflow.git
cd newsflow/backend
pip3.10 install --user fastapi uvicorn pydantic pydantic-settings python-multipart python-slugify mangum
echo "✅ Setup completato!"
```

## ✅ Dopo il Clone

Torna qui e dimmi quando hai finito! Farò il reload finale della webapp.

## 🧪 Test

Dopo il clone, testa:
- https://braccobaldo.pythonanywhere.com/api/v1/articles?limit=1

Dovresti vedere JSON con gli articoli!


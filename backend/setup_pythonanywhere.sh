#!/bin/bash
# Script per setup automatico su PythonAnywhere
# Esegui questo script nella console Bash di PythonAnywhere

echo "🐍 Setup NewsFlow Backend su PythonAnywhere"
echo "=========================================="
echo ""

# Colora output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Clona repository
echo -e "${YELLOW}[1/5] Clonando repository...${NC}"
cd ~
if [ -d "newsflow" ]; then
    echo "Repository già esistente, aggiorno..."
    cd newsflow
    git pull
else
    git clone https://github.com/ballales1984-wq/newsflow.git
    cd newsflow
fi

# Step 2: Vai in backend
echo -e "${YELLOW}[2/5] Entrando in directory backend...${NC}"
cd backend
pwd

# Step 3: Installa dipendenze
echo -e "${YELLOW}[3/5] Installando dipendenze...${NC}"
pip3.10 install --user fastapi uvicorn pydantic pydantic-settings python-multipart python-slugify mangum

# Step 4: Verifica file
echo -e "${YELLOW}[4/5] Verificando file...${NC}"
if [ -f "app/main_simple.py" ]; then
    echo -e "${GREEN}✅ app/main_simple.py trovato${NC}"
else
    echo "❌ app/main_simple.py non trovato!"
    exit 1
fi

if [ -f "final_news_italian.json" ]; then
    echo -e "${GREEN}✅ final_news_italian.json trovato${NC}"
else
    echo "⚠️  final_news_italian.json non trovato (opzionale)"
fi

# Step 5: Mostra path
echo -e "${YELLOW}[5/5] Setup completato!${NC}"
echo ""
echo -e "${GREEN}✅ Repository clonato e dipendenze installate${NC}"
echo ""
echo "📋 Prossimi passi:"
echo "1. Vai su Dashboard → Web tab"
echo "2. Clicca 'Add a new web app'"
echo "3. Scegli Flask, Python 3.10"
echo "4. Path: $(pwd)"
echo "5. Configura WSGI (vedi SETUP_PYTHONANYWHERE.md)"
echo "6. Reload web app"
echo ""
echo "Path completo: $(pwd)"
echo "Username: $(whoami)"


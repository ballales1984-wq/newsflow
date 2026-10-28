#!/bin/bash

# NewsFlow Quick Start Script
# Questo script automatizza il setup iniziale dell'ambiente di sviluppo

set -e  # Exit on error

echo "🚀 NewsFlow Quick Start"
echo "======================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

command -v python3 >/dev/null 2>&1 || { echo -e "${RED}Python 3 not found. Please install Python 3.11+${NC}"; exit 1; }
command -v node >/dev/null 2>&1 || { echo -e "${RED}Node.js not found. Please install Node.js 18+${NC}"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo -e "${YELLOW}Docker not found. Will skip Docker setup${NC}"; SKIP_DOCKER=1; }

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Ask user for setup method
echo "Select setup method:"
echo "1) Full setup with Docker (recommended)"
echo "2) Manual setup (requires PostgreSQL and Redis installed)"
read -p "Enter choice [1-2]: " setup_choice

if [ "$setup_choice" = "1" ] && [ -z "$SKIP_DOCKER" ]; then
    echo ""
    echo "🐳 Setting up with Docker..."
    
    # Start Docker services
    docker-compose up -d postgres redis
    
    echo "Waiting for services to be ready..."
    sleep 10
    
    # Backend setup
    echo ""
    echo "🔧 Setting up Backend..."
    cd backend
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate || . venv/Scripts/activate
    
    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Download NLP models
    echo "Downloading NLP models (this may take a while)..."
    python -m spacy download it_core_news_lg
    python -m spacy download en_core_web_lg
    
    # Copy env file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠ Please edit backend/.env with your configuration${NC}"
    fi
    
    # Initialize database
    echo "Initializing database..."
    python init_db.py
    
    cd ..
    
    # Frontend setup
    echo ""
    echo "🎨 Setting up Frontend..."
    cd frontend
    npm install
    cd ..
    
    echo ""
    echo -e "${GREEN}✅ Setup completed!${NC}"
    echo ""
    echo "To start the application:"
    echo ""
    echo "Terminal 1 (Backend):"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
    echo ""
    echo "Terminal 2 (Frontend):"
    echo "  cd frontend"
    echo "  npm start"
    echo ""
    echo "Or use Docker:"
    echo "  docker-compose up"
    echo ""
    
elif [ "$setup_choice" = "2" ]; then
    echo ""
    echo "📝 Manual Setup"
    echo ""
    echo "Please ensure PostgreSQL and Redis are running."
    read -p "Press enter to continue..."
    
    # Backend setup
    echo ""
    echo "🔧 Setting up Backend..."
    cd backend
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate || . venv/Scripts/activate
    
    # Install dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Download NLP models
    echo "Downloading NLP models (this may take a while)..."
    python -m spacy download it_core_news_lg
    python -m spacy download en_core_web_lg
    
    # Copy env file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠ Please edit backend/.env with your configuration${NC}"
        read -p "Press enter after editing .env..."
    fi
    
    # Initialize database
    echo "Initializing database..."
    python init_db.py
    
    cd ..
    
    # Frontend setup
    echo ""
    echo "🎨 Setting up Frontend..."
    cd frontend
    npm install
    cd ..
    
    echo ""
    echo -e "${GREEN}✅ Setup completed!${NC}"
    echo ""
    echo "To start the application:"
    echo ""
    echo "Terminal 1 (Backend):"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
    echo ""
    echo "Terminal 2 (Frontend):"
    echo "  cd frontend"
    echo "  npm start"
    echo ""
    
else
    echo -e "${RED}Invalid choice${NC}"
    exit 1
fi

echo "🌐 Access the application:"
echo "  Frontend: http://localhost:4200"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/api/docs"
echo ""
echo "📚 Read SETUP.md for detailed instructions"
echo "🚀 Read DEPLOYMENT.md for production deployment"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"


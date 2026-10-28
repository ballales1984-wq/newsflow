@echo off
REM NewsFlow Quick Start Script for Windows
REM This script automates the initial development environment setup

echo ================================
echo NewsFlow Quick Start (Windows)
echo ================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3 not found. Please install Python 3.11+
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    exit /b 1
)

where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Docker not found. Will skip Docker setup
    set SKIP_DOCKER=1
)

echo [OK] Prerequisites check passed
echo.

REM Ask user for setup method
echo Select setup method:
echo 1) Full setup with Docker (recommended)
echo 2) Manual setup (requires PostgreSQL and Redis installed)
set /p setup_choice="Enter choice [1-2]: "

if "%setup_choice%"=="1" (
    if not defined SKIP_DOCKER (
        echo.
        echo Setting up with Docker...
        
        REM Start Docker services
        docker-compose up -d postgres redis
        
        echo Waiting for services to be ready...
        timeout /t 10 /nobreak >nul
        
        REM Backend setup
        echo.
        echo Setting up Backend...
        cd backend
        
        REM Create virtual environment
        python -m venv venv
        call venv\Scripts\activate
        
        REM Install dependencies
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
        REM Download NLP models
        echo Downloading NLP models (this may take a while)...
        python -m spacy download it_core_news_lg
        python -m spacy download en_core_web_lg
        
        REM Copy env file
        if not exist .env (
            copy .env.example .env
            echo [WARNING] Please edit backend\.env with your configuration
        )
        
        REM Initialize database
        echo Initializing database...
        python init_db.py
        
        cd ..
        
        REM Frontend setup
        echo.
        echo Setting up Frontend...
        cd frontend
        call npm install
        cd ..
        
        echo.
        echo [SUCCESS] Setup completed!
        echo.
        echo To start the application:
        echo.
        echo Terminal 1 (Backend):
        echo   cd backend
        echo   venv\Scripts\activate
        echo   uvicorn app.main:app --reload
        echo.
        echo Terminal 2 (Frontend):
        echo   cd frontend
        echo   npm start
        echo.
        echo Or use Docker:
        echo   docker-compose up
        echo.
    )
) else if "%setup_choice%"=="2" (
    echo.
    echo Manual Setup
    echo.
    echo Please ensure PostgreSQL and Redis are running.
    pause
    
    REM Backend setup
    echo.
    echo Setting up Backend...
    cd backend
    
    REM Create virtual environment
    python -m venv venv
    call venv\Scripts\activate
    
    REM Install dependencies
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    REM Download NLP models
    echo Downloading NLP models (this may take a while)...
    python -m spacy download it_core_news_lg
    python -m spacy download en_core_web_lg
    
    REM Copy env file
    if not exist .env (
        copy .env.example .env
        echo [WARNING] Please edit backend\.env with your configuration
        pause
    )
    
    REM Initialize database
    echo Initializing database...
    python init_db.py
    
    cd ..
    
    REM Frontend setup
    echo.
    echo Setting up Frontend...
    cd frontend
    call npm install
    cd ..
    
    echo.
    echo [SUCCESS] Setup completed!
    echo.
    echo To start the application:
    echo.
    echo Terminal 1 (Backend):
    echo   cd backend
    echo   venv\Scripts\activate
    echo   uvicorn app.main:app --reload
    echo.
    echo Terminal 2 (Frontend):
    echo   cd frontend
    echo   npm start
    echo.
) else (
    echo [ERROR] Invalid choice
    exit /b 1
)

echo.
echo Access the application:
echo   Frontend: http://localhost:4200
echo   Backend API: http://localhost:8000
echo   API Docs: http://localhost:8000/api/docs
echo.
echo Read SETUP.md for detailed instructions
echo Read DEPLOYMENT.md for production deployment
echo.
echo Happy coding!
pause


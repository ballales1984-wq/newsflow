@echo off
chcp 65001 >nul
title NewsFlow - Rigenera Notizie con Immagini
color 0A

echo.
echo ========================================
echo    RIGENERAZIONE NOTIZIE CON IMMAGINI
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Raccolta notizie con estrazione immagini...
set PYTHONIOENCODING=UTF-8
python collect_italian_priority.py
if errorlevel 1 (
    echo.
    echo ❌ Errore durante la raccolta notizie!
    pause
    exit /b 1
)

echo.
echo [2/2] Aggiornamento final_news_italian.json...
python update_news.py
if errorlevel 1 (
    echo.
    echo ❌ Errore durante l'aggiornamento!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ✅✅✅ NOTIZIE RIGENERATE!
echo ========================================
echo.
echo Le notizie sono state rigenerate con le immagini estratte.
echo Controlla il file final_news_italian.json
echo.
pause


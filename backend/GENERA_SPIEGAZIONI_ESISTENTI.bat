@echo off
chcp 65001 >nul
title NewsFlow - Genera Spiegazioni AI per Articoli Esistenti
color 0B

echo.
echo ========================================
echo    GENERAZIONE SPIEGAZIONI AI
echo    per articoli esistenti
echo ========================================
echo.
echo Questo script genera spiegazioni AI per tutti gli articoli
echo già presenti nel file final_news_italian.json
echo.
echo ⚠️  ATTENZIONE:
echo    Questo processo può richiedere 10-30 minuti
echo    a seconda del numero di articoli e della velocità AI
echo.
echo 💡 CONSIGLIO:
echo    Lascia il PC acceso e non chiudere questa finestra
echo.
pause

cd /d "%~dp0"

echo.
echo [1/2] Generazione spiegazioni AI...
echo    (Questo può richiedere diversi minuti)
echo.

python genera_spiegazioni_esistenti.py

if errorlevel 1 (
    echo.
    echo ❌ Errore durante la generazione!
    pause
    exit /b 1
)

echo.
echo [2/2] Copia file aggiornato in api/...
set "API_DIR=%~dp0..\api"

if not exist "%API_DIR%" (
    mkdir "%API_DIR%"
    echo ✅ Cartella api/ creata
)

if exist "final_news_italian.json" (
    copy /Y "final_news_italian.json" "%API_DIR%\final_news_italian.json" >nul
    echo ✅ final_news_italian.json copiato in api/
)

echo.
echo ========================================
echo    COMPLETATO!
echo ========================================
echo.
echo ✅ Spiegazioni AI generate e salvate
echo ✅ File copiato in api/
echo.
echo Le spiegazioni sono ora disponibili nel JSON
echo e verranno caricate istantaneamente dal sito!
echo.
pause


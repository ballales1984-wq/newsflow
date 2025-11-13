@echo off
chcp 65001 >nul
echo ========================================
echo   AGGIORNAMENTO NOTIZIE MANUALE
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Attivazione ambiente virtuale Python...
if exist "backend\venv\Scripts\activate.bat" (
    call backend\venv\Scripts\activate.bat
    echo ✅ Ambiente virtuale attivato
) else (
    echo ⚠️  Ambiente virtuale non trovato, uso Python di sistema
)

echo.
echo [2/3] Raccolta notizie italiane prioritarie...
cd backend
set PYTHONIOENCODING=UTF-8
python collect_italian_priority.py
if errorlevel 1 (
    echo ❌ Errore durante la raccolta notizie!
    pause
    exit /b 1
)
echo ✅ Notizie raccolte

echo.
echo [3/3] Copia file per update_news.py...
copy /Y italian_priority_news.json all_sources_news.json >nul
echo ✅ File copiato

echo.
echo [4/4] Aggiornamento final_news_italian.json...
python update_news.py
if errorlevel 1 (
    echo ❌ Errore durante l'aggiornamento!
    pause
    exit /b 1
)
echo ✅ Notizie aggiornate

echo.
echo ========================================
echo   AGGIORNAMENTO COMPLETATO!
echo ========================================
echo.
echo Ora puoi fare commit e push:
echo   git add backend/final_news_italian.json backend/all_sources_news.json backend/italian_priority_news.json
echo   git commit -m "🤖 Manual update: Aggiornate notizie"
echo   git push origin main
echo.
pause


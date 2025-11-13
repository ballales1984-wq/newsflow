@echo off
chcp 65001 >nul
title NewsFlow - Aggiorna Notizie
color 0B

echo.
echo ========================================
echo    AGGIORNAMENTO NOTIZIE NEWSFLOW
echo ========================================
echo.

cd /d "%~dp0"
set "BACKEND_DIR=%~dp0"
set "API_DIR=%~dp0..\api"

echo [1/4] Verifica backend attivo...
timeout /t 2 /nobreak >nul
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend non attivo!
    echo    Avvia prima il backend con AVVIA_TUTTO.bat
    pause
    exit /b 1
)
echo ✅ Backend attivo
echo.

echo [2/4] Aggiornamento notizie tramite API...
echo    Questo potrebbe richiedere 1-2 minuti...
echo.

powershell -Command "$ngrokUrl = 'https://tonita-deposable-manneristically.ngrok-free.dev'; $headers = @{'ngrok-skip-browser-warning' = 'true'}; try { $response = Invoke-RestMethod -Uri \"$ngrokUrl/api/admin/collect-news\" -Method Post -Headers $headers -TimeoutSec 120; Write-Host '✅ Notizie aggiornate!' -ForegroundColor Green; Write-Host \"   Articoli totali: $($response.total_articles)\" -ForegroundColor Gray; Write-Host \"   Messaggio: $($response.message)\" -ForegroundColor Gray; exit 0 } catch { Write-Host '❌ Errore:' -ForegroundColor Red; Write-Host $_.Exception.Message -ForegroundColor Yellow; exit 1 }"

if errorlevel 1 (
    echo.
    echo ❌ Errore durante l'aggiornamento!
    pause
    exit /b 1
)

echo.
echo [3/4] Copia file aggiornati in api/...
if not exist "%API_DIR%" (
    mkdir "%API_DIR%"
    echo ✅ Cartella api/ creata
)

if exist "%BACKEND_DIR%final_news_italian.json" (
    copy /Y "%BACKEND_DIR%final_news_italian.json" "%API_DIR%\final_news_italian.json" >nul
    echo ✅ final_news_italian.json copiato
) else (
    echo ⚠️  final_news_italian.json non trovato in backend/
)

if exist "%BACKEND_DIR%all_sources_news.json" (
    copy /Y "%BACKEND_DIR%all_sources_news.json" "%API_DIR%\all_sources_news.json" >nul
    echo ✅ all_sources_news.json copiato
)

echo.
echo [4/4] Riavvio backend per caricare nuove notizie...
echo    Chiudo processo backend esistente...
powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*python*' } | Stop-Process -Force -ErrorAction SilentlyContinue"
timeout /t 2 /nobreak >nul

echo    Avvio nuovo backend...
start "NewsFlow Backend" /MIN powershell -NoExit -Command "cd '%BACKEND_DIR%'; $env:CORS_ORIGINS='https://newsflow-orcin.vercel.app,http://localhost:4200'; Write-Host '=== BACKEND NEWSFLOW (RIAVVIATO) ===' -ForegroundColor Green; Write-Host 'Caricamento nuove notizie...' -ForegroundColor Cyan; python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo    Verifica nuove notizie...
powershell -Command "$ngrokUrl = 'https://tonita-deposable-manneristically.ngrok-free.dev'; $headers = @{'ngrok-skip-browser-warning' = 'true'}; Start-Sleep -Seconds 3; try { $articles = Invoke-RestMethod -Uri \"$ngrokUrl/api/v1/articles\" -Headers $headers -TimeoutSec 5; Write-Host \"   Articoli disponibili: $($articles.total)\" -ForegroundColor Green; if ($articles.total -ge 80) { Write-Host '   ✅✅✅ NUOVE NOTIZIE CARICATE!' -ForegroundColor Green } } catch { Write-Host '   ⚠️  Backend ancora in avvio...' -ForegroundColor Yellow }"

echo.
echo ========================================
echo    AGGIORNAMENTO COMPLETATO!
echo ========================================
echo.
echo ✅ Notizie aggiornate
echo ✅ File copiati in api/
echo ✅ Backend riavviato
echo.
echo Le nuove notizie sono disponibili sul sito!
echo Ricarica la pagina (CTRL+F5) per vederle.
echo.
pause


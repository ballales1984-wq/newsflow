@echo off
title NewsFlow - Backend + ngrok (SEMPRE ATTIVO)
color 0A

echo ========================================
echo   NEWSFLOW - BACKEND + NGROK
echo   Avvia backend e ngrok in background
echo ========================================
echo.

cd /d %~dp0

REM Avvia backend in background
echo [1/2] Avvio backend su porta 8000...
start "NewsFlow Backend" /MIN powershell -NoExit -Command "cd '%CD%'; $env:CORS_ORIGINS='https://newsflow-orcin.vercel.app,http://localhost:4200'; Write-Host '=== BACKEND NEWSFLOW ===' -ForegroundColor Green; Write-Host 'Backend su http://localhost:8000' -ForegroundColor Cyan; Write-Host 'URL ngrok: https://tonita-deposable-manneristically.ngrok-free.dev' -ForegroundColor Yellow; Write-Host ''; python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

REM Avvia ngrok in background
echo [2/2] Avvio ngrok tunnel...
start "NewsFlow ngrok" powershell -NoExit -Command "cd '%CD%'; Write-Host '=== NGROK TUNNEL ===' -ForegroundColor Cyan; Write-Host ''; Write-Host 'URL: https://tonita-deposable-manneristically.ngrok-free.dev' -ForegroundColor Green; Write-Host 'Espone backend su porta 8000' -ForegroundColor Yellow; Write-Host 'IMPORTANTE: Mantieni questo terminale aperto!' -ForegroundColor Red; Write-Host ''; .\ngrok.exe http 8000"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   ✅ TUTTO AVVIATO!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo ngrok:   https://tonita-deposable-manneristically.ngrok-free.dev
echo.
echo IMPORTANTE:
echo - Mantieni i terminali aperti
echo - Non chiudere ngrok o il backend si disconnette
echo - Il PC deve rimanere acceso
echo.
pause


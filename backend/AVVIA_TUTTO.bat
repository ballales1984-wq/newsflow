@echo off
chcp 65001 >nul
title NewsFlow - Backend + ngrok
color 0A

echo.
echo ========================================
echo    NEWSFLOW - AVVIO AUTOMATICO
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Avvio Backend...
start "NewsFlow Backend" /MIN powershell -NoExit -Command "cd '%CD%'; $env:CORS_ORIGINS='https://newsflow-orcin.vercel.app,http://localhost:4200'; Write-Host '=== BACKEND NEWSFLOW ===' -ForegroundColor Green; Write-Host 'Backend su http://localhost:8000' -ForegroundColor Cyan; Write-Host ''; python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo [2/2] Avvio ngrok...
start "NewsFlow ngrok" powershell -NoExit -Command "cd '%CD%'; Write-Host '=== NGROK TUNNEL ===' -ForegroundColor Cyan; Write-Host ''; Write-Host 'URL: https://tonita-deposable-manneristically.ngrok-free.dev' -ForegroundColor Green; Write-Host ''; .\ngrok.exe http 8000"

timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo    TUTTO AVVIATO!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo ngrok: https://tonita-deposable-manneristically.ngrok-free.dev
echo Frontend: https://newsflow-orcin.vercel.app
echo.
echo I terminali sono stati aperti in finestre separate.
echo NON CHIUDERE i terminali per mantenere il sito attivo!
echo.
pause


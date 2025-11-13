@echo off
chcp 65001 >nul
title NewsFlow - Avvio Automatico
color 0A

REM Script per avvio automatico (senza pause)
REM Questo script viene eseguito all'avvio di Windows

cd /d "%~dp0"

REM Avvia backend in background
start "NewsFlow Backend" /MIN powershell -NoExit -Command "cd '%CD%'; $env:CORS_ORIGINS='https://newsflow-orcin.vercel.app,http://localhost:4200'; Write-Host '=== BACKEND NEWSFLOW (AUTO) ===' -ForegroundColor Green; Write-Host 'Backend su http://localhost:8000' -ForegroundColor Cyan; Write-Host 'Avviato automaticamente all''avvio di Windows' -ForegroundColor Gray; Write-Host ''; python -m uvicorn app.main_simple:app --host 0.0.0.0 --port 8000"

REM Attendi che il backend si avvii
timeout /t 5 /nobreak >nul

REM Avvia ngrok in background
start "NewsFlow ngrok" /MIN powershell -NoExit -Command "cd '%CD%'; Write-Host '=== NGROK TUNNEL (AUTO) ===' -ForegroundColor Cyan; Write-Host ''; Write-Host 'URL: https://tonita-deposable-manneristically.ngrok-free.dev' -ForegroundColor Green; Write-Host 'Avviato automaticamente all''avvio di Windows' -ForegroundColor Gray; Write-Host ''; .\ngrok.exe http 8000"

REM Script termina senza pause - perfetto per avvio automatico
exit


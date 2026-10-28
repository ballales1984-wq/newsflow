@echo off
chcp 65001 >nul
title NewsFlow - Attiva Automazione 24H
color 0A

echo.
echo ========================================
echo    ATTIVAZIONE AUTOMAZIONE 24H
echo ========================================
echo.
echo Questo script creerà un task Windows che esegue
echo automaticamente l'aggiornamento ogni giorno alle 06:00
echo.
echo ⚠️  RICHIEDE PRIVILEGI DI AMMINISTRATORE
echo.
pause

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoExit', '-File', '%CD%\CREA_AUTOMAZIONE_24H.ps1'"

echo.
echo ========================================
echo    ✅ PowerShell avviato come Admin
echo ========================================
echo.
echo Nella finestra PowerShell che si è aperta:
echo 1. Se richiesto, conferma l'elevazione
echo 2. Lo script creerà automaticamente il task
echo 3. Chiudi la finestra quando finito
echo.
pause


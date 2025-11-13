@echo off
chcp 65001 >nul
title NewsFlow - Reminder Lancio Product Hunt
color 0E

echo.
echo ========================================
echo    🚀 REMINDER LANCIO PRODUCT HUNT
echo ========================================
echo.
echo ⏰ ORA: %TIME%
echo 📅 DATA: %DATE%
echo.
echo ⚠️  IMPORTANTE: Lancio alle 9:00!
echo.
echo 📋 COSA FARE ORA:
echo.
echo    1. Avvia backend e ngrok:
echo       Doppio click su: AVVIA_TUTTO.bat
echo.
echo    2. Verifica sito:
echo       https://newsflow-orcin.vercel.app
echo.
echo    3. Alle 9:00:
echo       Clicca "Make it live" su Product Hunt
echo.
echo ========================================
echo.
echo Vuoi avviare backend e ngrok ora? (S/N)
set /p choice="> "

if /i "%choice%"=="S" (
    echo.
    echo Avvio backend e ngrok...
    call AVVIA_TUTTO.bat
) else (
    echo.
    echo Ricorda di avviare AVVIA_TUTTO.bat alle 8:50!
    echo.
    pause
)


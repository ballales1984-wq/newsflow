@echo off
chcp 65001 >nul
echo.
echo === CONFIGURAZIONE NGROK ===
echo.
echo 1. Vai su: https://dashboard.ngrok.com/get-started/your-authtoken
echo 2. Copia il token che vedi
echo 3. Incollalo qui sotto quando richiesto
echo.
set /p TOKEN="Incolla il token ngrok qui: "
echo.
echo Configurazione in corso...
ngrok.exe config add-authtoken %TOKEN%
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅✅✅ NGROK CONFIGURATO!
    echo.
    echo Ora puoi avviare il backend con:
    echo    AVVIA_BACKEND_NGROK.ps1
) else (
    echo ❌ Errore durante la configurazione
)
echo.
pause


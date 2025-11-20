@echo off
REM Script batch per aggiornamento automatico notizie (alternativa a .ps1)
REM Può essere usato con Task Scheduler se PowerShell non è disponibile

cd /d "%~dp0"
echo.
echo ======================================================================
echo 🔄 AGGIORNAMENTO AUTOMATICO NOTIZIE
echo ======================================================================
echo.

REM Esegui script PowerShell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0AGGIORNA_NOTIZIE_AUTOMATICO.ps1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Aggiornamento completato con successo!
) else (
    echo.
    echo ❌ Errore durante l'aggiornamento
    exit /b %ERRORLEVEL%
)


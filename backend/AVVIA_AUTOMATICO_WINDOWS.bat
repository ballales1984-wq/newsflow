@echo off
chcp 65001 >nul
title NewsFlow - Setup Avvio Automatico Windows
color 0E

echo.
echo ========================================
echo    SETUP AVVIO AUTOMATICO WINDOWS
echo ========================================
echo.
echo Questo script aggiunge NewsFlow all'avvio automatico
echo di Windows, cosi' backend e ngrok si avviano da soli.
echo.

set "SCRIPT_PATH=%~dp0AVVIA_TUTTO.bat"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\NewsFlow.lnk"

echo Script da aggiungere: %SCRIPT_PATH%
echo Cartella avvio: %STARTUP_FOLDER%
echo.

pause

echo.
echo Creazione collegamento...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Avvia NewsFlow Backend e ngrok'; $Shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo.
    echo ========================================
    echo    SUCCESSO!
    echo ========================================
    echo.
    echo NewsFlow sara' avviato automaticamente
    echo ad ogni riavvio di Windows!
    echo.
    echo Per rimuovere l'avvio automatico:
    echo   Elimina: %SHORTCUT_PATH%
    echo.
) else (
    echo.
    echo ERRORE: Impossibile creare il collegamento.
    echo Prova ad eseguire come Amministratore.
    echo.
)

pause


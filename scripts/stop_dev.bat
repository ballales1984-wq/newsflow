@echo off
echo ==========================================
echo   NEWSFLOW - Stopping Development
echo ==========================================
echo.

echo Fermando tutti i processi...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul

echo.
echo ==========================================
echo   TUTTO FERMATO!
echo ==========================================
echo.
pause


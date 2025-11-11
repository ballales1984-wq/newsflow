@echo off
echo ==========================================
echo   NEWSFLOW - Development Environment
echo ==========================================
echo.

echo [1/3] Pulendo processi precedenti...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/3] Avviando Backend (porta 8000)...
start "NewsFlow Backend" cmd /k "cd backend && .\venv\Scripts\activate && python -m uvicorn app.main_simple:app --reload --port 8000"

echo [3/3] Avviando Frontend (porta 4200)...
timeout /t 3 /nobreak >nul
start "NewsFlow Frontend" cmd /k "cd frontend && npm start"

echo.
echo ==========================================
echo   NEWSFLOW AVVIATO!
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:4200
echo.
echo Premi un tasto per chiudere questo prompt...
echo (I server continueranno in finestre separate)
pause >nul


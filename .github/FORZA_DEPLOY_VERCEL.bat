@echo off
chcp 65001 >nul
title NewsFlow - Forza Deploy Vercel
color 0A

echo.
echo ========================================
echo    FORZA DEPLOY SU VERCEL
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Creazione commit vuoto per triggerare deploy...
git commit --allow-empty -m "🚀 FORCE DEPLOY: Trigger Vercel - %date% %time%"
if errorlevel 1 (
    echo ⚠️  Nessun commit necessario o errore
)

echo.
echo [2/2] Push su GitHub...
git push origin main
if errorlevel 1 (
    echo.
    echo ❌ Errore durante il push!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ✅ DEPLOY TRIGGERATO!
echo ========================================
echo.
echo Il deploy su Vercel partirà automaticamente.
echo Controlla lo stato su: https://vercel.com/dashboard
echo.
echo Attendi 2-3 minuti per il completamento.
echo.
pause


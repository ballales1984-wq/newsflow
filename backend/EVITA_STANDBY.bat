@echo off
chcp 65001 >nul
title NewsFlow - Configurazione Anti-Standby
color 0B

echo.
echo ========================================
echo    CONFIGURAZIONE ANTI-STANDBY
echo ========================================
echo.
echo Questo script configura Windows per NON andare
echo in standby quando collegato alla corrente.
echo.
echo IMPORTANTE: Il sito si chiude se il PC va in standby!
echo.
pause

echo.
echo [1/3] Configurazione alimentazione...
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 0

echo.
echo [2/3] Disabilitazione sleep quando collegato...
powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP STANDBYIDLE 0
powercfg /setacvalueindex SCHEME_CURRENT SUB_SLEEP HIBERNATEIDLE 0
powercfg /setactive SCHEME_CURRENT

echo.
echo [3/3] Verifica configurazione...
powercfg /query SCHEME_CURRENT SUB_SLEEP

echo.
echo ========================================
echo    CONFIGURAZIONE COMPLETATA!
echo ========================================
echo.
echo Il PC NON andra' in standby quando collegato alla corrente.
echo.
echo Per ripristinare le impostazioni originali:
echo   powercfg /change standby-timeout-ac 30
echo.
pause


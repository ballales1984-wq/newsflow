# Script per deploy completo
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   DEPLOY COMPLETO NEWSFLOW" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootDir

Write-Host "[1/4] Sincronizzazione file JSON..." -ForegroundColor Yellow

# Sincronizza final_news_italian.json
if (Test-Path "backend\final_news_italian.json") {
    Copy-Item -Path "backend\final_news_italian.json" -Destination "api\final_news_italian.json" -Force
    Copy-Item -Path "backend\final_news_italian.json" -Destination "frontend\src\assets\final_news_italian.json" -Force
    Write-Host "   ✅ final_news_italian.json sincronizzato" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  backend\final_news_italian.json non trovato" -ForegroundColor Yellow
}

# Sincronizza digest.json
if (Test-Path "backend\digest.json") {
    Copy-Item -Path "backend\digest.json" -Destination "api\digest.json" -Force
    Copy-Item -Path "backend\digest.json" -Destination "frontend\src\assets\digest.json" -Force
    Write-Host "   ✅ digest.json sincronizzato" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  backend\digest.json non trovato" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[2/4] Verifica stato Git..." -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "[3/4] Aggiunta file a Git..." -ForegroundColor Yellow
git add backend/final_news_italian.json backend/digest.json api/final_news_italian.json api/digest.json frontend/src/assets/final_news_italian.json frontend/src/assets/digest.json -ErrorAction SilentlyContinue
git add backend/collect_italian_priority.py -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "[4/4] Commit e Push..." -ForegroundColor Yellow
$commitMsg = "🤖 Aggiornamento: notizie con immagini + digest + fix timeout"
git commit -m $commitMsg
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ DEPLOY COMPLETATO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Il deploy su Vercel partirà automaticamente." -ForegroundColor Cyan
Write-Host ""


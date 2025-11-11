# Script per creare EXE di NewsFlow
# Salva come: CREA_EXE.ps1

Write-Host "🚀 Creazione EXE NewsFlow..." -ForegroundColor Cyan
Write-Host ""

# Vai nella cartella frontend
Set-Location "$PSScriptRoot\frontend"

# Verifica dipendenze
Write-Host "📦 Verifico dipendenze..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules\electron")) {
    Write-Host "⚠️  Electron non installato. Installo..." -ForegroundColor Yellow
    npm install
}

# Build Angular
Write-Host "`n🔨 Build Angular (production)..." -ForegroundColor Yellow
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore nel build Angular!" -ForegroundColor Red
    exit 1
}

# Build EXE con Electron
Write-Host "`n📦 Creo EXE con Electron..." -ForegroundColor Yellow
Write-Host "   ⏳ Questo richiederà 5-10 minuti..." -ForegroundColor Gray
npm run electron:build:exe
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore nella creazione EXE!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ EXE creato con successo!" -ForegroundColor Green
Write-Host "📁 Trova l'EXE in: frontend\dist-electron\" -ForegroundColor Cyan
Write-Host "`n🎉 NewsFlow è pronto come app desktop!" -ForegroundColor Green
Write-Host "`nPremi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


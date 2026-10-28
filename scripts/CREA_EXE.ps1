# Script per creare EXE di NewsFlow
# Crea un'applicazione desktop Windows da NewsFlow

Write-Host "🚀 Creazione EXE NewsFlow" -ForegroundColor Cyan
Write-Host ""

# Vai nella cartella frontend
$rootDir = $PSScriptRoot
$frontendDir = Join-Path $rootDir "frontend"
Set-Location $frontendDir

# Verifica che siamo nella directory corretta
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Directory frontend non trovata!" -ForegroundColor Red
    Write-Host "   Assicurati di essere nella root del progetto" -ForegroundColor Yellow
    exit 1
}

# Verifica dipendenze
Write-Host "📦 Verifico dipendenze..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  node_modules non trovato. Installo dipendenze..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Errore nell'installazione dipendenze!" -ForegroundColor Red
        exit 1
    }
}

# Verifica Electron
if (-not (Test-Path "node_modules\electron")) {
    Write-Host "⚠️  Electron non installato. Installo..." -ForegroundColor Yellow
    npm install electron electron-builder --save-dev
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Errore nell'installazione Electron!" -ForegroundColor Red
        exit 1
    }
}

# Build Angular
Write-Host ""
Write-Host "🔨 Build Angular (production)..." -ForegroundColor Yellow
npm run build --configuration production
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore nel build Angular!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build Angular completato!" -ForegroundColor Green

# Build EXE con Electron
Write-Host ""
Write-Host "📦 Creo EXE con Electron..." -ForegroundColor Yellow
Write-Host "   ⏳ Questo richiederà 5-10 minuti..." -ForegroundColor Gray

# Verifica se esiste script electron:build:exe
$packageJson = Get-Content "package.json" | ConvertFrom-Json
if ($packageJson.scripts.'electron:build:exe') {
    npm run electron:build:exe
} elseif ($packageJson.scripts.'electron:build') {
    npm run electron:build
} else {
    Write-Host "⚠️  Script Electron non trovato in package.json" -ForegroundColor Yellow
    Write-Host "   Aggiungi uno di questi script:" -ForegroundColor Gray
    Write-Host "   - electron:build:exe" -ForegroundColor Gray
    Write-Host "   - electron:build" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   Oppure usa electron-builder direttamente:" -ForegroundColor Gray
    Write-Host "   npx electron-builder --win" -ForegroundColor Cyan
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Errore nella creazione EXE!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ EXE creato con successo!" -ForegroundColor Green
Write-Host "📁 Trova l'EXE in: frontend\dist-electron\" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 NewsFlow è pronto come app desktop!" -ForegroundColor Green
Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


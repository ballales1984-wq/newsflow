# Script PowerShell per sincronizzare file JSON e fare deploy su Vercel
# Questo script:
# 1. Sincronizza i file JSON (root -> api -> backend)
# 2. Fa commit e push su GitHub
# 3. Vercel farà deploy automatico

Write-Host "🔄 Sincronizzazione e Deploy NewsFlow" -ForegroundColor Green
Write-Host ""

$rootDir = $PSScriptRoot

# 1. Verifica che il file principale esista
$mainFile = Join-Path $rootDir "final_news_italian.json"
if (-not (Test-Path $mainFile)) {
    Write-Host "❌ File final_news_italian.json non trovato nella root!" -ForegroundColor Red
    exit 1
}

Write-Host "📁 File principale trovato: final_news_italian.json" -ForegroundColor Green

# 2. Sincronizza i file
Write-Host ""
Write-Host "📋 Sincronizzazione file JSON..." -ForegroundColor Yellow

$apiDir = Join-Path $rootDir "api"
$backendDir = Join-Path $rootDir "backend"

# Crea directory se non esistono
if (-not (Test-Path $apiDir)) {
    New-Item -ItemType Directory -Path $apiDir -Force | Out-Null
}
if (-not (Test-Path $backendDir)) {
    New-Item -ItemType Directory -Path $backendDir -Force | Out-Null
}

# Copia file
Copy-Item $mainFile (Join-Path $apiDir "final_news_italian.json") -Force
Copy-Item $mainFile (Join-Path $backendDir "final_news_italian.json") -Force

Write-Host "   ✅ File copiato in api/" -ForegroundColor Green
Write-Host "   ✅ File copiato in backend/" -ForegroundColor Green

# 3. Verifica conteggio articoli
Write-Host ""
Write-Host "🔍 Verifica articoli..." -ForegroundColor Yellow
try {
    $jsonContent = Get-Content $mainFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $articleCount = $jsonContent.items.Count
    Write-Host "   ✅ Articoli trovati: $articleCount" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Impossibile verificare il conteggio articoli" -ForegroundColor Yellow
}

# 4. Git commit e push
Write-Host ""
Write-Host "📤 Commit e Push su GitHub..." -ForegroundColor Yellow

Set-Location $rootDir

# Verifica che sia una repository Git
if (-not (Test-Path ".git")) {
    Write-Host "   ⚠️  Directory non è una repository Git!" -ForegroundColor Yellow
    Write-Host "   Esegui 'git init' prima di continuare" -ForegroundColor Gray
    exit 1
}

# Aggiungi file modificati
git add api/final_news_italian.json backend/final_news_italian.json final_news_italian.json -ErrorAction SilentlyContinue

# Commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$commitMessage = "Auto-sync: Sincronizzazione articoli - $timestamp"
git commit -m $commitMessage 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Commit creato: $commitMessage" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  Nessuna modifica da committare" -ForegroundColor Cyan
}

# Push
Write-Host "   📤 Push su GitHub..." -ForegroundColor Yellow
git push 2>&1 | ForEach-Object {
    if ($_ -match "error" -or $_ -match "fatal") {
        Write-Host "   ❌ $_" -ForegroundColor Red
    } else {
        Write-Host "   $_" -ForegroundColor Gray
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deploy completato!" -ForegroundColor Green
    Write-Host "   Vercel avvierà il deploy automatico tra pochi secondi" -ForegroundColor Cyan
    Write-Host "   Controlla lo stato su: https://vercel.com/dashboard" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "⚠️  Errore durante il push. Verifica la connessione Git." -ForegroundColor Yellow
}

Write-Host ""


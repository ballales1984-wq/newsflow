# Script per forzare un nuovo deploy su Vercel e invalidare la cache
# Questo script:
# 1. Sincronizza i file JSON
# 2. Aggiunge un timestamp al deploy per forzare l'aggiornamento
# 3. Fa push su GitHub per triggerare Vercel

Write-Host "🔄 Forza Deploy Vercel con invalidazione cache" -ForegroundColor Green
Write-Host ""

$rootDir = $PSScriptRoot

# 1. Sincronizza file JSON
Write-Host "📋 STEP 1: Sincronizzazione file JSON..." -ForegroundColor Yellow
$mainFile = Join-Path $rootDir "final_news_italian.json"
if (Test-Path $mainFile) {
    Copy-Item $mainFile (Join-Path $rootDir "api\final_news_italian.json") -Force
    Copy-Item $mainFile (Join-Path $rootDir "backend\final_news_italian.json") -Force
    Write-Host "   ✅ File sincronizzati" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  File principale non trovato" -ForegroundColor Yellow
}

# 2. Crea un file di versione per forzare il deploy
Write-Host ""
Write-Host "📝 STEP 2: Creazione file versione..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$versionContent = @{
    version = $timestamp
    deploy_forced = $true
    cache_invalidated = $true
} | ConvertTo-Json

$versionFile = Join-Path $rootDir ".vercel_version.json"
$versionContent | Out-File -FilePath $versionFile -Encoding UTF8
Write-Host "   ✅ File versione creato: $timestamp" -ForegroundColor Green

# 3. Verifica che vercel.json abbia gli header anti-cache
Write-Host ""
Write-Host "🔍 STEP 3: Verifica configurazione Vercel..." -ForegroundColor Yellow
$vercelConfig = Join-Path $rootDir ".github\vercel.json"
if (Test-Path $vercelConfig) {
    $config = Get-Content $vercelConfig -Raw | ConvertFrom-Json
    if ($config.headers) {
        Write-Host "   ✅ Header anti-cache configurati" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Header anti-cache non trovati" -ForegroundColor Yellow
    }
}

# 4. Git commit e push
Write-Host ""
Write-Host "📤 STEP 4: Commit e Push su GitHub..." -ForegroundColor Yellow

Set-Location $rootDir

# Aggiungi tutti i file modificati
git add api/final_news_italian.json backend/final_news_italian.json final_news_italian.json .vercel_version.json -ErrorAction SilentlyContinue

# Commit con messaggio che include timestamp
$commitMessage = "FORCE DEPLOY: Aggiornamento articoli e invalidazione cache - $timestamp"
git commit -m $commitMessage 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Commit creato" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  Nessuna modifica da committare" -ForegroundColor Cyan
    # Forza comunque un commit vuoto per triggerare il deploy
    git commit --allow-empty -m "FORCE DEPLOY: Invalidazione cache CDN - $timestamp" 2>&1 | Out-Null
    Write-Host "   ✅ Commit vuoto creato per forzare deploy" -ForegroundColor Green
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
    Write-Host "✅ Deploy forzato completato!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Prossimi passi:" -ForegroundColor Cyan
    Write-Host "   1. Attendi 2-3 minuti per il deploy su Vercel" -ForegroundColor White
    Write-Host "   2. Controlla lo stato su: https://vercel.com/dashboard" -ForegroundColor White
    Write-Host "   3. Se il dominio personalizzato non si aggiorna:" -ForegroundColor White
    Write-Host "      - Vai su Vercel Dashboard > Domains" -ForegroundColor Gray
    Write-Host "      - Rimuovi e riaggiungi il dominio" -ForegroundColor Gray
    Write-Host "      - Oppure attendi fino a 24h per la propagazione DNS" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 Per invalidare la cache del browser:" -ForegroundColor Yellow
    Write-Host "   - Premi Ctrl+F5 (hard refresh)" -ForegroundColor Gray
    Write-Host "   - Oppure apri in modalità incognito" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "⚠️  Errore durante il push. Verifica la connessione Git." -ForegroundColor Yellow
}

Write-Host ""


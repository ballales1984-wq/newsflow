# Script COMPLETO per aggiornare notizie NewsFlow
# Questo script:
# 1. Completa il merge Git in sospeso
# 2. Aggiorna le notizie (via API o script locale)
# 3. Sincronizza i file JSON in tutte le cartelle
# 4. Fa commit e push su GitHub
# 5. Vercel farà deploy automatico su https://newsflow-orcin.vercel.app/

$ErrorActionPreference = "Continue"
$rootDir = $PSScriptRoot
if (-not $rootDir) {
    $rootDir = Get-Location
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "🔄 AGGIORNAMENTO COMPLETO NOTIZIE NEWSFLOW" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# STEP 1: Completa merge Git in sospeso
Write-Host "📋 STEP 1: Verifica stato Git..." -ForegroundColor Yellow
Set-Location $rootDir

try {
    $gitStatus = git status --porcelain 2>&1
    $isMerging = git status 2>&1 | Select-String "All conflicts fixed but you are still merging"
    
    if ($isMerging) {
        Write-Host "   🔀 Merge in sospeso trovato - completamento..." -ForegroundColor Yellow
        git commit -m "Merge: Completa merge automatico $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-Null
        Write-Host "   ✅ Merge completato" -ForegroundColor Green
    } else {
        Write-Host "   ✅ Nessun merge in sospeso" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠️  Errore verifica Git: $_" -ForegroundColor Yellow
}

Write-Host ""

# STEP 2: Aggiorna notizie ONLINE (Render)
Write-Host "🌐 STEP 2: Aggiornamento notizie ONLINE (Render)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://newsflow-backend-v2.onrender.com/api/admin/collect-news" -Method POST -TimeoutSec 300
    Write-Host "   ✅ ONLINE: $($response.total_articles) notizie aggiornate!" -ForegroundColor Green
    Write-Host "   📝 Messaggio: $($response.message)" -ForegroundColor Gray
    
    # Attendi un po' per il backend processare
    Write-Host "   ⏳ Attesa 10 secondi per elaborazione..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
} catch {
    Write-Host "   ⚠️  Errore aggiornamento online: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   💡 Proseguo con aggiornamento locale..." -ForegroundColor Cyan
}

Write-Host ""

# STEP 3: Aggiorna notizie LOCALI (se script disponibile)
Write-Host "💻 STEP 3: Aggiornamento notizie LOCALI..." -ForegroundColor Yellow
$collectScript = Join-Path $rootDir "backend\collect_italian_priority.py"
if (Test-Path $collectScript) {
    Set-Location (Join-Path $rootDir "backend")
    try {
        Write-Host "   🔄 Esecuzione collect_italian_priority.py..." -ForegroundColor Gray
        python collect_italian_priority.py 2>&1 | ForEach-Object {
            if ($_ -match "✅|🎉|✅") {
                Write-Host "   $_" -ForegroundColor Green
            } elseif ($_ -match "❌|⚠️|ERROR") {
                Write-Host "   $_" -ForegroundColor Red
            } else {
                Write-Host "   $_" -ForegroundColor Gray
            }
        }
        
        # Copia in final_news_italian.json
        if (Test-Path "italian_priority_news.json") {
            Copy-Item "italian_priority_news.json" "final_news_italian.json" -Force
            Copy-Item "italian_priority_news.json" "all_sources_news.json" -Force
            Write-Host "   ✅ File JSON locali aggiornati" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ⚠️  Errore aggiornamento locale: $_" -ForegroundColor Yellow
    }
    Set-Location $rootDir
} else {
    Write-Host "   ℹ️  Script di raccolta locale non trovato - salto" -ForegroundColor Cyan
}

Write-Host ""

# STEP 4: Sincronizza file JSON in tutte le cartelle
Write-Host "📁 STEP 4: Sincronizzazione file JSON..." -ForegroundColor Yellow

# Trova il file più recente tra backend, api e root
$backendFile = Join-Path $rootDir "backend\final_news_italian.json"
$apiFile = Join-Path $rootDir "api\final_news_italian.json"
$rootFile = Join-Path $rootDir "final_news_italian.json"

$mostRecentFile = $null
$mostRecentTime = [DateTime]::MinValue

foreach ($file in @($backendFile, $apiFile, $rootFile)) {
    if (Test-Path $file) {
        $fileTime = (Get-Item $file).LastWriteTime
        if ($fileTime -gt $mostRecentTime) {
            $mostRecentTime = $fileTime
            $mostRecentFile = $file
        }
    }
}

if ($mostRecentFile) {
    Write-Host "   📄 File più recente: $mostRecentFile" -ForegroundColor Gray
    Write-Host "   🕐 Timestamp: $mostRecentTime" -ForegroundColor Gray
    
    # Copia in tutte le cartelle necessarie
    $targets = @(
        $backendFile,
        $apiFile,
        $rootFile,
        (Join-Path $rootDir "frontend\src\assets\final_news_italian.json")
    )
    
    foreach ($target in $targets) {
        $targetDir = Split-Path $target -Parent
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        Copy-Item $mostRecentFile $target -Force
        Write-Host "   ✅ Copiato: $target" -ForegroundColor Green
    }
    
    # Verifica conteggio articoli
    try {
        $jsonContent = Get-Content $mostRecentFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $articleCount = if ($jsonContent.items) { $jsonContent.items.Count } elseif ($jsonContent.articles) { $jsonContent.articles.Count } else { 0 }
        Write-Host "   📊 Articoli totali: $articleCount" -ForegroundColor Cyan
    } catch {
        Write-Host "   ⚠️  Impossibile verificare conteggio articoli" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ Nessun file final_news_italian.json trovato!" -ForegroundColor Red
    Write-Host "   💡 Esegui prima lo script di raccolta notizie" -ForegroundColor Yellow
}

Write-Host ""

# STEP 5: Git add, commit e push
Write-Host "📤 STEP 5: Commit e Push su GitHub..." -ForegroundColor Yellow

Set-Location $rootDir

if (-not (Test-Path ".git")) {
    Write-Host "   ❌ Directory non è una repository Git!" -ForegroundColor Red
    Write-Host "   💡 Esegui 'git init' prima di continuare" -ForegroundColor Yellow
    exit 1
}

# Aggiungi tutti i file JSON modificati
$filesToAdd = @(
    "final_news_italian.json",
    "api/final_news_italian.json",
    "backend/final_news_italian.json",
    "backend/all_sources_news.json",
    "backend/italian_priority_news.json",
    "frontend/src/assets/final_news_italian.json"
)

$hasChanges = $false
foreach ($file in $filesToAdd) {
    $filePath = Join-Path $rootDir $file
    if (Test-Path $filePath) {
        git add $file 2>&1 | Out-Null
        $hasChanges = $true
    }
}

if ($hasChanges) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMessage = "🤖 Auto-update: Aggiornate notizie - $timestamp"
    
    git commit -m $commitMessage 2>&1 | ForEach-Object {
        if ($_ -match "nothing to commit") {
            Write-Host "   ℹ️  Nessuna modifica da committare" -ForegroundColor Cyan
        } else {
            Write-Host "   $_" -ForegroundColor Gray
        }
    }
    
    Write-Host "   ✅ Commit creato: $commitMessage" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  Nessun file da committare" -ForegroundColor Cyan
}

# Push su GitHub
Write-Host ""
Write-Host "   📤 Push su GitHub..." -ForegroundColor Yellow
try {
    git push 2>&1 | ForEach-Object {
        if ($_ -match "error|fatal|rejected") {
            Write-Host "   ❌ $_" -ForegroundColor Red
        } elseif ($_ -match "Already up to date") {
            Write-Host "   ℹ️  Repository già aggiornato" -ForegroundColor Cyan
        } else {
            Write-Host "   $_" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    Write-Host "✅ Push completato!" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Errore durante push: $_" -ForegroundColor Yellow
    Write-Host "   💡 Prova manualmente: git push" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "✅ AGGIORNAMENTO COMPLETATO!" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Prossimi passi:" -ForegroundColor Cyan
Write-Host "   1. ⏳ Attendi 2-3 minuti per deploy automatico su Vercel" -ForegroundColor White
Write-Host "   2. 🌐 Controlla lo stato su: https://vercel.com/dashboard" -ForegroundColor White
Write-Host "   3. 🔍 Verifica l'app: https://newsflow-orcin.vercel.app/" -ForegroundColor White
Write-Host ""
Write-Host "💡 Per invalidare la cache del browser:" -ForegroundColor Yellow
Write-Host "   - Premi Ctrl+F5 (hard refresh)" -ForegroundColor Gray
Write-Host "   - Oppure apri in modalità incognito" -ForegroundColor Gray
Write-Host ""




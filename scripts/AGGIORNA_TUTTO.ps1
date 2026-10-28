# Script COMPLETO per aggiornare notizie, digest e deploy
# Esegue tutto in un'unica operazione: raccolta -> digest -> commit -> push

$ErrorActionPreference = "Continue"
$rootDir = $PSScriptRoot
if (-not $rootDir) {
    $rootDir = Get-Location
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "🔄 AGGIORNAMENTO COMPLETO NEWSFLOW" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

Set-Location $rootDir

# STEP 0: Cancella file JSON vecchi
Write-Host "🗑️  STEP 0: Cancellazione file JSON vecchi..." -ForegroundColor Yellow
$filesToDelete = @(
    "backend\italian_priority_news.json",
    "backend\final_news_italian.json",
    "backend\all_sources_news.json",
    "api\final_news_italian.json",
    "final_news_italian.json",
    "frontend\src\assets\final_news_italian.json"
)

$deletedCount = 0
foreach ($file in $filesToDelete) {
    $filePath = Join-Path $rootDir $file
    if (Test-Path $filePath) {
        try {
            Remove-Item $filePath -Force
            Write-Host "   ✅ Cancellato: $file" -ForegroundColor Green
            $deletedCount++
        } catch {
            Write-Host "   ⚠️  Errore cancellazione $file : $_" -ForegroundColor Yellow
        }
    }
}

if ($deletedCount -gt 0) {
    Write-Host "   📊 $deletedCount file vecchi cancellati" -ForegroundColor Cyan
} else {
    Write-Host "   ℹ️  Nessun file vecchio da cancellare" -ForegroundColor Gray
}

Write-Host ""

# STEP 1: Raccolta notizie
Write-Host "📰 STEP 1: Raccolta notizie..." -ForegroundColor Yellow
$collectScript = Join-Path $rootDir "backend\collect_italian_priority.py"
if (Test-Path $collectScript) {
    Set-Location (Join-Path $rootDir "backend")
    try {
        Write-Host "   🔄 Esecuzione collect_italian_priority.py..." -ForegroundColor Gray
        $output = python collect_italian_priority.py 2>&1
        $output | ForEach-Object {
            if ($_ -match "✅|🎉|TOTALE") {
                Write-Host "   $_" -ForegroundColor Green
            } elseif ($_ -match "❌|⚠️|ERROR") {
                Write-Host "   $_" -ForegroundColor Red
            } else {
                Write-Host "   $_" -ForegroundColor Gray
            }
        }
        
        # Copia file JSON
        if (Test-Path "italian_priority_news.json") {
            Copy-Item "italian_priority_news.json" "final_news_italian.json" -Force
            Copy-Item "italian_priority_news.json" "all_sources_news.json" -Force
            Write-Host "   ✅ File JSON backend aggiornati" -ForegroundColor Green
        }
    } catch {
        Write-Host "   ⚠️  Errore raccolta: $_" -ForegroundColor Yellow
    }
    Set-Location $rootDir
} else {
    Write-Host "   ❌ Script di raccolta non trovato!" -ForegroundColor Red
}

Write-Host ""

# STEP 2: Sincronizza file JSON
Write-Host "📁 STEP 2: Sincronizzazione file JSON..." -ForegroundColor Yellow
$backendFile = Join-Path $rootDir "backend\final_news_italian.json"
if (Test-Path $backendFile) {
    $targets = @(
        (Join-Path $rootDir "api\final_news_italian.json"),
        (Join-Path $rootDir "final_news_italian.json"),
        (Join-Path $rootDir "frontend\src\assets\final_news_italian.json")
    )
    
    foreach ($target in $targets) {
        $targetDir = Split-Path $target -Parent
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }
        Copy-Item $backendFile $target -Force
        Write-Host "   ✅ Copiato: $target" -ForegroundColor Green
    }
    
    # Verifica conteggio
    try {
        $jsonContent = Get-Content $backendFile -Raw -Encoding UTF8 | ConvertFrom-Json
        $articleCount = if ($jsonContent.items) { $jsonContent.items.Count } else { 0 }
        Write-Host "   📊 Articoli totali: $articleCount" -ForegroundColor Cyan
    } catch {
        Write-Host "   ⚠️  Impossibile verificare conteggio" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ File JSON non trovato!" -ForegroundColor Red
}

Write-Host ""

# STEP 3: Genera digest
Write-Host "📰 STEP 3: Generazione digest giornaliero..." -ForegroundColor Yellow
$digestScript = Join-Path $rootDir "backend\genera_digest_giornaliero.py"
if (Test-Path $digestScript) {
    Set-Location (Join-Path $rootDir "backend")
    try {
        Write-Host "   🔄 Esecuzione genera_digest_giornaliero.py..." -ForegroundColor Gray
        $output = python genera_digest_giornaliero.py 2>&1
        $output | ForEach-Object {
            if ($_ -match "✅|Digest") {
                Write-Host "   $_" -ForegroundColor Green
            } elseif ($_ -match "❌|⚠️|ERROR") {
                Write-Host "   $_" -ForegroundColor Red
            } else {
                Write-Host "   $_" -ForegroundColor Gray
            }
        }
        
        # Sincronizza digest.json in tutte le cartelle necessarie
        $digestFile = Join-Path $rootDir "backend\digest.json"
        if (Test-Path $digestFile) {
            $digestTargets = @(
                (Join-Path $rootDir "api\digest.json"),
                (Join-Path $rootDir "frontend\src\assets\digest.json")
            )
            
            foreach ($target in $digestTargets) {
                $targetDir = Split-Path $target -Parent
                if (-not (Test-Path $targetDir)) {
                    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                }
                Copy-Item $digestFile $target -Force
                Write-Host "   ✅ Digest sincronizzato: $target" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "   ⚠️  Errore generazione digest: $_" -ForegroundColor Yellow
    }
    Set-Location $rootDir
} else {
    Write-Host "   ⚠️  Script digest non trovato - salto" -ForegroundColor Yellow
}

Write-Host ""

# STEP 4: Git commit e push
Write-Host "📤 STEP 4: Commit e Push su GitHub..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    Write-Host "   ⚠️  Directory non è una repository Git - salto" -ForegroundColor Yellow
} else {
    # Completa merge se necessario
    try {
        $isMerging = git status 2>&1 | Select-String "All conflicts fixed but you are still merging"
        if ($isMerging) {
            Write-Host "   🔀 Completamento merge..." -ForegroundColor Yellow
            git commit -m "Merge: Completa merge automatico $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-Null
        }
    } catch {
        # Ignora errori
    }
    
    # Aggiungi file
    $filesToAdd = @(
        "final_news_italian.json",
        "api/final_news_italian.json",
        "backend/final_news_italian.json",
        "backend/all_sources_news.json",
        "backend/italian_priority_news.json",
        "frontend/src/assets/final_news_italian.json",
        "api/digest.json",
        "backend/digest.json",
        "frontend/src/assets/digest.json"
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
        $commitMessage = "🤖 Auto-update: Aggiornate notizie e digest - $timestamp"
        
        git commit -m $commitMessage 2>&1 | ForEach-Object {
            if ($_ -match "nothing to commit") {
                Write-Host "   ℹ️  Nessuna modifica da committare" -ForegroundColor Cyan
            } else {
                Write-Host "   $_" -ForegroundColor Gray
            }
        }
        
        Write-Host "   ✅ Commit creato" -ForegroundColor Green
        
        # Pull prima di push
        Write-Host "   📥 Pull da GitHub..." -ForegroundColor Yellow
        try {
            git pull --rebase 2>&1 | Out-Null
            Write-Host "   ✅ Pull completato" -ForegroundColor Green
        } catch {
            Write-Host "   ⚠️  Errore pull: $_" -ForegroundColor Yellow
        }
        
        # Push
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
            Write-Host "   ✅ Push completato!" -ForegroundColor Green
        } catch {
            Write-Host "   ⚠️  Errore push: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ℹ️  Nessun file da committare" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "✅ AGGIORNAMENTO COMPLETATO!" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Prossimi passi:" -ForegroundColor Cyan
Write-Host "   1. ⏳ Attendi 2-3 minuti per deploy automatico su Vercel" -ForegroundColor White
Write-Host "   2. 🌐 Verifica: https://newsflow-orcin.vercel.app/" -ForegroundColor White
Write-Host ""


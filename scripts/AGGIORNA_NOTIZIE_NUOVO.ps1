# Script per aggiornare le notizie - Versione Corretta
# Esegue: raccolta notizie, generazione digest, sincronizzazione file

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "AGGIORNAMENTO NOTIZIE NEWSFLOW" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""

# Definiamo le funzioni
function Write-Log {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

# ============================================
# STEP 1: Raccolta notizie
# ============================================
Write-Log "========================================" "Cyan"
Write-Log "STEP 1: Raccolta notizie da RSS" "Yellow"
Write-Log "========================================" "Cyan"

$collectResult = & python -X utf8 "c:/Users/user/news/backend/collect_news_now.py" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Log "[OK] Notizie raccolte con successo" "Green"
} else {
    Write-Log "[ERRORE] Raccolta notizie fallita" "Red"
    Write-Log $collectResult "Red"
}

# ============================================
# STEP 2: Generazione digest
# ============================================
Write-Log ""
Write-Log "========================================" "Cyan"
Write-Log "STEP 2: Generazione digest giornaliero" "Yellow"
Write-Log "========================================" "Cyan"

$digestResult = & python -X utf8 "c:/Users/user/news/backend/genera_digest_ora.py" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Log "[OK] Digest generato con successo" "Green"
} else {
    Write-Log "[ERRORE] Generazione digest fallita" "Red"
    Write-Log $digestResult "Red"
}

# ============================================
# STEP 3: Sincronizzazione file JSON
# ============================================
Write-Log ""
Write-Log "========================================" "Cyan"
Write-Log "STEP 3: Sincronizzazione file JSON" "Yellow"
Write-Log "========================================" "Cyan"

$backendDir = "c:/Users/user/news/backend"
$apiDir = "c:/Users/user/news/api"
$frontendDir = "c:/Users/user/news/frontend/src/assets"

$filesToSync = @("notizie_vere.json", "final_news_italian.json", "digest.json")

foreach ($file in $filesToSync) {
    $sourcePath = Join-Path $backendDir $file

    # Copia in api/
    $apiPath = Join-Path $apiDir $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $apiPath -Force
        Write-Log "[OK] Copiato $file -> api/" "Green"
    } else {
        Write-Log "[WARN] File non trovato: $sourcePath" "Yellow"
    }

    # Copia in frontend/src/assets/
    $frontendPath = Join-Path $frontendDir $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $frontendPath -Force
        Write-Log "[OK] Copiato $file -> frontend/src/assets/" "Green"
    }
}

# ============================================
# COMPLETATO
# ============================================
Write-Log ""
Write-Log "========================================" "Cyan"
Write-Log "AGGIORNAMENTO COMPLETATO!" "Green"
Write-Log "========================================" "Cyan"
Write-Log ""
Write-Log "Prossimi passi:" "Yellow"
Write-Log "1. Commit e push su GitHub (opzionale)" "White"
Write-Log "2. Deploy automatico Vercel (2-3 min)" "White"
Write-Log ""


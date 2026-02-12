# Script per forzare l'aggiornamento delle notizie su NewsFlow
Write-Host "🚀 Inizio procedura di aggiornamento NewsFlow..." -ForegroundColor Cyan

# Determina la directory corrente (gestisce sia esecuzione file che copia-incolla)
$scriptDir = $PSScriptRoot
if (-not $scriptDir) {
    $scriptDir = (Get-Location).Path
}

# 1. Vai alla cartella backend
$backendDir = Join-Path $scriptDir "backend"
if (-not (Test-Path $backendDir)) {
    Write-Host "❌ Errore: Cartella backend non trovata in $backendDir" -ForegroundColor Red
    exit 1
}
Set-Location $backendDir

# 2. Esegui lo script Python per raccogliere le news
Write-Host "📥 Raccolta nuove notizie in corso (attendere)..." -ForegroundColor Yellow
try {
    # Esegue la funzione di raccolta notizie del backend
    python -c "from app.services.tasks import collect_all_news; collect_all_news()"
    Write-Host "✅ Notizie raccolte e salvate nei file JSON." -ForegroundColor Green
} catch {
    Write-Host "❌ Errore durante la raccolta notizie. Verifica che il backend funzioni." -ForegroundColor Red
    Write-Host "   Dettaglio errore: $_" -ForegroundColor Gray
    exit 1
}

# 3. Torna alla root e fai Git Push per scatenare il deploy di Vercel
Set-Location $scriptDir
Write-Host "☁️  Sincronizzazione con GitHub e Vercel..." -ForegroundColor Yellow

if (Test-Path ".git") {
    $status = git status --porcelain
    if ($status) {
        git add .
        git commit -m "Aggiornamento notizie: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

        # Gestione Push con Auto-Fix (Pull se necessario)
        git push
        Write-Host "✅ Modifiche inviate! Vercel aggiornerà il sito tra circa 2 minuti." -ForegroundColor Green
        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️  Rilevate modifiche remote. Eseguo 'git pull --rebase'..." -ForegroundColor Yellow
            git pull --rebase
            git push
        }

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Modifiche inviate! Vercel aggiornerà il sito tra circa 2 minuti." -ForegroundColor Green
        } else {
            Write-Host "❌ Errore critico: Impossibile sincronizzare con GitHub." -ForegroundColor Red
        }
    } else {
        Write-Host "⚠️  Nessuna nuova notizia trovata (i file non sono cambiati)." -ForegroundColor Gray
    }
} else {
    Write-Host "❌ ATTENZIONE: Non sei in un repository Git." -ForegroundColor Red
    Write-Host "   Le notizie sono state aggiornate in locale, ma non possono essere inviate a Vercel." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Procedura completata." -ForegroundColor Cyan
Start-Sleep -Seconds 5

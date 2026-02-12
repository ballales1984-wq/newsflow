# Script per forzare l'aggiornamento delle notizie su NewsFlow
Write-Host "🚀 Inizio procedura di aggiornamento NewsFlow..." -ForegroundColor Cyan

# 1. Vai alla cartella backend
$backendDir = Join-Path $PSScriptRoot "backend"
Set-Location $backendDir

# 2. Esegui lo script Python per raccogliere le news
Write-Host "📥 Raccolta nuove notizie in corso (attendere)..." -ForegroundColor Yellow
try {
    # Esegue la funzione di raccolta notizie del backend
    python -c "from app.services.tasks import collect_all_news; collect_all_news()"
    Write-Host "✅ Notizie raccolte e salvate nei file JSON." -ForegroundColor Green
} catch {
    Write-Host "❌ Errore durante la raccolta notizie. Verifica che il backend funzioni." -ForegroundColor Red
    exit 1
}

# 3. Torna alla root e fai Git Push per scatenare il deploy di Vercel
Set-Location $PSScriptRoot
Write-Host "☁️  Sincronizzazione con GitHub e Vercel..." -ForegroundColor Yellow

$status = git status --porcelain
if ($status) {
    git add .
    git commit -m "Aggiornamento notizie: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push
    Write-Host "✅ Modifiche inviate! Vercel aggiornerà il sito tra circa 2 minuti." -ForegroundColor Green
} else {
    Write-Host "⚠️  Nessuna nuova notizia trovata (i file non sono cambiati)." -ForegroundColor Gray
}

Write-Host ""
Write-Host "🎉 Procedura completata." -ForegroundColor Cyan
Start-Sleep -Seconds 5

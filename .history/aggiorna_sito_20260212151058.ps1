Write-Host "📥 Raccolta nuove notizie in corso (attendere)..." -ForegroundColor Yellow
try {
    # Esegue la funzione di raccolta notizie del backend
    # Nasconde l'output di errore di Python per gestirlo in modo pulito
    python -c "from app.services.tasks import collect_all_news; collect_all_news()" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        # Forza un errore per attivare il blocco catch
        throw "Lo script Python ha fallito. Probabile dipendenza mancante."
    }
    Write-Host "✅ Notizie raccolte e salvate nei file JSON." -ForegroundColor Green
} catch {
    Write-Host "❌ Errore durante la raccolta notizie. Verifica che il backend funzioni." -ForegroundColor Red
    Write-Host "   Dettaglio errore: $_" -ForegroundColor Gray
    Write-Host "   💡 PROVA QUESTO COMANDO per risolvere: pip install -r backend/requirements.txt" -ForegroundColor Cyan
    exit 1
}

# 3. Torna alla root e fai Git Push per scatenare il deploy di Vercel


    if ($status) {
        git add .
        git commit -m "Aggiornamento notizie: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

        # Gestione Push con Auto-Fix (Pull se necessario)
        git push
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

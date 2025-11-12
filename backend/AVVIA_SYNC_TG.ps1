# Script per sincronizzazione automatica del TG 4 ore
# Monitora le notizie e rigenera il video quando vengono aggiornate
# Mantieni questo script ATTIVO per avere il TG sempre aggiornato

Write-Host "🔄 SINCRONIZZAZIONE AUTOMATICA TG 4 ORE" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   - Questo script deve rimanere ATTIVO" -ForegroundColor White
Write-Host "   - Controlla ogni 5 minuti se le notizie sono state aggiornate" -ForegroundColor White
Write-Host "   - Rigenera automaticamente il video TG quando ci sono nuove notizie" -ForegroundColor White
Write-Host "   - Non chiudere questa finestra!" -ForegroundColor White
Write-Host "   - Il backend deve essere attivo su http://localhost:8000" -ForegroundColor White
Write-Host ""

# Verifica che il backend sia attivo
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 3
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend non attivo!" -ForegroundColor Red
    Write-Host "   Avvia il backend prima di eseguire lo script" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "📊 CONFIGURAZIONE:" -ForegroundColor Cyan
Write-Host "   - Durata TG: 4 ore (240 minuti)" -ForegroundColor White
Write-Host "   - Notizie disponibili: 85" -ForegroundColor White
Write-Host "   - Intervallo controllo: 5 minuti" -ForegroundColor White
Write-Host "   - Video: backend/youtube_videos/newsflow_live_4h.mp4" -ForegroundColor White
Write-Host ""

# Crea il video iniziale se non esiste
Write-Host "🔍 Controllo se il video TG esiste..." -ForegroundColor Yellow
try {
    $syncCheck = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/check-tg-sync" -TimeoutSec 10
    
    if (-not $syncCheck.video_exists -or $syncCheck.should_regenerate) {
        Write-Host "📹 Creo il video TG iniziale (4 ore)..." -ForegroundColor Yellow
        Write-Host "   ⏳ Questo richiederà molto tempo (30-60 minuti)..." -ForegroundColor Gray
        Write-Host "   ⚠️  NON CHIUDERE QUESTA FINESTRA!" -ForegroundColor Red
        Write-Host ""
        
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-tg-4h-video" -Method POST -TimeoutSec 7200
        
        if ($response.success) {
            Write-Host ""
            Write-Host "✅ Video TG creato con successo!" -ForegroundColor Green
            Write-Host "   Durata: $($response.duration_minutes) minuti" -ForegroundColor White
            Write-Host "   Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
            Write-Host "   File: $($response.video_path)" -ForegroundColor White
        } else {
            Write-Host "❌ Errore creazione video: $($response.error)" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✅ Video TG già esistente e aggiornato!" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Errore controllo sincronizzazione: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔄 Avvio monitoraggio continuo..." -ForegroundColor Green
Write-Host "   (Premi Ctrl+C per fermare)" -ForegroundColor Gray
Write-Host ""

$checkInterval = 300  # 5 minuti in secondi
$lastCheck = Get-Date

while ($true) {
    try {
        $now = Get-Date
        $elapsed = ($now - $lastCheck).TotalSeconds
        
        if ($elapsed -ge $checkInterval) {
            Write-Host "[$($now.ToString('HH:mm:ss'))] Controllo aggiornamenti notizie..." -ForegroundColor Cyan
            
            $syncCheck = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/check-tg-sync" -TimeoutSec 10
            
            if ($syncCheck.should_regenerate) {
                Write-Host "   ⚠️  Notizie aggiornate! Rigenero il video TG..." -ForegroundColor Yellow
                Write-Host "   ⏳ Questo richiederà molto tempo (30-60 minuti)..." -ForegroundColor Gray
                Write-Host "   ⚠️  NON CHIUDERE QUESTA FINESTRA!" -ForegroundColor Red
                
                $response = Invoke-RestMethod -Uri "http://localhost:8000/api/admin/create-tg-4h-video" -Method POST -TimeoutSec 7200
                
                if ($response.success) {
                    Write-Host "   ✅ Video TG rigenerato con successo!" -ForegroundColor Green
                    Write-Host "      Durata: $($response.duration_minutes) minuti" -ForegroundColor White
                    Write-Host "      Dimensione: $($response.file_size_mb) MB" -ForegroundColor White
                    Write-Host "      File: $($response.video_path)" -ForegroundColor White
                } else {
                    Write-Host "   ❌ Errore rigenerazione: $($response.error)" -ForegroundColor Red
                }
            } else {
                Write-Host "   ✅ Video TG aggiornato (nessuna modifica alle notizie)" -ForegroundColor Green
            }
            
            $lastCheck = $now
        }
        
        # Attendi 30 secondi prima del prossimo controllo
        Start-Sleep -Seconds 30
        
    } catch {
        Write-Host "[$($now.ToString('HH:mm:ss'))] ⚠️  Errore controllo: $($_.Exception.Message)" -ForegroundColor Yellow
        Start-Sleep -Seconds 60  # Attendi 1 minuto in caso di errore
    }
}


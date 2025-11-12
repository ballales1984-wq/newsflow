# GUIDA: Configurazione YouTube Live per TG 4 Ore
# Segui questi passaggi per configurare la live streaming su YouTube

Write-Host "📺 GUIDA CONFIGURAZIONE YOUTUBE LIVE" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎬 PASSAGGI PER CONFIGURARE LA LIVE:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1️⃣  ACCEDI A YOUTUBE STUDIO" -ForegroundColor Cyan
Write-Host "   - Vai su: https://studio.youtube.com" -ForegroundColor White
Write-Host "   - Accedi con il tuo account Google" -ForegroundColor White
Write-Host "   - Seleziona il canale: UC9rdnY48FU0kzzGfMJ2wHaQ" -ForegroundColor White
Write-Host ""

Write-Host "2️⃣  CREA NUOVA TRASMISSIONE LIVE" -ForegroundColor Cyan
Write-Host "   - Nel menu a sinistra, clicca su 'Trasmissioni' (Live)" -ForegroundColor White
Write-Host "   - Clicca su 'Nuova trasmissione' o 'Crea'" -ForegroundColor White
Write-Host "   - Oppure vai direttamente a:" -ForegroundColor White
Write-Host "     https://studio.youtube.com/channel/UC9rdnY48FU0kzzGfMJ2wHaQ/livestreaming/stream" -ForegroundColor Gray
Write-Host ""

Write-Host "3️⃣  CONFIGURA LA TRASMISSIONE" -ForegroundColor Cyan
Write-Host "   Titolo: TG NewsFlow - Notizie in Diretta 24/7" -ForegroundColor White
Write-Host "   Descrizione: Telegiornale automatico con le ultime notizie." -ForegroundColor White
Write-Host "                Aggiornato automaticamente ogni 4 ore." -ForegroundColor White
Write-Host "   Privacy: Pubblico (o Non in elenco)" -ForegroundColor White
Write-Host "   Categoria: Notizie e politica" -ForegroundColor White
Write-Host ""

Write-Host "4️⃣  SCEGLI LA FONTE DI TRASMISSIONE" -ForegroundColor Cyan
Write-Host "   - Seleziona 'Trasmetti da file' o 'Streaming da file'" -ForegroundColor White
Write-Host "   - Clicca su 'Scegli file' o 'Carica file'" -ForegroundColor White
Write-Host "   - Seleziona il video: backend\youtube_videos\newsflow_live_4h.mp4" -ForegroundColor White
Write-Host "   - ⚠️  Il file è grande, il caricamento richiederà tempo!" -ForegroundColor Yellow
Write-Host ""

Write-Host "5️⃣  IMPOSTAZIONI AVANZATE (OPZIONALE)" -ForegroundColor Cyan
Write-Host "   - Abilita 'Chat live' se vuoi i commenti" -ForegroundColor White
Write-Host "   - Configura 'Streaming continuo' se disponibile" -ForegroundColor White
Write-Host "   - Imposta 'Ripeti video' per loop continuo" -ForegroundColor White
Write-Host ""

Write-Host "6️⃣  AVVIA LA LIVE" -ForegroundColor Cyan
Write-Host "   - Clicca su 'Avvia trasmissione' o 'Go Live'" -ForegroundColor White
Write-Host "   - La live partirà automaticamente!" -ForegroundColor White
Write-Host ""

Write-Host "💡 SUGGERIMENTI:" -ForegroundColor Yellow
Write-Host "   - Il video dura 4 ore, quindi si ripeterà automaticamente" -ForegroundColor White
Write-Host "   - Per avere contenuto sempre nuovo, avvia AVVIA_SYNC_TG.ps1" -ForegroundColor White
Write-Host "   - Il sistema rigenererà il video quando le notizie vengono aggiornate" -ForegroundColor White
Write-Host "   - Carica il nuovo video quando è pronto" -ForegroundColor White
Write-Host ""

Write-Host "🔄 AUTOMATIZZAZIONE:" -ForegroundColor Cyan
Write-Host "   Per automatizzare completamente:" -ForegroundColor White
Write-Host "   1. Crea il video: .\CREA_TG_4H.ps1" -ForegroundColor Gray
Write-Host "   2. Avvia sincronizzazione: .\AVVIA_SYNC_TG.ps1" -ForegroundColor Gray
Write-Host "   3. Quando il video viene rigenerato, caricalo manualmente su YouTube" -ForegroundColor Gray
Write-Host "   4. Oppure configura YouTube API per upload automatico (richiede setup OAuth)" -ForegroundColor Gray
Write-Host ""

Write-Host "📁 PERCORSO VIDEO:" -ForegroundColor Cyan
$videoPath = Join-Path $PSScriptRoot "backend\youtube_videos\newsflow_live_4h.mp4"
if (Test-Path $videoPath) {
    $fileSize = [math]::Round((Get-Item $videoPath).Length / 1MB, 2)
    Write-Host "   ✅ Video trovato: $videoPath" -ForegroundColor Green
    Write-Host "   Dimensione: $fileSize MB" -ForegroundColor White
} else {
    Write-Host "   ⚠️  Video non trovato!" -ForegroundColor Yellow
    Write-Host "   Esegui prima: .\CREA_TG_4H.ps1" -ForegroundColor White
}

Write-Host ""
Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


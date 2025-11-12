# GUIDA RAPIDA: YouTube Live Setup
# Sistema con caricamento manuale (più semplice)

Write-Host "📺 GUIDA YOUTUBE LIVE - CARICAMENTO MANUALE" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ COSA HAI GIÀ:" -ForegroundColor Green
Write-Host "   - Canale YouTube: UC9rdnY48FU0kzzGfMJ2wHaQ" -ForegroundColor White
Write-Host "   - URL Studio: https://studio.youtube.com/channel/UC9rdnY48FU0kzzGfMJ2wHaQ" -ForegroundColor White
Write-Host ""

Write-Host "📋 PASSAGGI:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1️⃣  CREA IL VIDEO TG" -ForegroundColor Cyan
Write-Host "   Esegui: .\CONFIGURA_SISTEMA_OTTIMALE.ps1" -ForegroundColor White
Write-Host "   Oppure: .\CREA_TG_VELOCE.ps1" -ForegroundColor Gray
Write-Host "   Il video sarà in: backend\youtube_videos\newsflow_tg.mp4" -ForegroundColor Gray
Write-Host ""

Write-Host "2️⃣  CARICA SU YOUTUBE STUDIO" -ForegroundColor Cyan
Write-Host "   - Vai su: https://studio.youtube.com/channel/UC9rdnY48FU0kzzGfMJ2wHaQ/livestreaming/stream" -ForegroundColor White
Write-Host "   - Clicca 'Nuova trasmissione'" -ForegroundColor White
Write-Host "   - Titolo: 'TG NewsFlow - Notizie in Diretta'" -ForegroundColor White
Write-Host "   - Scegli 'Trasmetti da file'" -ForegroundColor White
Write-Host "   - Carica: backend\youtube_videos\newsflow_tg.mp4" -ForegroundColor White
Write-Host ""

Write-Host "3️⃣  PROGRAMMA LE LIVE" -ForegroundColor Cyan
Write-Host "   Esegui: .\PROGRAMMA_LIVE_MULTIPLE.ps1" -ForegroundColor White
Write-Host "   Oppure usa la programmazione già configurata:" -ForegroundColor Gray
Write-Host "   - 8 live al giorno: 6:00, 9:00, 12:00, 15:00, 18:00, 21:00, 0:00, 3:00" -ForegroundColor Gray
Write-Host ""

Write-Host "4️⃣  AVVIA LIVE MANUALMENTE" -ForegroundColor Cyan
Write-Host "   - Alle ore programmate, vai su YouTube Studio" -ForegroundColor White
Write-Host "   - Clicca 'Avvia trasmissione' sulla live configurata" -ForegroundColor White
Write-Host "   - La live durerà ~20 minuti e si spegnerà automaticamente" -ForegroundColor White
Write-Host ""

Write-Host "💡 SUGGERIMENTI:" -ForegroundColor Yellow
Write-Host "   - Puoi creare più live programmate in anticipo" -ForegroundColor White
Write-Host "   - Ogni live usa lo stesso video (newsflow_tg.mp4)" -ForegroundColor White
Write-Host "   - Quando aggiorni le notizie, rigenera il video: .\CREA_TG_VELOCE.ps1" -ForegroundColor White
Write-Host "   - Poi ricarica il nuovo video su YouTube" -ForegroundColor White
Write-Host ""

Write-Host "🎯 NON SERVE NULL'ALTRO!" -ForegroundColor Green
Write-Host "   Il sistema funziona così, semplice e efficace!" -ForegroundColor White
Write-Host ""

Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


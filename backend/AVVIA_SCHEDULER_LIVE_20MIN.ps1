# Script per avviare scheduler live YouTube ogni 20 minuti
# Crea video corti automaticamente e programma live

Write-Host "🔄 AVVIO SCHEDULER LIVE OGNI 20 MINUTI" -ForegroundColor Cyan
Write-Host ""

# Verifica che il backend sia attivo
Write-Host "📡 Verifico backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -TimeoutSec 3
    Write-Host "✅ Backend attivo!" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend non attivo!" -ForegroundColor Red
    Write-Host "   Avvia il backend prima di avviare lo scheduler" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Premi un tasto per chiudere..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "📊 SCHEDULER CONFIGURATO:" -ForegroundColor Cyan
Write-Host "   - Video corti da 2 minuti" -ForegroundColor White
Write-Host "   - Live ogni 20 minuti" -ForegroundColor White
Write-Host "   - Solo notizie con immagini" -ForegroundColor White
Write-Host "   - Voce narrante femminile" -ForegroundColor White
Write-Host ""
Write-Host "⏳ Avvio scheduler..." -ForegroundColor Yellow
Write-Host "   Lo scheduler creerà video automaticamente ogni 20 minuti" -ForegroundColor Gray
Write-Host "   Premi Ctrl+C per fermare" -ForegroundColor Gray
Write-Host ""

# Avvia scheduler Python
cd backend
python -c "
import schedule
import time
import requests
from datetime import datetime
import os
import sys

def create_short_video():
    try:
        print(f'🎬 Creo video corto alle {datetime.now().strftime(\"%H:%M\")}...')
        response = requests.post('http://localhost:8000/api/admin/create-youtube-short-video', timeout=1800)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f'✅ Video creato: {data.get(\"video_path\")}')
                print(f'   Durata: {data.get(\"duration_minutes\")} minuti')
            else:
                print(f'❌ Errore: {data.get(\"error\")}')
        else:
            print(f'❌ Errore HTTP: {response.status_code}')
    except Exception as e:
        print(f'❌ Errore: {e}')

# Programma ogni 20 minuti
for hour in range(24):
    for minute in [0, 20, 40]:
        schedule.every().day.at(f'{hour:02d}:{minute:02d}').do(create_short_video)

print('✅ Scheduler avviato! Video ogni 20 minuti')
print(f'   Totale: 72 video al giorno')
print('   Premi Ctrl+C per fermare')
print('')

while True:
    schedule.run_pending()
    time.sleep(60)
"


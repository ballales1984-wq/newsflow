# 🌐 Status Ngrok Tunnel

## ✅ Ngrok Attivo

**URL Pubblico:** `https://tonita-deposable-manneristically.ngrok-free.dev`

**Backend Locale:** `http://localhost:8000`

**Dashboard Ngrok:** `http://localhost:4040`

---

## 📋 Informazioni

- **Stato:** ✅ Attivo
- **Porta Locale:** 8000
- **Tipo:** HTTP Tunnel
- **Provider:** ngrok-free.dev

---

## 🔧 Comandi Utili

### Riavviare Ngrok
```powershell
.\riavvia_ngrok.ps1
```

### Verificare Status
```powershell
# Apri dashboard
Start-Process "http://localhost:4040"

# Oppure via API
Invoke-WebRequest "http://localhost:4040/api/tunnels" | ConvertFrom-Json
```

### Fermare Ngrok
```powershell
Get-Process | Where-Object {$_.ProcessName -eq "ngrok"} | Stop-Process
```

---

## ⚠️ Note Importanti

1. **URL Temporaneo:** L'URL ngrok-free cambia ad ogni riavvio
2. **Dominio Personalizzato:** Per un URL fisso, configura un dominio personalizzato su ngrok
3. **Backend Locale:** Deve essere attivo sulla porta 8000 prima di avviare ngrok
4. **CORS:** Assicurati che il backend accetti richieste dal dominio ngrok

---

## 🔄 Aggiornare Configurazione

Se l'URL ngrok cambia, aggiorna:
- Frontend: `frontend/src/environments/environment.prod.ts`
- Vercel: Variabili d'ambiente se necessario

---

**Ultimo Aggiornamento:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")


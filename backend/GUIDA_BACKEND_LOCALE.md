# 🖥️ Guida: Backend sul PC Locale

Questa guida ti spiega come far girare il backend NewsFlow sul tuo PC come server pubblico.

## 📋 Opzioni Disponibili

### Opzione 1: ngrok (⭐ CONSIGLIATO - Più Semplice)

**Vantaggi:**
- ✅ Nessuna configurazione router/firewall
- ✅ URL pubblico gratuito
- ✅ Funziona subito
- ✅ HTTPS automatico

**Svantaggi:**
- ⚠️ URL cambia ad ogni riavvio (versione gratuita)
- ⚠️ Limite di connessioni simultanee

**Come usare:**

1. **Installa ngrok:**
   ```powershell
   # Opzione A: Chocolatey
   choco install ngrok
   
   # Opzione B: Download manuale
   # Vai su https://ngrok.com/download
   # Estrai ngrok.exe nella cartella backend
   ```

2. **Avvia backend + ngrok:**
   ```powershell
   cd backend
   .\AVVIA_BACKEND_NGROK.ps1
   ```

3. **Copia l'URL ngrok** che appare (es: `https://abc123.ngrok-free.app`)

4. **Aggiorna il frontend:**
   - Modifica `frontend/src/environments/environment.prod.ts`:
     ```typescript
     export const environment = {
       production: true,
       apiUrl: 'https://abc123.ngrok-free.app/api/v1'  // ← Sostituisci con il tuo URL ngrok
     };
     ```

5. **Ricompila il frontend:**
   ```powershell
   cd frontend
   ng build --configuration production
   ```

6. **Rideploya su Vercel** (push su GitHub)

---

### Opzione 2: Port Forwarding sul Router

**Vantaggi:**
- ✅ URL stabile (se hai IP statico)
- ✅ Nessun limite di connessioni
- ✅ Controllo completo

**Svantaggi:**
- ⚠️ Richiede configurazione router
- ⚠️ Espone il PC a Internet (sicurezza)
- ⚠️ Richiede IP pubblico statico (o servizio DDNS)

**Come usare:**

1. **Trova il tuo IP pubblico:**
   - Vai su https://whatismyipaddress.com
   - Annota il tuo IP pubblico

2. **Configura Port Forwarding sul router:**
   - Accedi al pannello del router (solitamente `192.168.1.1` o `192.168.0.1`)
   - Vai su "Port Forwarding" o "Virtual Server"
   - Aggiungi regola:
     - **Porta esterna:** 8000
     - **Porta interna:** 8000
     - **IP interno:** [IP del tuo PC sulla rete locale]
     - **Protocollo:** TCP

3. **Configura firewall Windows:**
   ```powershell
   # Apri PowerShell come Amministratore
   New-NetFirewallRule -DisplayName "NewsFlow Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

4. **Avvia backend:**
   ```powershell
   cd backend
   .\AVVIA_BACKEND_SEMPLICE.ps1
   ```

5. **Aggiorna frontend** con il tuo IP pubblico:
   ```typescript
   apiUrl: 'http://[TUO_IP_PUBBLICO]:8000/api/v1'
   ```

---

### Opzione 3: Solo Rete Locale (per test)

**Per testare solo sulla tua rete locale:**

```powershell
cd backend
.\AVVIA_BACKEND_LOCALE.ps1
```

Il backend sarà accessibile solo da dispositivi sulla stessa rete WiFi.

---

## 🔧 Configurazione CORS

Il backend è già configurato per accettare richieste da:
- `https://newsflow-orcin.vercel.app` (frontend Vercel)
- `http://localhost:4200` (frontend locale)

Se usi ngrok o un altro dominio, aggiungi l'URL alla variabile `CORS_ORIGINS` nello script.

---

## 🚀 Avvio Rapido

**Per iniziare subito con ngrok:**

```powershell
# 1. Installa ngrok (se non già installato)
choco install ngrok

# 2. Avvia backend + ngrok
cd backend
.\AVVIA_BACKEND_NGROK.ps1

# 3. Copia l'URL ngrok e aggiorna frontend/src/environments/environment.prod.ts
# 4. Ricompila frontend
cd ..\frontend
ng build --configuration production

# 5. Push su GitHub per deploy Vercel
cd ..
git add .
git commit -m "Backend locale con ngrok"
git push origin main
```

---

## ⚠️ Note Importanti

1. **Sicurezza:**
   - Il backend locale è esposto pubblicamente
   - Considera di aggiungere autenticazione se necessario
   - Non esporre dati sensibili

2. **Performance:**
   - Il PC deve essere sempre acceso per servire le richieste
   - Considera l'uso di un VPS per produzione

3. **ngrok URL:**
   - L'URL ngrok gratuito cambia ad ogni riavvio
   - Per URL stabile, considera il piano a pagamento ngrok

4. **Backup:**
   - I file JSON delle notizie sono sul PC locale
   - Fai backup regolari

---

## 🆘 Risoluzione Problemi

**Backend non si avvia:**
- Verifica che Python sia installato: `python --version`
- Installa dipendenze: `pip install -r requirements.txt`

**ngrok non funziona:**
- Verifica che ngrok sia autenticato: `ngrok config add-authtoken [TOKEN]`
- Ottieni il token da https://dashboard.ngrok.com/get-started/your-authtoken

**Frontend non si connette:**
- Verifica che il backend sia attivo: `http://localhost:8000/api/health`
- Controlla CORS nel browser console (F12)
- Verifica che l'URL nel frontend sia corretto

**Port forwarding non funziona:**
- Verifica che il router supporti port forwarding
- Controlla che il firewall Windows permetta la porta 8000
- Verifica che il PC abbia un IP statico sulla rete locale

---

## 📞 Supporto

Se hai problemi, controlla:
1. Log del backend nella console PowerShell
2. Browser console (F12) per errori CORS
3. `http://localhost:8000/api/debug/files` per verificare file JSON


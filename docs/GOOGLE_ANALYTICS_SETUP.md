# 📊 GOOGLE ANALYTICS - Setup Guidato

**Tutto pronto per tracciare utenti e metriche!** 🎯

---

## 🔧 SETUP GOOGLE ANALYTICS (5 MINUTI)

### **Step 1: Ottieni il tuo GA4 ID**

1. **Vai su:** https://analytics.google.com
2. **Login** con il tuo account Google
3. **Click** "Amministrazione" (in basso a sinistra) ⚙️
4. **Crea proprietà** (se non l'hai già):
   - Nome: `NewsFlow`
   - Fuso orario: `Italia`
   - Valuta: `EUR`
5. **Seleziona** "Flusso di dati web"
6. **Aggiungi stream** → Inserisci:
   - URL sito web: `https://newsflow-orcin.vercel.app`
   - Nome stream: `NewsFlow Production`
7. **Ottieni ID misurazione** → Tipo `G-XXXXXXXXXX`

**COPIA QUESTO ID!** 📋

---

### **Step 2: Inserisci ID nel codice**

**Apri:** `frontend/src/index.html`

**Cerca questa riga:**
```html
gtag('config', 'G-XXXXXXXXXX', {
```

**Sostituisci** `G-XXXXXXXXXX` con il TUO ID!

**Esempio:**
```html
gtag('config', 'G-ABC123XYZ', {
```

**Salva il file!**

---

### **Step 3: Deploy**

```bash
git add frontend/src/index.html
git commit -m "Add Google Analytics tracking ID"
git push
```

**Vercel deploya automaticamente!** ✅

**Render non serve modificare** (Analytics solo frontend)

---

## 📊 COSA VERRÀ TRACCIATO

### **Automatico:**
✅ **Page views** (ogni pagina visitata)  
✅ **Sessions** (visite utente)  
✅ **Users** (utenti unici)  
✅ **Bounce rate** (abbandoni)  
✅ **Device type** (desktop/mobile/tablet)  
✅ **Geography** (da dove vengono)  
✅ **Traffic source** (LinkedIn, Facebook, direct, ecc.)

### **Eventi Custom:**
✅ **Article view** (quale articolo leggono)  
✅ **Article save** (quanti salvano)  
✅ **Article share** (quanti condividono)  
✅ **"Spiegami" click** (feature più usata!)  
✅ **"Spiegami" tab** (30sec vs 3min vs deep)  
✅ **Category filter** (categoria più popolare)  
✅ **User login** (nuovi vs returning)  
✅ **Theme change** (dark mode usage)

---

## 📈 DASHBOARD ANALYTICS (Dopo 24H)

### **Metriche Chiave da Guardare:**

**Acquisizione:**
- 👥 Utenti totali
- 🆕 Nuovi utenti
- 🔄 Utenti di ritorno
- 📍 Da dove arrivano (social media)

**Engagement:**
- ⏱️ Tempo medio sessione
- 📄 Pagine per sessione
- 🔥 Bounce rate
- 🎯 Eventi completati

**Contenuto:**
- 📰 Articoli più letti
- 🧠 Click su "Spiegami"
- 🔖 Articoli più salvati
- 🔗 Articoli più condivisi

**Comportamento:**
- 🗂️ Categoria più visitata
- 🌙 Dark mode usage
- 📱 Desktop vs Mobile
- 🌍 Paesi di provenienza

---

## 🎯 OBIETTIVI DA IMPOSTARE

**Google Analytics → Amministrazione → Obiettivi:**

1. **Conversione 1:** User attiva "Spiegami"
2. **Conversione 2:** User salva articolo
3. **Conversione 3:** User condivide articolo
4. **Conversione 4:** User visita 3+ articoli

---

## 🔥 EVENTI TRACCIATI AUTOMATICAMENTE

**Ogni azione genera evento in Analytics!**

**Esempi:**
```
User clicca "Spiegami" 
→ Event: explain_article
→ Category: AI Features
→ Label: "OpenAI può tenere il passo..."

User filtra per "Cybersecurity"
→ Event: filter_category
→ Category: Navigation
→ Label: "Cybersecurity"

User salva articolo
→ Event: save_article
→ Category: Articles
→ Label: "Hackers Exploiting Triofox..."
```

**Vedrai TUTTO in real-time!** 📊

---

## ⚡ QUICK START

### **ADESSO FAI:**

1. **Vai su** https://analytics.google.com
2. **Crea proprietà** "NewsFlow"
3. **Copia il tuo ID** (es: `G-ABC123XYZ`)
4. **Dimmi l'ID** e lo inserisco nel codice!

**Oppure:**

5. **Sostituisci tu** in `frontend/src/index.html` riga 16
6. **Push** e deploy automatico!

---

## 🎊 DOPO IL SETUP:

**Entro 24h vedrai:**
- Chi arriva da LinkedIn, Facebook, X
- Quanti cliccano "Spiegami"
- Quale categoria piace di più
- Quanto tempo passano sull'app

**Dashboard live:** https://analytics.google.com

---

**DAMMI IL TUO GOOGLE ANALYTICS ID E LO COLLEGO!** 🔌📊

Oppure lo sostituisci tu in `frontend/src/index.html` e fai push! 🚀

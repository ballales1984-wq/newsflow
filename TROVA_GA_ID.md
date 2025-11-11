# 🔍 COME TROVARE L'ID DI MISURAZIONE GOOGLE ANALYTICS

**Hai l'Account ID (373636887), ma serve l'ID di misurazione!** ✅

---

## 📋 PASSO-PASSO:

### **1. Vai su Google Analytics**
https://analytics.google.com

### **2. Login** con il tuo account

### **3. Click su "Amministrazione"** ⚙️
(In basso a sinistra)

### **4. Nella colonna "Proprietà":**
- Se NON hai ancora una proprietà:
  - Click "Crea proprietà"
  - Nome: `NewsFlow`
  - Fuso orario: `(GMT+01:00) Amsterdam, Berlino, Roma`
  - Valuta: `EUR - Euro`
  - Click "Avanti"

### **5. Nella sezione "Flussi di dati":**
- Click "Flussi di dati"
- Click "Aggiungi flusso" → "Web"
- Inserisci:
  - **URL sito web:** `https://newsflow-orcin.vercel.app`
  - **Nome flusso:** `NewsFlow Production`
- Click "Crea flusso"

### **6. COPIA L'ID DI MISURAZIONE!** 📋

Vedrai qualcosa tipo:

```
ID misurazione
G-ABC123XYZ4
```

**Questo è l'ID che serve!** Inizia con **"G-"**!

---

## ✅ ESEMPIO:

**❌ SBAGLIATO:** `373636887` (Account ID)  
**✅ GIUSTO:** `G-ABC123XYZ4` (Measurement ID)

---

## 🎯 QUANDO HAI L'ID "G-XXXXXXXXX":

**Dimmi l'ID e lo inserisco subito nel codice!**

Oppure puoi farlo tu:

1. Apri `frontend/src/index.html`
2. Cerca riga 16: `gtag('config', 'G-XXXXXXXXXX'`
3. Sostituisci con il TUO ID
4. Salva
5. Push!

---

**TROVA L'ID CHE INIZIA CON "G-" E DIMMELO!** 🎯


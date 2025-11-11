# 🧪 Test Manuale Frontend - Checklist

## ✅ HOMEPAGE

### Elementi Visibili:
- [ ] Header con logo "NewsFlow"
- [ ] Barra ricerca funzionante
- [ ] Pulsante tema chiaro/scuro
- [ ] Sidebar con modalità lettura
- [ ] Sidebar con 8 categorie
- [ ] Sidebar con Libreria (Salvati, Preferiti, ecc.)
- [ ] Almeno 10 card notizie visibili
- [ ] Paginazione in fondo (se > 20 notizie)

---

## ✅ CARD NOTIZIA

Ogni card dovrebbe avere:
- [ ] Immagine (se disponibile dalla fonte)
- [ ] Titolo notizia
- [ ] Autore e data
- [ ] Tempo di lettura
- [ ] Sommario (prime righe)
- [ ] Quality score badge
- [ ] Keywords chips
- [ ] **4 PULSANTI:**
  - [ ] 🔖 Salva (bookmark)
  - [ ] 📤 Condividi (share)
  - [ ] 🔗 Apri originale (open_in_new)
  - [ ] 🧠 **SPIEGAMI** (school icon)
  - [ ] ➡️ Leggi (arrow_forward)

---

## ✅ FUNZIONALITÀ PULSANTI

### Pulsante "Salva":
- [ ] Click → Icona diventa piena (bookmark → bookmark_filled)
- [ ] Click di nuovo → Icona torna vuota
- [ ] Articolo salvato appare in "Salvati" (sidebar)

### Pulsante "Condividi":
- [ ] Click → Share API (se supportato) O copia link
- [ ] Messaggio "Link copiato" appare

### Pulsante "Apri originale":
- [ ] Click → Apre sito fonte in nuova tab
- [ ] URL corretto (Guardian, Wired, ecc.)

### Pulsante "SPIEGAMI" 🧠:
- [ ] Click → Si apre MODAL
- [ ] Modal ha titolo "Spiegami questa notizia"
- [ ] **3 TAB visibili:**
  - [ ] ⚡ "30 secondi"
  - [ ] 📄 "3 minuti"
  - [ ] 📚 "Approfondimento"
- [ ] Contenuto cambia tra tab
- [ ] Pulsante "Chiudi" funziona
- [ ] Pulsante "Leggi Originale" funziona

### Pulsante "Leggi":
- [ ] Click → Apre pagina dettaglio
- [ ] URL cambia in `/article/slug-notizia`

---

## ✅ PAGINA DETTAGLIO ARTICOLO

- [ ] Pulsante "Indietro" (← arrow_back)
- [ ] Titolo completo
- [ ] Metadata (autore, data, tempo lettura)
- [ ] Immagine articolo (se disponibile)
- [ ] Sommario evidenziato
- [ ] Contenuto completo
- [ ] Parole chiave chips
- [ ] Entità riconosciute (se disponibili)
- [ ] Pulsanti: Salva, Condividi, Leggi originale

---

## ✅ PAGINA SALVATI

- [ ] Click "Salvati" in sidebar → Apre pagina
- [ ] URL = `/saved`
- [ ] Mostra solo articoli salvati
- [ ] Se nessuno salvato → Messaggio "Nessun articolo salvato"

---

## ✅ RICERCA

- [ ] Campo ricerca in header
- [ ] Digitare testo + Enter → Va a `/search`
- [ ] Mostra risultati filtrati
- [ ] Filtri categoria funzionano
- [ ] Filtri data funzionano

---

## ✅ CATEGORIE

- [ ] Click categoria in sidebar → Filtra notizie
- [ ] URL cambia con `?category=X`
- [ ] Solo notizie di quella categoria
- [ ] Click "Tutte" → Rimuove filtro

---

## ✅ TEMA

- [ ] Click icona tema → Body cambia classe
- [ ] Tema scuro: Sfondo scuro, testo chiaro
- [ ] Tema chiaro: Sfondo chiaro, testo scuro
- [ ] Preferenza salvata (refresh mantiene tema)

---

## ✅ RESPONSIVE

- [ ] Mobile (< 768px): Sidebar nascosta
- [ ] Mobile: Card a colonna singola
- [ ] Tablet (768-1024px): 2 colonne
- [ ] Desktop (> 1024px): 3+ colonne

---

## ✅ PERFORMANCE

- [ ] Homepage carica in < 3 secondi
- [ ] Click notizia → Dettaglio in < 1 secondo
- [ ] Modal "Spiegami" si apre istantaneamente
- [ ] Nessun lag o freeze

---

## 📊 RISULTATO ATTESO:

✅ **Tutti i checkbox spuntati** = App perfetta!

⚠️ **Qualche checkbox vuoto** = Cose da sistemare

❌ **Molti vuoti** = Debug necessario

---

## 🎯 COME USARE:

1. Apri http://localhost:4200
2. Segui checklist punto per punto
3. Spunta checkbox quando funziona
4. Annota cosa NON funziona
5. Mandami la lista e sistemo!

---

*Test creato: 11 Nov 2024, 02:10 AM*


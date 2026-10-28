# 📰 Progetto Testata Giornalistica Digitale

## 🎯 IDENTITÀ DELLA TESTATA

### Nome Proposto: **SINTESI**
*Sottotitolo: "Notizie curate dall'intelligenza critica"*

**Alternative:**
- **Specchio Critico** - riflette senza distorcere
- **Contrappunto** - dialettico, musicale
- **Ritmo del Mondo** - cadenzato, ritualistico
- **Fatti e Contrappunti** - duale, comparativo
- **L'Essenziale** - minimalista, preciso

---

## 🧭 MANIFESTO FONDATIVO

### Vision

> In un mondo sommerso da informazioni, **SINTESI** distilla l'essenziale. 
> 
> Non siamo giornalisti che scrivono: siamo curatori che selezionano.
> Non abbiamo opinioni: presentiamo contrappunti.
> Non rincorriamo click: rispettiamo il tuo tempo.

### Mission

**SINTESI** offre ogni giorno una selezione imparziale e semanticamente rilevante delle notizie che contano, confrontando sempre le fonti e restituendo solo ciò che merita attenzione.

### Principi

1. **Imparzialità algoritmica** - L'AI seleziona per qualità, non per ideologia
2. **Confronto sistemico** - Ogni fatto presenta almeno due interpretazioni
3. **Ritualità** - Orari fissi, sezioni ricorrenti, linguaggio coerente
4. **Trasparenza** - Fonti sempre citate, metodo sempre spiegato
5. **Rispetto del tempo** - Brevità, chiarezza, sintesi
6. **Qualità > Quantità** - 5 notizie verificate > 50 rumori

---

## 📂 STRUTTURA DELLA TESTATA

### Homepage Sezioni

```
┌─────────────────────────────────────────┐
│  🔹 SINTESI - Il giornale dell'essen-   │
│     ziale                               │
├─────────────────────────────────────────┤
│                                         │
│  📌 LE TRE DEL GIORNO                   │
│  ├─ Notizia 1 (confronto fonti A vs B) │
│  ├─ Notizia 2 (analisi semantica)      │
│  └─ Notizia 3 (impatto globale)        │
│                                         │
│  🎭 FATTI & CAMPANE                     │
│  └─ Stesso tema, tre prospettive:      │
│      • Fonte progressista               │
│      • Fonte conservatrice              │
│      • Fonte tecnica/neutrale           │
│                                         │
│  🔍 SEGNALI DEBOLI                      │
│  └─ Notizie sottovalutate ma significa- │
│     tive (low volume, high impact)      │
│                                         │
│  📖 EDITORIALE RITUALE                  │
│  └─ Una riflessione quotidiana breve    │
│     (max 200 parole)                    │
│                                         │
│  🗂️ ARCHIVIO SEMANTICO                 │
│  └─ Ricerca per tema, tono, fonte       │
│                                         │
└─────────────────────────────────────────┘
```

### Pagine Secondarie

- **Chi Siamo / Manifesto**
- **Come Funziona** (trasparenza algoritmica)
- **Fonti** (lista e metodologia)
- **Archivio** (cronologico e tematico)
- **Newsletter** (iscrizione)
- **Contatti / Segnalazioni**

---

## 🎨 IDENTITÀ VISIVA

### Palette Colori

```css
:root {
  /* Neutri - base della testata */
  --nero-inchiostro: #1a1a1a;
  --grigio-carta: #f5f5f5;
  --bianco-pagina: #ffffff;
  
  /* Accenti - categorie */
  --blu-tecnologia: #2563eb;
  --verde-scienza: #059669;
  --rosso-urgente: #dc2626;
  --giallo-cultura: #d97706;
  --viola-filosofia: #7c3aed;
  
  /* Sentiment */
  --grigio-neutro: #6b7280;
  --ambra-warning: #f59e0b;
}
```

### Typography

```css
/* Titoli - Autoritari ma leggibili */
font-family: 'Merriweather', serif;

/* Body - Chiarezza assoluta */
font-family: 'Inter', sans-serif;

/* Monospace - Dati e codici */
font-family: 'JetBrains Mono', monospace;
```

### Logo Concept

```
┌─────────────┐
│   SINTESI   │  ← Maiuscolo, spaziato
│      ◆      │  ← Simbolo: diamante (purezza)
│   dal 2024  │  ← Timestamp: trasparenza
└─────────────┘
```

---

## ✍️ STILE EDITORIALE

### Tono

- **Sobrio** - niente sensazionalismi
- **Chiaro** - linguaggio B2 (upper intermediate)
- **Simbolico** - uso di metafore geometriche/musicali
- **Rispettoso** - del lettore e delle fonti

### Formato Standard Articolo

```markdown
# Titolo (max 10 parole)

**Sintesi** (3 righe)
Riassunto ultra-compresso della notizia.

**Contesto**
Perché questa notizia è rilevante ora.

**Confronto Fonti**
- Fonte A (progressista): "[citazione]"
- Fonte B (conservatrice): "[citazione]"
- Fonte C (tecnica): "[citazione]"

**Analisi**
Cosa emerge dal confronto, senza giudizio.

**Impatto**
Chi/cosa è influenzato da questo evento.

**Collegamenti**
- Articolo originale Fonte A
- Articolo originale Fonte B
- Background context (Wikipedia/etc)

---
Pubblicato: 2024-01-15 07:00
Categoria: Tecnologia
Quality Score: 0.87
Keyword: AI, Regolamentazione, Europa
```

### Linee Guida Scrittura

1. **Prima riga = massima densità informativa**
2. **Soggetto-Verbo-Oggetto** (no inversioni artificiali)
3. **Niente aggettivi emotivi** (grande → significativo)
4. **Sempre fonte esplicita** (secondo X, Y afferma che...)
5. **Confronto obbligatorio** (mai un solo punto di vista)

---

## 🌐 CANALI DISTRIBUZIONE

### 1. Sito Web (Primario)

**URL suggeriti:**
- sintesi.news
- sintesi.media
- sintesi.world
- leggisintesi.it

**Stack Tech:**
- Frontend: Angular (già pronto con NewsFlow!)
- Backend: FastAPI + NLP (già pronto!)
- CMS: Headless (Strapi/Contentful) per editoriali
- Hosting: Vercel + Render

### 2. Newsletter

**Formato:**

```
SINTESI - Edizione Mattutina
15 Gennaio 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 LE TRE DEL GIORNO

1. [Titolo breve]
   → Sintesi in 2 righe
   → [Leggi analisi completa]

2. [Titolo breve]
   → Sintesi in 2 righe
   → [Leggi analisi completa]

3. [Titolo breve]
   → Sintesi in 2 righe
   → [Leggi analisi completa]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎭 Confronto del Giorno
[Tema caldo visto da 3 angolazioni]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 Editoriale Rituale
[150 parole di riflessione]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Questa newsletter è curata da algoritmi
semantici e supervisionata da esseri umani.

[Modifica preferenze] | [Archivio] | [Chi siamo]
```

**Orari:**
- **Edizione Mattutina**: 07:00 (prima del lavoro)
- **Edizione Serale**: 19:00 (approfondimento)
- **Sintesi Settimanale**: Domenica 10:00

### 3. Canale Telegram

**Nome:** @SintesiNews

**Formato post:**

```
🔹 [CATEGORIA]

Titolo ultra-compresso

→ Sintesi 1 riga
→ Fonte A: [posizione]
→ Fonte B: [posizione]

🔗 Leggi analisi: [link]

#keyword1 #keyword2
```

**Frequenza:** Max 5 post/giorno

### 4. Social (Selettivi)

- **X/Twitter**: Per dibattito e segnalazioni
- **LinkedIn**: Notizie business/tech
- **Mastodon**: Community indipendente
- **NO Facebook/Instagram**: troppo rumorosi

### 5. Podcast/YouTube (Fase 2)

**Format:** "Il Contrappunto"
- 15 minuti/giorno
- 2-3 notizie analizzate a voce
- Stesso stile sobrio

---

## 💾 MODELLO DATI ESTESO

```typescript
interface ArticoloTestata extends Article {
  // Campi base da NewsFlow
  id: number;
  title: string;
  content: string;
  
  // Campi specifici testata
  sintesi: string;              // 3 righe max
  contesto: string;             // Perché ora
  confrontoFonti: {
    fonte: string;
    posizione: string;
    citazione: string;
    url: string;
    orientamento: 'progressista' | 'conservatore' | 'neutrale';
  }[];
  impatto: string;              // Chi è influenzato
  segnaliDeboli: boolean;       // Low volume, high impact
  editoriale: boolean;          // È un editoriale?
  
  // Metadati editoriali
  editore: string;              // Chi ha curato
  dataPublicazione: Date;
  oraPublicazione: string;      // "07:00" per ritualità
  versioneTestata: number;      // Per tracking modifiche
  
  // Engagement
  visualizzazioni: number;
  salvataggi: number;
  condivisioni: {
    telegram: number;
    twitter: number;
    email: number;
  };
}
```

---

## 🚀 ROADMAP LANCIO

### Fase 0: Preparazione (2 settimane)

- [x] Definire identità e manifesto ✅
- [ ] Registrare dominio
- [ ] Setup infrastruttura tech
- [ ] Creare logo e identità visiva
- [ ] Scrivere 10 articoli pilota

### Fase 1: Soft Launch (1 mese)

- [ ] Sito online con 5 notizie/giorno
- [ ] Newsletter a 50 beta tester
- [ ] Canale Telegram privato
- [ ] Raccolta feedback

### Fase 2: Lancio Pubblico (2 mesi)

- [ ] Campagna social mirata
- [ ] Collaborazioni con altre testate indipendenti
- [ ] Prime interviste/podcast
- [ ] Target: 1000 lettori/giorno

### Fase 3: Consolidamento (6 mesi)

- [ ] Podcast settimanale
- [ ] Partnership fonti premium
- [ ] Community forum/Discord
- [ ] Target: 10.000 lettori/giorno

### Fase 4: Monetizzazione (12 mesi)

- [ ] Abbonamenti premium (€3/mese)
- [ ] Sponsor etici (no pubblicità invasiva)
- [ ] Licenza algoritmo ad altre testate
- [ ] Target: Sostenibilità economica

---

## 💰 MODELLO BUSINESS

### Freemium

**Gratis:**
- 3 notizie/giorno
- Newsletter base
- Archivio ultimi 7 giorni

**Premium (€2.99/mese):**
- Tutte le notizie
- Newsletter completa (mattina + sera)
- Archivio illimitato
- Export PDF/EPUB
- Notifiche personalizzate
- No ads (se presenti)

### Sponsor Etici

- Università e centri ricerca
- Think tank indipendenti
- Fondazioni culturali
- Tech company etiche

**Regole:**
- Max 1 sponsor/giorno
- Disclaimer trasparente
- No influenza editoriale
- Revoca immediata se conflitto

---

## 📐 LAYOUT TECNICO HOMEPAGE

```html
<div class="testata-container">
  <!-- Header -->
  <header class="testata-header">
    <div class="logo">SINTESI</div>
    <nav>
      <a href="#tre-del-giorno">Le Tre</a>
      <a href="#fatti-campane">Confronti</a>
      <a href="#archivio">Archivio</a>
      <a href="#manifesto">Manifesto</a>
    </nav>
    <div class="azioni">
      <button>Newsletter</button>
      <button>Accedi</button>
    </div>
  </header>

  <!-- Sezione Hero -->
  <section class="tre-del-giorno">
    <h2>Le Tre del Giorno</h2>
    <div class="orario">Aggiornato: Oggi, 07:00</div>
    
    <article class="notizia-principale">
      <!-- Notizia 1 - Grande -->
    </article>
    
    <div class="notizie-secondarie">
      <article><!-- Notizia 2 --></article>
      <article><!-- Notizia 3 --></article>
    </div>
  </section>

  <!-- Confronti -->
  <section class="fatti-campane">
    <h2>Fatti & Campane</h2>
    <div class="tema-del-giorno">
      <h3>[Tema caldo]</h3>
      <div class="prospettive">
        <div class="prospettiva fonte-a">...</div>
        <div class="prospettiva fonte-b">...</div>
        <div class="prospettiva fonte-c">...</div>
      </div>
    </div>
  </section>

  <!-- Segnali Deboli -->
  <section class="segnali-deboli">
    <h2>Segnali Deboli</h2>
    <!-- Notizie sottovalutate -->
  </section>

  <!-- Editoriale -->
  <section class="editoriale">
    <h2>Editoriale Rituale</h2>
    <article class="riflessione-giorno">
      <!-- Max 200 parole -->
    </article>
  </section>

  <!-- Footer -->
  <footer class="testata-footer">
    <div class="manifesto-breve">
      "Notizie curate dall'intelligenza critica"
    </div>
    <div class="metodo">
      <a href="/come-funziona">Come funziona</a>
      <a href="/fonti">Le nostre fonti</a>
      <a href="/manifesto">Manifesto completo</a>
    </div>
    <div class="social">
      <!-- Link social -->
    </div>
  </footer>
</div>
```

---

## 🎯 KPI e Metriche

### Qualità (priorità)

- Tempo medio di lettura (target: >3 min)
- Tasso salvataggio (target: >15%)
- Condivisioni spontanee
- Feedback qualitativo

### Crescita

- Lettori unici/giorno
- Iscritti newsletter
- Follower Telegram
- Retention rate (>60%)

### Business (fase 3+)

- Conversione free→premium (target: 5%)
- Churn rate (<10%)
- Revenue per user

---

## 📞 PROSSIMI PASSI IMMEDIATI

### Azione 1: Scegliere Nome e Dominio

```bash
# Verifica disponibilità
whois sintesi.news
whois sintesi.media
whois specchiocritic.com
```

### Azione 2: Setup Tecnico

```bash
# Clone NewsFlow e personalizza
git clone newsflow newsflow-testata
cd newsflow-testata

# Personalizza branding
# Modifica frontend/src/styles.scss (colori)
# Modifica logo e favicon
# Aggiungi sezioni testata
```

### Azione 3: Scrivere Primi 5 Articoli

- Scegli 5 notizie rilevanti di oggi
- Applica formato "Confronto Fonti"
- Pubblica come test

### Azione 4: Landing Page

Crea pagina minima:
- Manifesto
- Esempio articolo
- Form newsletter
- "Coming Soon: [data]"

---

## 🤝 COLLABORAZIONI POTENZIALI

- **Open Source:** Condividi algoritmo curation
- **Università:** Partnership ricerca su news literacy
- **Altre testate indipendenti:** Scambio contenuti
- **Fact-checking:** Integrazione servizi verifica

---

## ✨ ELEMENTI DISTINTIVI UNICI

1. **Ritualità oraria** - pubblichi sempre 07:00 e 19:00
2. **Confronto obbligatorio** - mai una sola fonte
3. **Quality score visibile** - trasparenza algoritmica
4. **Segnali deboli** - notizie sottovalutate
5. **Editoriale rituale** - 200 parole di riflessione
6. **Zero clickbait** - titoli descrittivi, non emotivi
7. **Open algorithm** - codice pubblico su GitHub

---

## 🎬 CONCLUSIONE

**SINTESI** non è solo una testata: è un **esperimento di giornalismo algoritmico etico**.

Combina:
- La potenza dell'AI (NewsFlow)
- La responsabilità umana (cura editoriale)
- La trasparenza radicale (codice aperto)
- Il rispetto del lettore (brevità e chiarezza)

**Sei pronto a lanciare?**

---

**Vuoi che sviluppi:**
1. Il **logo e identità visiva** completa?
2. I primi **3 articoli esempio** formattati?
3. Il **codice della homepage** della testata?
4. La **landing page** pre-lancio?

**Oppure procediamo con il lancio tecnico immediato?**

Dimmi tu! 🚀


# Piano miglioramento Frontend (NewsFlow Angular)

## Contesto
App Angular 17 + Angular Material, temi light/dark, pagine: home, search, saved, digest, article-detail, auth, privacy/terms. Backend FastAPI su Vercel/Render.

## Obiettivi
- Performance (bundle, lazy loading, change detection)
- UX/UI (responsive, accessibilità, stati loading/empty/error)
- Qualità codice (rimozione console.log, tipizzazione, service patterns)
- PWA/offline, SEO, analytics

## Fasi

### Fase 1 — Igiene e stabilità (priorità alta)
1. Rimuovere tutti i `console.log`/`console.error` di debug da componenti e servizi (62 occorrenze); sostituire con logging condizionale in dev only.
2. Eliminare `alert()` da flussi utente (home, article-card, explain) → usare MatSnackBar.
3. Tipizzare `any` nei service (article.service, category.service) e modelli.
4. Aggiungere error boundaries / stato errore riutilizzabile (componente `error-state`).
5. Unificare gestione errori HTTP in interceptor (toast + retry).

### Fase 2 — Performance
1. Lazy loading delle route (loadComponent) per search/saved/digest/article-detail/auth/privacy/terms.
2. OnPush change detection su componenti presentazionali (article-card, category-filter, header).
3. Virtual scrolling per liste lunghe (cdk-virtual-scroll-viewport) in home/article-list.
4. Ottimizzare `loadCategoryCounts` (evitare fetch 1000 articoli lato client; spostare conteggi in endpoint backend `/categories/counts`).
5. Preconnect/prefetch immagini, lazy loading immagini (`loading="lazy"`).
6. Bundle analysis (source-map-explorer) e tree-shaking Material (importare solo moduli usati).

### Fase 3 — UX/UI
1. Skeleton loaders al posto dello spinner globale.
2. Stati empty (nessun articolo, nessun risultato ricerca, nessun salvato).
3. Migliorare responsive (mobile nav, drawer sidebar, bottom nav).
4. Dark/light theme toggle persistente (già presente: verificare FOUC e prefers-color-scheme).
5. Accessibilità: focus management nei dialog, aria-label su bottoni icona, contrasto colori.
6. Infinite scroll o paginazione più fluida (caricamento incrementale).

### Fase 4 — Funzionalità
1. Ricerca full-text server-side (debounce 300ms, cancellazione richieste).
2. Filtri avanzati (data, fonte, qualità minima).
3. Salvataggio articoli offline (IndexedDB + sync).
4. Notifiche push (service worker già configurato).
5. Condivisione nativa robusta (fallback clipboard con feedback).
6. Lettura vocale migliorata (voice selection, play/pause, speed).

### Fase 5 — Qualità e test
1. Unit test per servizi (article, saved, category) e componenti chiave.
2. E2E Playwright (già presente spec) esteso a flussi critici.
3. Lint/format (eslint + prettier) in CI.
4. Storybook per componenti UI (opzionale).

### Fase 6 — SEO e analytics
1. Meta tags dinamici per articolo (title, description, og:image) via SeoService.
2. Sitemap/robots, structured data (JSON-LD NewsArticle).
3. GA4 eventi già presenti: verificare naming e consent (cookie banner).

## Metriche di successo
- LCP < 2.5s, CLS < 0.1, INP < 200ms
- Bundle iniziale < 300KB gzipped
- 0 `console.log` in build prod
- Copertura test > 60% sui servizi

## Primi passi consigliati
1. Fase 1 (igiene) — quick wins, basso rischio.
2. Fase 2.1 (lazy loading) + 2.4 (conteggi backend) — impatto alto.
3. Fase 3.1 (skeleton) — percezione performance.

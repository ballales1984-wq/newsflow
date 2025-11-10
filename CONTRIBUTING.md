# Contribuire a NewsFlow

Grazie per il tuo interesse nel contribuire a NewsFlow! Questa guida ti aiuterà a iniziare.

## 🤝 Come Contribuire

### 1. Fork e Clone

```bash
# Fork il repository su GitHub, poi:
git clone https://github.com/your-username/newsflow.git
cd newsflow
```

### 2. Crea un Branch

```bash
git checkout -b feature/nome-feature
# oppure
git checkout -b fix/nome-bug
```

### 3. Setup Ambiente

Segui la guida in [SETUP.md](./SETUP.md) per configurare l'ambiente di sviluppo.

### 4. Fai le Modifiche

- Scrivi codice pulito e ben documentato
- Segui le convenzioni di stile del progetto
- Aggiungi test per le nuove funzionalità
- Aggiorna la documentazione se necessario

### 5. Test

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
ng test
ng lint
```

### 6. Commit

Usa messaggi di commit descrittivi:

```bash
git add .
git commit -m "feat: aggiungi filtro per data pubblicazione"
```

**Convenzioni commit:**
- `feat:` nuova funzionalità
- `fix:` correzione bug
- `docs:` modifiche documentazione
- `style:` formattazione, punto e virgola mancanti, etc
- `refactor:` refactoring codice
- `test:` aggiunta test
- `chore:` task di manutenzione

### 7. Push e Pull Request

```bash
git push origin feature/nome-feature
```

Apri una Pull Request su GitHub con:
- Titolo descrittivo
- Descrizione delle modifiche
- Screenshot se applicabile
- Riferimenti a issue correlate

## 📝 Linee Guida

### Codice Backend (Python)

- Segui [PEP 8](https://pep8.org/)
- Usa type hints
- Documenta funzioni con docstrings
- Mantieni funzioni piccole e focalizzate

```python
def calculate_relevance(
    article_keywords: List[str],
    user_interests: List[str]
) -> float:
    """
    Calculate relevance score between article and user interests.
    
    Args:
        article_keywords: Keywords from article
        user_interests: User's interest keywords
        
    Returns:
        Relevance score between 0 and 1
    """
    # Implementation
    pass
```

### Codice Frontend (Angular/TypeScript)

- Segui [Angular Style Guide](https://angular.io/guide/styleguide)
- Usa TypeScript strict mode
- Componenti piccoli e riutilizzabili
- Usa RxJS operators appropriati

```typescript
export class ArticleService {
  constructor(private http: HttpClient) {}

  /**
   * Get articles with pagination and filters
   */
  getArticles(page: number, filters?: ArticleFilters): Observable<ArticleList> {
    // Implementation
  }
}
```

### Documentazione

- README per overview
- Commenti nel codice per logica complessa
- JSDoc/Docstrings per API pubbliche
- Esempi di utilizzo

## 🐛 Segnalare Bug

Usa il [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) e includi:

- Descrizione chiara del problema
- Passi per riprodurre
- Comportamento atteso vs attuale
- Screenshots se applicabile
- Versioni (OS, browser, Python, Node)
- Logs rilevanti

## 💡 Proporre Feature

Usa il [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) e includi:

- Descrizione della feature
- Casi d'uso
- Benefici
- Possibili implementazioni
- Alternative considerate

## 🎨 Aree di Contribuzione

### Backend

- [ ] Nuovi collector per fonti RSS
- [ ] Miglioramenti analisi NLP
- [ ] Ottimizzazioni performance
- [ ] Sistema di raccomandazioni
- [ ] API per esportazione dati

### Frontend

- [ ] Nuovi componenti UI
- [ ] Temi personalizzati
- [ ] Modalità offline
- [ ] PWA features
- [ ] Accessibility improvements

### Documentazione

- [ ] Tutorial video
- [ ] Guide per utenti
- [ ] Esempi codice
- [ ] Traduzioni

### Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Performance tests

## 🔍 Code Review

Tutte le Pull Request passano attraverso code review:

- Verifica che i test passino
- Controlla la qualità del codice
- Valuta impatto su performance
- Assicura documentazione adeguata

## 📜 Licenza

Contribuendo a NewsFlow, accetti che i tuoi contributi saranno licenziati sotto la [MIT License](./LICENSE).

## 🌟 Riconoscimenti

I contributori saranno riconosciuti in:
- [Contributors page](https://github.com/your-username/newsflow/contributors)
- Release notes
- README.md (per contributi significativi)

## 📞 Domande?

- Apri una [Discussion](https://github.com/your-username/newsflow/discussions)
- Contatta il maintainer
- Consulta la documentazione

## 🙏 Grazie!

Il tuo contributo rende NewsFlow migliore per tutti!

---

**Happy Coding!** 💻


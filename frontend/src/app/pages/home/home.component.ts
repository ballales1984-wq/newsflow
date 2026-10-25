import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ArticleService } from '../../services/article.service';
import { CategoryService } from '../../services/category.service';
import { SpeechService } from '../../services/speech.service';
import { ScrollPositionService } from '../../services/scroll-position.service';
import { Article } from '../../models/article.model';
import { Category } from '../../models/category.model';
import { PageEvent } from '@angular/material/paginator';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatPaginatorModule } from '@angular/material/paginator';
import { timeout, catchError, filter } from 'rxjs/operators';
import { of, Subscription } from 'rxjs';
import { CategoryFilterComponent } from '../../components/category-filter/category-filter.component';
import { ArticleListComponent } from '../../components/article-list/article-list.component';

/**
 * Pagina principale: elenco articoli, filtro per categoria, ricerca rapida
 * e paginazione.
 *
 * L'URL è la fonte di verità dello stato di navigazione: la categoria scelta
 * vive in ?category=<id> e il componente si ricostruisce da lì (reload, link
 * condiviso, back dal browser).
 */
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatButtonModule,
    MatTooltipModule,
    MatPaginatorModule,
    CategoryFilterComponent,
    ArticleListComponent
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  // articles = vista filtrata mostrata a schermo; rawArticles = pagina
  // ricevuta dal server. La ricerca client-side lavora solo su rawArticles.
  articles: Article[] = [];
  rawArticles: Article[] = [];
  categories: Category[] = [];
  categoryCounts: { [categoryId: number]: number } = {}; // Conteggio articoli per categoria
  loading = false;
  selectedCategoryId: number | null = null;
  searchQuery: string = '';
  private routerSubscription?: Subscription;
  
  // Pagination
  totalArticles = 0;
  // Pagina grande di proposito: con il filtro e la ricerca applicati lato
  // client, una pagina più piccola mostrerebbe pochi risultati utili.
  pageSize = 50; // Aumentato per mostrare più articoli per pagina
  // Numero di pagina 1-based come atteso dal servizio, che lo converte in
  // skip = (pagina - 1) * pageSize per l'API.
  currentPage = 1;
  
  // Error display
  // Dettagli dell'ultimo errore mostrati in un pannello e salvati in
  // localStorage, così restano recuperabili anche dopo un reload.
  lastError: string | null = null;
  showError = false;

  constructor(
    private articleService: ArticleService,
    private categoryService: CategoryService,
    private speechService: SpeechService,
    private scrollPositionService: ScrollPositionService,
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    console.log('🏠 HomeComponent initialized');
    try {
      this.loadCategories();
      
      // Ascolta navigazione per ripristinare scroll quando si torna dalla pagina articolo
      // La posizione è salvata dalla card prima di aprire l'articolo e ripristinata
      // qui al rientro, così l'utente torna al punto esatto della lista.
      this.routerSubscription = this.router.events
        .pipe(filter(event => event instanceof NavigationEnd))
        .subscribe((event: any) => {
          // Se torniamo alla home da un articolo, ripristina la posizione
          if (event.url === '/' || event.urlAfterRedirects === '/') {
            setTimeout(() => {
              this.scrollPositionService.restoreScrollPosition('home');
            }, 100);
          }
        });
      
      // Load articles immediately on init and listen to query params changes
      // Ogni cambio di ?category rilancia il caricamento: il filtro non viene
      // applicato in locale, è il server a restituire gli articoli della categoria.
      this.route.queryParams.subscribe(params => {
        console.log('📋 Query params changed:', params);
        const previousCategoryId = this.selectedCategoryId;
        const isFirstLoad = this.selectedCategoryId === null && previousCategoryId === null;
        // La categoria arriva come stringa nella query param: va convertita
        // in numero per confrontarla con gli id delle categorie.
        this.selectedCategoryId = params['category'] ? +params['category'] : null;
        // Cambio di filtro = nuova pagina 1: la pagina corrente riguarderebbe
        // un insieme di articoli diverso.
        this.currentPage = 1;
        this.loadArticles();
        
        // Scroll to filtered articles section when category changes
        // Scroll sempre quando c'è una categoria selezionata (anche se è la stessa)
        // Lo scroll verrà fatto anche dopo il caricamento degli articoli (nel subscribe)
        // Questo è un backup nel caso il componente sia già caricato
        if (this.selectedCategoryId !== null && previousCategoryId !== this.selectedCategoryId) {
          setTimeout(() => {
            this.scrollToFilteredArticles();
          }, 1000); // Aspetta che gli articoli siano caricati
        }
      });
    } catch (error) {
      console.error('❌ Error in ngOnInit:', error);
    }
  }

  ngOnDestroy(): void {
    if (this.routerSubscription) {
      this.routerSubscription.unsubscribe();
    }
  }

  loadCategories(): void {
    this.categoryService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        // Carica conteggi articoli per categoria
        this.loadCategoryCounts();
      },
      error: (error) => {
        console.error('Error loading categories:', error);
      }
    });
  }

  loadCategoryCounts(): void {
    // Ottimizzato: usa requestAnimationFrame per non bloccare UI
    // Carica tutti gli articoli per contare quelli per categoria
    // Il backend non espone un conteggio per categoria, quindi si scarica una
    // pagina molto grande (fino a 1000 articoli) e si conta qui: è un costo
    // una tantum, contenuto dal fatto che il conteggio gira a chunk.
    this.articleService.getArticles(1, 1000, {}).subscribe({
      next: (response) => {
        const allArticles = response.items || [];
        
        // Mappa keywords → category_id (come nel backend) - ottimizzata per lookup veloce
        // Replica la classificazione del backend: serve solo per gli articoli
        // che arrivano senza category_id.
        const KEYWORD_TO_CATEGORY_ID: { [key: string]: number } = {
          'technology': 1, 'tech': 1, 'tecnologia': 1,
          'science': 2, 'scienz': 2,
          'philosophy': 3, 'filosofia': 3,
          'cybersecurity': 4, 'security': 4, 'sicurezza': 4,
          'ai': 5, 'artificial intelligence': 5, 'intelligenza artificiale': 5,
          'innovation': 6, 'innovazione': 6,
          'culture': 7, 'cultura': 7,
          'ethics': 8, 'etica': 8,
          'sport': 9, 'calcio': 9, 'football': 9,
          'nature': 10, 'ambiente': 10, 'environment': 10,
          'business': 11, 'economia': 11, 'finance': 11,
          'health': 12, 'salute': 12, 'medical': 12,
          'politics': 13, 'politica': 13,
          'entertainment': 14, 'intrattenimento': 14
        };
        
        // Inizializza conteggi
        this.categoryCounts = {};
        // La chiave 0 rappresenta "Tutte" nel filtro.
        this.categoryCounts[0] = allArticles.length; // "Tutte"
        
        // Ottimizzazione: usa requestAnimationFrame per spezzare il lavoro e non bloccare UI
        // Il conteggio gira a blocchi da 50 articoli, uno per frame: il browser
        // resta responsivo mentre i conteggi si riempiono.
        const processInChunks = (articles: any[], categories: any[], chunkSize: number = 50) => {
          let articleIndex = 0;
          
          const processChunk = () => {
            const endIndex = Math.min(articleIndex + chunkSize, articles.length);
            
            // Processa chunk di articoli
            for (let i = articleIndex; i < endIndex; i++) {
              const article = articles[i];
              const articleCategoryId = article.category_id;
              
              // Incrementa conteggio per category_id diretto
              if (articleCategoryId) {
                if (!this.categoryCounts[articleCategoryId]) {
                  this.categoryCounts[articleCategoryId] = 0;
                }
                this.categoryCounts[articleCategoryId]++;
              } else {
                // Fallback: cerca nei keywords (solo se category_id mancante)
                const keywords = article.keywords || [];
                const matchedCategories = new Set<number>();
                
                for (const kw of keywords) {
                  const kwLower = String(kw).toLowerCase();
                  const mappedId = KEYWORD_TO_CATEGORY_ID[kwLower];
                  if (mappedId) {
                    matchedCategories.add(mappedId);
                  }
                }
                
                // Incrementa conteggi per categorie trovate
                matchedCategories.forEach(catId => {
                  if (!this.categoryCounts[catId]) {
                    this.categoryCounts[catId] = 0;
                  }
                  this.categoryCounts[catId]++;
                });
              }
            }
            
            articleIndex = endIndex;
            
            // Se ci sono ancora articoli da processare, continua nel prossimo frame
            if (articleIndex < articles.length) {
              requestAnimationFrame(processChunk);
            } else {
              // Inizializza a 0 le categorie senza articoli
              // Senza questa passata una categoria vuota resterebbe assente
              // dalla mappa e il filtro la mostrerebbe con un conteggio 'undefined'.
              categories.forEach(category => {
                if (!this.categoryCounts[category.id]) {
                  this.categoryCounts[category.id] = 0;
                }
              });
              
              console.log('✅ Conteggi categorie:', this.categoryCounts);
            }
          };
          
          // Inizia il processing
          requestAnimationFrame(processChunk);
        };
        
        // Avvia processing ottimizzato
        processInChunks(allArticles, this.categories);
      },
      error: (error) => {
        console.error('Error loading category counts:', error);
        // Inizializza conteggi a 0 in caso di errore
        this.categories.forEach(category => {
          this.categoryCounts[category.id] = 0;
        });
      }
    });
  }


  loadArticles(): void {
    this.loading = true;
    console.log('🔄 Loading articles...', { page: this.currentPage, size: this.pageSize, category: this.selectedCategoryId });
    
    // Log API URL per debug
    const apiUrl = (this.articleService as any).apiUrl || 'N/A';
    console.log('🌐 API URL:', apiUrl);
    
    // Filtro solo per categoria: gli altri filtri (ricerca, qualità) sono
    // applicati lato client su rawArticles.
    const filters = this.selectedCategoryId 
      ? { category_id: this.selectedCategoryId } 
      : {};

    this.articleService.getArticles(this.currentPage, this.pageSize, filters)
      .pipe(
        timeout(60000), // 60 secondi timeout per permettere wake-up Render
        catchError(error => {
          console.error('❌ Error loading articles:', error);
          console.error('❌ Error details:', {
            message: error?.message,
            status: error?.status,
            statusText: error?.statusText,
            url: error?.url,
            error: error?.error,
            name: error?.name
          });
          console.error('❌ Full error:', JSON.stringify(error, null, 2));
          
          // Salva errore per visualizzazione
          const errorDetails = {
            message: error?.message || 'N/A',
            status: error?.status || 'N/A',
            statusText: error?.statusText || 'N/A',
            url: error?.url || apiUrl,
            error: error?.error || 'N/A',
            name: error?.name || 'N/A',
            timestamp: new Date().toISOString()
          };
          
          const errorMsg = `Errore caricamento articoli:\n\n` +
            `Messaggio: ${errorDetails.message}\n` +
            `Status: ${errorDetails.status}\n` +
            `StatusText: ${errorDetails.statusText}\n` +
            `URL: ${errorDetails.url}\n` +
            `Error: ${JSON.stringify(errorDetails.error)}\n` +
            `Name: ${errorDetails.name}\n\n` +
            `Verifica:\n` +
            `1. Backend locale attivo?\n` +
            `2. Ngrok attivo?\n` +
            `3. Console per dettagli`;
          
          // Salva errore nel componente per visualizzazione
          this.lastError = JSON.stringify(errorDetails, null, 2);
          this.showError = true;
          
          // Salva anche nel localStorage per recupero
          try {
            localStorage.setItem('newsflow_last_error', JSON.stringify(errorDetails));
            localStorage.setItem('newsflow_last_error_text', errorMsg);
          } catch (e) {
            console.warn('Impossibile salvare errore in localStorage:', e);
          }
          
          this.snackBar.open(errorMsg, 'Chiudi', { duration: 8000, panelClass: ['error-snack'] });
          
          return of({
            items: [],
            total: 0,
            page: 1,
            size: 0,
            pages: 1
          });
        })
      )
      .subscribe({
        next: (response) => {
          console.log('✅ Articles loaded:', { count: response.items?.length || 0, total: response.total });
          console.log('✅ First article:', response.items?.[0]?.title || 'N/A');
          // La pagina grezza viene conservata: la ricerca client-side la filtra
          // senza dover richiedere nuovi dati al server.
          this.rawArticles = response.items || [];
          this.applyClientSearch();
          this.totalArticles = response.total || 0;
          this.loading = false;
          
          if (this.articles.length === 0) {
            console.warn('⚠️  ATTENZIONE: Nessun articolo caricato!');
            console.warn('⚠️  Response:', response);
          }
          
          // Riproduci messaggio vocale quando gli articoli vengono caricati per la prima volta
          // Solo quando non c'è una categoria selezionata (homepage principale)
          // Il messaggio di benvenuto introduce l'elenco generale: con un
          // filtro attivo sarebbe fuorviante.
          if (this.articles.length > 0 && !this.selectedCategoryId) {
            // Resetta il flag per permettere la riproduzione anche dopo refresh
            this.speechService.reset();
            // Aspetta un po' per permettere al browser di caricare le voci
            setTimeout(() => {
              console.log('🔊 Riproduzione messaggio vocale di benvenuto');
              this.speechService.speakWelcome();
            }, 500);
          }
          
          // Scroll agli articoli filtrati dopo che sono stati caricati (se c'è una categoria selezionata)
          if (this.selectedCategoryId !== null) {
            setTimeout(() => {
              this.scrollToFilteredArticles();
            }, 300); // Aspetta che il DOM sia aggiornato
          }
        },
        error: (error) => {
          console.error('❌ Subscribe error loading articles:', error);
          console.error('❌ Full error object:', JSON.stringify(error, null, 2));
          
          const errorDetails = {
            message: error?.message || 'Errore sconosciuto',
            status: error?.status || 'N/A',
            statusText: error?.statusText || 'N/A',
            url: error?.url || 'N/A',
            error: error?.error || 'N/A',
            name: error?.name || 'N/A',
            timestamp: new Date().toISOString()
          };
          
          // Salva errore
          this.lastError = JSON.stringify(errorDetails, null, 2);
          this.showError = true;
          
          try {
            localStorage.setItem('newsflow_last_error', JSON.stringify(errorDetails));
            localStorage.setItem('newsflow_last_error_text', `Errore subscribe: ${errorDetails.message}`);
          } catch (e) {
            console.warn('Impossibile salvare errore:', e);
          }
          
          this.articles = [];
          this.totalArticles = 0;
          this.loading = false;
          this.snackBar.open(`Errore subscribe: ${errorDetails.message}`, 'Chiudi', { duration: 8000 });
        }
      });
  }

  onSearchInput(query: string): void {
    this.searchQuery = query;
    this.applyClientSearch();
  }

  clearSearch(): void {
    this.searchQuery = '';
    this.applyClientSearch();
  }

  applyClientSearch(): void {
    const q = (this.searchQuery || '').trim().toLowerCase();
    if (!q) {
      this.articles = [...this.rawArticles];
      return;
    }
    this.articles = this.rawArticles.filter(article => {
      const titleMatch = article.title?.toLowerCase().includes(q) || false;
      const summaryMatch = article.summary?.toLowerCase().includes(q) || false;
      const authorMatch = article.author?.toLowerCase().includes(q) || false;
      const keywordsMatch = article.keywords?.some(k => k.toLowerCase().includes(q)) || false;
      return titleMatch || summaryMatch || authorMatch || keywordsMatch;
    });
  }

  onCategoryChange(categoryId: number | null): void {
    this.router.navigate([], {
      queryParams: { category: categoryId },
      queryParamsHandling: 'merge'
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.loadArticles();
    this.scrollToFilteredArticles();
  }

  scrollToFilteredArticles(): void {
    // Cerca l'elemento degli articoli filtrati con retry multipli
    let attempts = 0;
    const maxAttempts = 5;
    
    const tryScroll = () => {
      attempts++;
      const element = document.getElementById('articoli-filtrati');
      
      if (element) {
        const headerOffset = 80; // Offset per l'header fisso
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        console.log('📍 Scrolling to filtered articles:', { offsetPosition, elementPosition, scrollY: window.pageYOffset });
        
        // Scroll fluido agli articoli filtrati
        window.scrollTo({
          top: Math.max(0, offsetPosition), // Assicura che non vada in negativo
          behavior: 'smooth'
        });
      } else if (attempts < maxAttempts) {
        // Retry se l'elemento non è ancora disponibile
        console.log(`⏳ Retry scroll (attempt ${attempts}/${maxAttempts})...`);
        setTimeout(tryScroll, 200);
      } else {
        console.warn('⚠️ Elemento articoli-filtrati non trovato dopo', maxAttempts, 'tentativi');
      }
    };
    
    tryScroll();
  }

  copyError(): void {
    if (!this.lastError) return;
    
    const errorText = this.lastError; // TypeScript sa che non è null qui
    
    // Prova a copiare nel clipboard
    navigator.clipboard.writeText(errorText).then(() => {
      alert('✅ Errore copiato negli appunti!\n\nPuoi incollarlo dove vuoi.');
      console.log('✅ Errore copiato:', errorText);
    }).catch(err => {
      // Fallback: mostra in un textarea selezionabile
      const textarea = document.createElement('textarea');
      textarea.value = errorText;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        alert('✅ Errore copiato!');
      } catch (e) {
        alert('⚠️ Copia manuale:\n\nSeleziona il testo sopra e premi Ctrl+C');
      }
      document.body.removeChild(textarea);
    });
  }
}


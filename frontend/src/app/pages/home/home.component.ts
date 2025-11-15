import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { CategoryService } from '../../services/category.service';
import { SpeechService } from '../../services/speech.service';
import { ScrollPositionService } from '../../services/scroll-position.service';
import { Article } from '../../models/article.model';
import { Category } from '../../models/category.model';
import { PageEvent } from '@angular/material/paginator';
import { timeout, catchError, filter } from 'rxjs/operators';
import { of, Subscription } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  articles: Article[] = [];
  categories: Category[] = [];
  categoryCounts: { [categoryId: number]: number } = {}; // Conteggio articoli per categoria
  loading = false;
  selectedCategoryId: number | null = null;
  private routerSubscription?: Subscription;
  
  // Pagination
  totalArticles = 0;
  pageSize = 50; // Aumentato per mostrare più articoli per pagina
  currentPage = 1;
  
  // Error display
  lastError: string | null = null;
  showError = false;

  constructor(
    private articleService: ArticleService,
    private categoryService: CategoryService,
    private speechService: SpeechService,
    private scrollPositionService: ScrollPositionService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log('🏠 HomeComponent initialized');
    try {
      this.loadCategories();
      
      // Ascolta navigazione per ripristinare scroll quando si torna dalla pagina articolo
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
      this.route.queryParams.subscribe(params => {
        console.log('📋 Query params changed:', params);
        const previousCategoryId = this.selectedCategoryId;
        const isFirstLoad = this.selectedCategoryId === null && previousCategoryId === null;
        this.selectedCategoryId = params['category'] ? +params['category'] : null;
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
    this.articleService.getArticles(1, 1000, {}).subscribe({
      next: (response) => {
        const allArticles = response.items || [];
        
        // Mappa keywords → category_id (come nel backend) - ottimizzata per lookup veloce
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
        this.categoryCounts[0] = allArticles.length; // "Tutte"
        
        // Ottimizzazione: usa requestAnimationFrame per spezzare il lavoro e non bloccare UI
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
          
          alert(errorMsg);
          
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
          this.articles = response.items || [];
          this.totalArticles = response.total || 0;
          this.loading = false;
          
          if (this.articles.length === 0) {
            console.warn('⚠️  ATTENZIONE: Nessun articolo caricato!');
            console.warn('⚠️  Response:', response);
          }
          
          // Riproduci messaggio vocale quando gli articoli vengono caricati per la prima volta
          // Solo quando non c'è una categoria selezionata (homepage principale)
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
          alert(`Errore subscribe: ${errorDetails.message}\n\nErrore salvato! Clicca sul pulsante "Mostra Errore" in basso per copiarlo.`);
        }
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


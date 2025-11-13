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
  pageSize = 20;
  currentPage = 1;

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
    // Carica tutti gli articoli per contare quelli per categoria
    this.articleService.getArticles(1, 1000, {}).subscribe({
      next: (response) => {
        const allArticles = response.items || [];
        
        // Mappa keywords → category_id (come nel backend)
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
        
        // Conta articoli per categoria usando category_id o keywords come fallback
        this.categories.forEach(category => {
          const count = allArticles.filter(article => {
            // Prima prova con category_id
            if (article.category_id === category.id) {
              return true;
            }
            
            // Fallback: cerca nei keywords
            const keywords = article.keywords || [];
            for (const kw of keywords) {
              const kwLower = String(kw).toLowerCase();
              const mappedId = KEYWORD_TO_CATEGORY_ID[kwLower];
              if (mappedId === category.id) {
                return true;
              }
              // Cerca anche parziali
              for (const [key, catId] of Object.entries(KEYWORD_TO_CATEGORY_ID)) {
                if (key.includes(kwLower) || kwLower.includes(key)) {
                  if (catId === category.id) {
                    return true;
                  }
                }
              }
            }
            return false;
          }).length;
          
          this.categoryCounts[category.id] = count;
        });
        
        console.log('✅ Conteggi categorie:', this.categoryCounts);
      },
      error: (error) => {
        console.error('Error loading category counts:', error);
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
          
          // Alert visibile per debug
          const errorMsg = `Errore caricamento articoli:\n\n` +
            `Messaggio: ${error?.message || 'N/A'}\n` +
            `Status: ${error?.status || 'N/A'}\n` +
            `URL: ${error?.url || apiUrl}\n\n` +
            `Verifica:\n` +
            `1. Backend locale attivo?\n` +
            `2. Ngrok attivo?\n` +
            `3. Console per dettagli`;
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
          this.articles = [];
          this.totalArticles = 0;
          this.loading = false;
          alert(`Errore subscribe: ${error?.message || 'Errore sconosciuto'}\n\nControlla la console per dettagli.`);
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
}


import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SeoService } from '../../services/seo.service';
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
    private snackBar: MatSnackBar,
    private seoService: SeoService
  ) {}

  ngOnInit(): void {
    this.seoService.resetToHomepage();
    try {
      this.loadCategories();
      
      this.routerSubscription = this.router.events
        .pipe(filter(event => event instanceof NavigationEnd))
        .subscribe((event: any) => {
          if (event.url === '/' || event.urlAfterRedirects === '/') {
            setTimeout(() => {
              this.scrollPositionService.restoreScrollPosition('home');
            }, 50);
          }
        });
      
      this.route.queryParams.subscribe(params => {
        const previousCategoryId = this.selectedCategoryId;
        this.selectedCategoryId = params['category'] ? +params['category'] : null;
        this.currentPage = 1;
        this.loadArticles();
        
        if (this.selectedCategoryId !== null && previousCategoryId !== this.selectedCategoryId) {
          setTimeout(() => {
            this.scrollToFilteredArticles();
          }, 500);
        }
      });
    } catch (error) {
      // Silently fail
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
    this.articleService.getArticles(1, 500, {}).subscribe({
      next: (response) => {
        const allArticles = response.items || [];
        
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
        
        this.categoryCounts = {};
        this.categoryCounts[0] = allArticles.length;
        
        const processInChunks = (articles: any[], categories: any[], chunkSize: number = 30) => {
          let articleIndex = 0;
          
          const processChunk = () => {
            const endIndex = Math.min(articleIndex + chunkSize, articles.length);
            
            for (let i = articleIndex; i < endIndex; i++) {
              const article = articles[i];
              const articleCategoryId = article.category_id;
              
              if (articleCategoryId) {
                if (!this.categoryCounts[articleCategoryId]) {
                  this.categoryCounts[articleCategoryId] = 0;
                }
                this.categoryCounts[articleCategoryId]++;
              } else {
                const keywords = article.keywords || [];
                const matchedCategories = new Set<number>();
                
                for (const kw of keywords) {
                  const kwLower = String(kw).toLowerCase();
                  const mappedId = KEYWORD_TO_CATEGORY_ID[kwLower];
                  if (mappedId) {
                    matchedCategories.add(mappedId);
                  }
                }
                
                matchedCategories.forEach(catId => {
                  if (!this.categoryCounts[catId]) {
                    this.categoryCounts[catId] = 0;
                  }
                  this.categoryCounts[catId]++;
                });
              }
            }
            
            articleIndex = endIndex;
            
            if (articleIndex < articles.length) {
              requestAnimationFrame(processChunk);
            } else {
              categories.forEach(category => {
                if (!this.categoryCounts[category.id]) {
                  this.categoryCounts[category.id] = 0;
                }
              });
            }
          };
          
          requestAnimationFrame(processChunk);
        };
        
        processInChunks(allArticles, this.categories);
      },
      error: (error) => {
        this.categories.forEach(category => {
          this.categoryCounts[category.id] = 0;
        });
      }
    });
  }


  loadArticles(): void {
    this.loading = true;
    
    const filters = this.selectedCategoryId 
      ? { category_id: this.selectedCategoryId } 
      : {};

    this.articleService.getArticles(this.currentPage, this.pageSize, filters)
      .pipe(
        timeout(60000),
        catchError(error => {
          this.lastError = JSON.stringify({
            message: error?.message || 'N/A',
            status: error?.status || 'N/A',
            statusText: error?.statusText || 'N/A',
            url: error?.url || '',
            error: error?.error || 'N/A',
            name: error?.name || 'N/A',
            timestamp: new Date().toISOString()
          }, null, 2);
          this.showError = true;
          
          try {
            localStorage.setItem('newsflow_last_error', this.lastError);
          } catch (e) {}
          
          this.snackBar.open('Errore caricamento articoli', 'Chiudi', { duration: 5000, panelClass: ['error-snack'] });
          
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
          this.rawArticles = response.items || [];
          this.applyClientSearch();
          this.totalArticles = response.total || 0;
          this.loading = false;
          
          if (this.articles.length > 0 && !this.selectedCategoryId) {
            this.speechService.reset();
            setTimeout(() => {
              this.speechService.speakWelcome();
            }, 300);
          }
          
          if (this.selectedCategoryId !== null) {
            setTimeout(() => {
              this.scrollToFilteredArticles();
            }, 200);
          }
        },
        error: (error) => {
          this.articles = [];
          this.totalArticles = 0;
          this.loading = false;
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
    this.scrollPositionService.scrollToElement('articoli-filtrati', 80);
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


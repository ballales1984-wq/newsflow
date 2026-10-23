import { Component, OnInit, Output, EventEmitter, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { ArticleService } from '../../services/article.service';
import { AnalyticsService } from '../../services/analytics.service';
import { Category } from '../../models/category.model';

/**
 * Sidebar con l'elenco delle categorie e i relativi contatori.
 * La lista delle categorie arriva dal backend (CategoryService), mentre i
 * contatori sono calcolati qui con più chiamate all'elenco articoli.
 */
@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  @Output() linkClicked = new EventEmitter<void>();
  categories: Category[] = [];
  selectedCategoryId: number | null = null;
  categoryCounts: { [key: number]: number } = {};
  totalArticles: number = 0;
  isMobile = false;

  constructor(
    private categoryService: CategoryService,
    private articleService: ArticleService,
    private analytics: AnalyticsService,
    private router: Router
  ) {}

  @HostListener('window:resize', ['$event'])
  onResize() {
    // Soglia 768px: sotto questo valore la sidebar diventa un drawer,
    // quindi il menu va chiuso al tap su una voce.
    this.isMobile = window.innerWidth < 768;
  }

  ngOnInit(): void {
    // La larghezza va letta subito: al primo render la sidebar potrebbe
    // risultare già "desktop" se il resize non viene innescato.
    this.isMobile = window.innerWidth < 768;
    this.loadCategories();
    this.loadArticleCounts();
  }

  loadCategories(): void {
    this.categoryService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (error) => {
        // Senza categorie la sidebar resta vuota: l'errore viene solo loggato,
        // la navigazione principale resta comunque disponibile.
        console.error('Error loading categories:', error);
      }
    });
  }

  loadArticleCounts(): void {
    this.categoryService.getCategoryCounts().subscribe({
      next: (counts) => {
        const parsed: { [key: number]: number } = {};
        let total = 0;
        Object.keys(counts).forEach((key) => {
          const id = Number(key);
          const count = counts[key] || 0;
          parsed[id] = count;
          total += count;
        });
        this.categoryCounts = parsed;
        this.totalArticles = total;
      },
      error: (error) => {
        console.error('Error loading category counts:', error);
      }
    });
  }

  selectCategory(categoryId: number | null): void {
    // La categoria attiva viene tenuta in campo per evidenziare la voce
    // di menu; la fonte di verità restituita dal reload è però la query
    // param dell'URL.
    this.selectedCategoryId = categoryId;
    
    // Track category filter
    const categoryName = categoryId 
      ? this.categories.find(c => c.id === categoryId)?.name || 'Unknown'
      : 'All';
    this.analytics.trackCategoryFilter(categoryName);
    
    // Chiudi sidebar immediatamente (sia mobile che desktop)
    this.linkClicked.emit();
    
    // La navigazione passa il filtro nell'URL: la home lo rileva nei query
    // params e ricarica gli articoli, così il filtro è condivisibile e
    // sopravvive a un refresh.
    if (categoryId) {
      this.router.navigate(['/'], { queryParams: { category: categoryId } });
    } else {
      this.router.navigate(['/']);
    }
    
    // Scroll automatico agli articoli filtrati dopo navigazione e caricamento
    // Aspetta più tempo per assicurarsi che gli articoli siano caricati
    setTimeout(() => {
      this.scrollToFilteredArticles();
    }, 800); // Aumentato a 800ms per dare tempo agli articoli di caricarsi
  }

  scrollToFilteredArticles(): void {
    // Cerca l'elemento degli articoli filtrati con retry multipli
    // L'elemento esiste solo dopo il render della lista filtrata: si ritenta
    // fino a 5 volte (ogni 200ms) prima di rinunciare.
    let attempts = 0;
    const maxAttempts = 5;
    
    const tryScroll = () => {
      attempts++;
      const element = document.getElementById('articoli-filtrati');
      
      if (element) {
        const headerOffset = 80; // Offset per l'header fisso
        // L'header è fisso in alto: senza questo scarto il primo articolo
        // finirebbe sotto la barra di navigazione.
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        console.log('📍 Scrolling to filtered articles:', { offsetPosition, elementPosition });
        
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

  onLinkClick(): void {
    // Su mobile la sidebar è un drawer: va richiusa a ogni link seguito.
    if (this.isMobile) {
      this.linkClicked.emit();
    }
  }

  getCategoryCount(categoryId: number): number {
    // 0 quando il conteggio non è ancora arrivato: preferibile mostrare 0
    // piuttosto che nascondere la voce di menu.
    return this.categoryCounts[categoryId] || 0;
  }
}


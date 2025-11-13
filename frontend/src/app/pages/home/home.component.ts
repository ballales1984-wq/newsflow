import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { CategoryService } from '../../services/category.service';
import { SpeechService } from '../../services/speech.service';
import { Article } from '../../models/article.model';
import { Category } from '../../models/category.model';
import { PageEvent } from '@angular/material/paginator';
import { timeout, catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  articles: Article[] = [];
  categories: Category[] = [];
  loading = false;
  selectedCategoryId: number | null = null;
  
  // Pagination
  totalArticles = 0;
  pageSize = 20;
  currentPage = 1;

  constructor(
    private articleService: ArticleService,
    private categoryService: CategoryService,
    private speechService: SpeechService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log('🏠 HomeComponent initialized');
    try {
      this.loadCategories();
      
      // Load articles immediately on init and listen to query params changes
      this.route.queryParams.subscribe(params => {
        console.log('📋 Query params changed:', params);
        const previousCategoryId = this.selectedCategoryId;
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

  loadCategories(): void {
    this.categoryService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (error) => {
        console.error('Error loading categories:', error);
      }
    });
  }


  loadArticles(): void {
    this.loading = true;
    console.log('🔄 Loading articles...', { page: this.currentPage, size: this.pageSize, category: this.selectedCategoryId });
    
    const filters = this.selectedCategoryId 
      ? { category_id: this.selectedCategoryId } 
      : {};

    this.articleService.getArticles(this.currentPage, this.pageSize, filters)
      .pipe(
        timeout(60000), // 60 secondi timeout per permettere wake-up Render
        catchError(error => {
          console.error('❌ Error loading articles:', error);
          console.error('Error details:', {
            message: error?.message,
            status: error?.status,
            url: error?.url
          });
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
          this.articles = response.items || [];
          this.totalArticles = response.total || 0;
          this.loading = false;
          
          // Riproduci messaggio vocale quando gli articoli vengono caricati per la prima volta
          if (this.articles.length > 0 && !this.selectedCategoryId) {
            // Aspetta un po' per permettere al browser di caricare le voci
            setTimeout(() => {
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
          this.articles = [];
          this.totalArticles = 0;
          this.loading = false;
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


import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { CategoryService } from '../../services/category.service';
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
  featuredArticles: Article[] = [];
  loading = false;
  selectedCategoryId: number | null = null;
  
  // Pagination
  totalArticles = 0;
  pageSize = 20;
  currentPage = 1;

  constructor(
    private articleService: ArticleService,
    private categoryService: CategoryService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log('🏠 HomeComponent initialized');
    try {
      this.loadCategories();
      this.loadFeaturedArticles();
      
      // Load articles immediately on init and listen to query params changes
      this.route.queryParams.subscribe(params => {
        console.log('📋 Query params changed:', params);
        const previousCategoryId = this.selectedCategoryId;
        this.selectedCategoryId = params['category'] ? +params['category'] : null;
        this.currentPage = 1;
        this.loadArticles();
        
        // Scroll to filtered articles section when category changes
        if (this.selectedCategoryId !== null && previousCategoryId !== this.selectedCategoryId) {
          setTimeout(() => {
            this.scrollToFilteredArticles();
          }, 300);
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

  loadFeaturedArticles(): void {
    this.articleService.getFeaturedArticles(5).subscribe({
      next: (articles) => {
        this.featuredArticles = articles;
      },
      error: (error) => {
        console.error('Error loading featured articles:', error);
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
    const element = document.getElementById('articoli-filtrati');
    if (element) {
      const headerOffset = 80; // Offset per l'header fisso
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  }
}


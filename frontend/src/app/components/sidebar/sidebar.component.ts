import { Component, OnInit, Output, EventEmitter, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { ArticleService } from '../../services/article.service';
import { AnalyticsService } from '../../services/analytics.service';
import { Category } from '../../models/category.model';

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
    this.isMobile = window.innerWidth < 768;
  }

  ngOnInit(): void {
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
        console.error('Error loading categories:', error);
      }
    });
  }

  loadArticleCounts(): void {
    // Carica totale articoli
    this.articleService.getArticles(1, 1000).subscribe({
      next: (response) => {
        this.totalArticles = response.total;
      }
    });

    // Carica conteggi per ogni categoria (tutte le 14 categorie)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14].forEach(catId => {
      this.articleService.getArticles(1, 1000, { category_id: catId }).subscribe({
        next: (response) => {
          this.categoryCounts[catId] = response.total;
        }
      });
    });
  }

  selectCategory(categoryId: number | null): void {
    this.selectedCategoryId = categoryId;
    
    // Track category filter
    const categoryName = categoryId 
      ? this.categories.find(c => c.id === categoryId)?.name || 'Unknown'
      : 'All';
    this.analytics.trackCategoryFilter(categoryName);
    
    if (categoryId) {
      this.router.navigate(['/'], { queryParams: { category: categoryId } });
    } else {
      this.router.navigate(['/']);
    }
    
    // Chiudi drawer su mobile dopo la selezione
    if (this.isMobile) {
      this.linkClicked.emit();
    }
  }

  onLinkClick(): void {
    if (this.isMobile) {
      this.linkClicked.emit();
    }
  }

  getCategoryCount(categoryId: number): number {
    return this.categoryCounts[categoryId] || 0;
  }
}


import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CategoryService } from '../../services/category.service';
import { ArticleService } from '../../services/article.service';
import { Category } from '../../models/category.model';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  categories: Category[] = [];
  selectedCategoryId: number | null = null;
  categoryCounts: { [key: number]: number } = {};
  totalArticles: number = 0;

  constructor(
    private categoryService: CategoryService,
    private articleService: ArticleService,
    private router: Router
  ) {}

  ngOnInit(): void {
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

    // Carica conteggi per ogni categoria
    [1, 2, 3, 4, 5, 6, 7, 8].forEach(catId => {
      this.articleService.getArticles(1, 1000, { category_id: catId }).subscribe({
        next: (response) => {
          this.categoryCounts[catId] = response.total;
        }
      });
    });
  }

  selectCategory(categoryId: number | null): void {
    this.selectedCategoryId = categoryId;
    if (categoryId) {
      this.router.navigate(['/'], { queryParams: { category: categoryId } });
    } else {
      this.router.navigate(['/']);
    }
  }

  getCategoryCount(categoryId: number): number {
    return this.categoryCounts[categoryId] || 0;
  }
}


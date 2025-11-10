import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ArticleService } from '../../services/article.service';
import { CategoryService } from '../../services/category.service';
import { Article } from '../../models/article.model';
import { Category } from '../../models/category.model';
import { PageEvent } from '@angular/material/paginator';

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
    this.loadCategories();
    this.loadFeaturedArticles();
    
    // Listen to query params
    this.route.queryParams.subscribe(params => {
      this.selectedCategoryId = params['category'] ? +params['category'] : null;
      this.currentPage = 1;
      this.loadArticles();
    });
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
    
    const filters = this.selectedCategoryId 
      ? { category_id: this.selectedCategoryId } 
      : {};

    this.articleService.getArticles(this.currentPage, this.pageSize, filters).subscribe({
      next: (response) => {
        this.articles = response.items;
        this.totalArticles = response.total;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading articles:', error);
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
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}


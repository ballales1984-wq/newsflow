import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ArticleService } from '../../services/article.service';
import { CategoryService } from '../../services/category.service';
import { Article, ArticleSearch } from '../../models/article.model';
import { Category } from '../../models/category.model';
import { PageEvent } from '@angular/material/paginator';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  articles: Article[] = [];
  categories: Category[] = [];
  loading = false;
  searchForm: FormGroup;
  
  // Pagination
  totalArticles = 0;
  pageSize = 20;
  currentPage = 1;

  constructor(
    private articleService: ArticleService,
    private categoryService: CategoryService,
    private route: ActivatedRoute,
    private fb: FormBuilder
  ) {
    this.searchForm = this.fb.group({
      query: [''],
      category_id: [null],
      language: [''],
      min_quality_score: [null],
      date_from: [null]
    });
  }

  ngOnInit(): void {
    this.loadCategories();
    
    // Get initial query from URL
    this.route.queryParams.subscribe(params => {
      if (params['q']) {
        this.searchForm.patchValue({ query: params['q'] });
        this.search();
      }
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

  search(): void {
    this.loading = true;
    this.currentPage = 1;
    
    const searchParams: ArticleSearch = {
      ...this.searchForm.value
    };

    // Remove empty values
    Object.keys(searchParams).forEach(key => {
      if (searchParams[key as keyof ArticleSearch] === null || 
          searchParams[key as keyof ArticleSearch] === '') {
        delete searchParams[key as keyof ArticleSearch];
      }
    });

    this.articleService.searchArticles(searchParams, this.currentPage, this.pageSize).subscribe({
      next: (response) => {
        this.articles = response.items;
        this.totalArticles = response.total;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error searching articles:', error);
        this.loading = false;
      }
    });
  }

  onPageChange(event: PageEvent): void {
    this.currentPage = event.pageIndex + 1;
    this.pageSize = event.pageSize;
    this.search();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  reset(): void {
    this.searchForm.reset();
    this.articles = [];
    this.totalArticles = 0;
  }
}


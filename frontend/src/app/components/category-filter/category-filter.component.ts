import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import { Category } from '../../models/category.model';

@Component({
  selector: 'app-category-filter',
  templateUrl: './category-filter.component.html',
  styleUrls: ['./category-filter.component.scss']
})
export class CategoryFilterComponent {
  @Input() categories: Category[] = [];
  @Input() selectedCategoryId: number | null = null;
  @Input() categoryCounts: { [categoryId: number]: number } = {};
  @Input() totalArticles: number = 0;
  @Output() categoryChange = new EventEmitter<number | null>();

  constructor(private router: Router) {}

  selectCategory(categoryId: number | null): void {
    this.selectedCategoryId = categoryId;
    this.categoryChange.emit(categoryId);
  }

  goToDigest(): void {
    console.log('🔗 Navigazione alla pagina Digest...');
    this.router.navigate(['/digest']);
  }

  getCategoryCount(categoryId: number | null): number {
    if (categoryId === null) {
      return this.totalArticles || this.categoryCounts[0] || 0;
    }
    return this.categoryCounts[categoryId] || 0;
  }
}


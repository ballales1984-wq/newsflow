import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Category } from '../../models/category.model';

@Component({
  selector: 'app-category-filter',
  templateUrl: './category-filter.component.html',
  styleUrls: ['./category-filter.component.scss']
})
export class CategoryFilterComponent {
  @Input() categories: Category[] = [];
  @Input() selectedCategoryId: number | null = null;
  @Output() categoryChange = new EventEmitter<number | null>();

  selectCategory(categoryId: number | null): void {
    this.selectedCategoryId = categoryId;
    this.categoryChange.emit(categoryId);
  }
}


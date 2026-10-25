import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';
import { Category } from '../../models/category.model';

/**
 * Riga di chip per il filtro per categoria.
 * Il componente non carica nulla e non naviga da solo: si limita a segnalare la
 * scelta con categoryChange, così chi lo ospita (la home) resta proprietario
 * dello stato dei filtri e dell'URL.
 */
@Component({
  selector: 'app-category-filter',
  standalone: true,
  imports: [
    CommonModule,
    MatChipsModule,
    MatIconModule,
    RouterModule
  ],
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
    // Aggiorna subito la chip selezionata per dare un riscontro immediato,
    // poi notifica il padre che farà partire il ricaricamento.
    // null = "Tutte", cioè nessun filtro applicato.
    this.selectedCategoryId = categoryId;
    this.categoryChange.emit(categoryId);
  }

  goToDigest(): void {
    // Il chip "Digest" non è una categoria: porta alla pagina del riepilogo.
    console.log('🔗 Navigazione alla pagina Digest...');
    this.router.navigate(['/digest']);
  }

  getCategoryCount(categoryId: number | null): number {
    // Per "Tutte" si preferisce il totale restituito dall'API; i conteggi per
    // categoria arrivano invece dalla mappa, calcolata dal padre.
    if (categoryId === null) {
      return this.totalArticles || this.categoryCounts[0] || 0;
    }
    // 0 quando il conteggio non è ancora arrivato: mostrare 0 è preferibile a
    // nascondere la chip, che renderebbe il filtro irraggiungibile.
    return this.categoryCounts[categoryId] || 0;
  }
}


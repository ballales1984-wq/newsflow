import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ArticleCardComponent } from '../article-card/article-card.component';
import { AdBannerComponent } from '../ad-banner/ad-banner.component';
import { Article } from '../../models/article.model';

/**
 * Componente puramente presentazionale: riceve già gli articoli filtrati dal padre
 * e si occupa solo di mostrare spinner, stato vuoto o griglia.
 * Non conosce il backend, quindi può essere riusato da home, ricerca e salvati.
 */
@Component({
  selector: 'app-article-list',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    ArticleCardComponent,
    AdBannerComponent
  ],
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.scss']
})
export class ArticleListComponent implements OnInit {
  @Input() articles: Article[] = [];
  @Input() loading = false;

  ngOnInit(): void {
    // Log di diagnostica: utile per verificare al volo quante card sono arrivate
    // e se il padre era ancora in fase di caricamento.
    console.log('📰 ArticleListComponent initialized:', { 
      articlesCount: this.articles?.length || 0, 
      loading: this.loading 
    });
  }
}


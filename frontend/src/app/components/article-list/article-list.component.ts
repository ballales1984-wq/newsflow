import { Component, Input, OnInit } from '@angular/core';
import { Article } from '../../models/article.model';

/**
 * Componente puramente presentazionale: riceve già gli articoli filtrati dal padre
 * e si occupa solo di mostrare spinner, stato vuoto o griglia.
 * Non conosce il backend, quindi può essere riusato da home, ricerca e salvati.
 */
@Component({
  selector: 'app-article-list',
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


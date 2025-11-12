import { Component, Input, OnInit } from '@angular/core';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.scss']
})
export class ArticleListComponent implements OnInit {
  @Input() articles: Article[] = [];
  @Input() loading = false;

  ngOnInit(): void {
    console.log('📰 ArticleListComponent initialized:', { 
      articlesCount: this.articles?.length || 0, 
      loading: this.loading 
    });
  }
}


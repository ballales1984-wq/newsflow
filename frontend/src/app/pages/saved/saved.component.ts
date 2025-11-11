import { Component, OnInit } from '@angular/core';
import { ArticleService } from '../../services/article.service';
import { SavedArticleService } from '../../services/saved-article.service';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-saved',
  templateUrl: './saved.component.html',
  styleUrls: ['./saved.component.scss']
})
export class SavedComponent implements OnInit {
  savedArticles: Article[] = [];
  loading = true;

  constructor(
    private articleService: ArticleService,
    private savedArticleService: SavedArticleService
  ) {}

  ngOnInit(): void {
    this.loadSavedArticles();
  }

  loadSavedArticles(): void {
    this.loading = true;
    
    // Carica tutti gli articoli
    this.articleService.getArticles(1, 100).subscribe({
      next: (response) => {
        const savedIds = this.savedArticleService.getSavedArticles();
        this.savedArticles = response.items.filter(article => 
          savedIds.includes(article.id)
        );
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading saved articles:', error);
        this.loading = false;
      }
    });
  }
}


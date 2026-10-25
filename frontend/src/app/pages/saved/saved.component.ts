import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { SeoService } from '../../services/seo.service';
import { ArticleService } from '../../services/article.service';
import { SavedArticleService } from '../../services/saved-article.service';
import { Article } from '../../models/article.model';
import { ArticleListComponent } from '../../components/article-list/article-list.component';

@Component({
  selector: 'app-saved',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    ArticleListComponent
  ],
  templateUrl: './saved.component.html',
  styleUrls: ['./saved.component.scss']
})
export class SavedComponent implements OnInit {
  savedArticles: Article[] = [];
  loading = true;

  constructor(
    private articleService: ArticleService,
    private savedArticleService: SavedArticleService,
    private seoService: SeoService
  ) {}

  ngOnInit(): void {
    this.seoService.updateSavedSeo();
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


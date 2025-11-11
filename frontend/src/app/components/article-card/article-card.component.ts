import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Article } from '../../models/article.model';
import { SavedArticleService } from '../../services/saved-article.service';

@Component({
  selector: 'app-article-card',
  templateUrl: './article-card.component.html',
  styleUrls: ['./article-card.component.scss']
})
export class ArticleCardComponent {
  @Input() article!: Article;

  constructor(
    private router: Router,
    public savedArticleService: SavedArticleService
  ) {}

  viewArticle(): void {
    this.router.navigate(['/article', this.article.slug]);
  }

  saveArticle(event: Event): void {
    event.stopPropagation();
    if (this.isSaved()) {
      this.savedArticleService.unsaveArticle(this.article.id);
    } else {
      this.savedArticleService.saveArticle(this.article.id);
    }
  }

  shareArticle(event: Event): void {
    event.stopPropagation();
    if (navigator.share) {
      navigator.share({
        title: this.article.title,
        text: this.article.summary,
        url: this.article.url
      });
    } else {
      // Fallback: copia URL
      navigator.clipboard.writeText(this.article.url);
      alert('Link copiato negli appunti!');
    }
  }

  isSaved(): boolean {
    return this.savedArticleService.isSaved(this.article.id);
  }

  getQualityColor(score?: number): string {
    if (!score) return 'accent';
    if (score >= 0.8) return 'primary';
    if (score >= 0.6) return 'accent';
    return 'warn';
  }

  formatDate(date?: string): string {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('it-IT', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  }
}


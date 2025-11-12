import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { Article } from '../../models/article.model';
import { SavedArticleService } from '../../services/saved-article.service';
import { AnalyticsService } from '../../services/analytics.service';
import { ExplainDialogComponent } from '../explain-dialog/explain-dialog.component';

@Component({
  selector: 'app-article-card',
  templateUrl: './article-card.component.html',
  styleUrls: ['./article-card.component.scss']
})
export class ArticleCardComponent {
  @Input() article!: Article;

  constructor(
    private router: Router,
    public savedArticleService: SavedArticleService,
    private dialog: MatDialog,
    private analytics: AnalyticsService
  ) {}

  viewArticle(): void {
    // Usa setTimeout per non bloccare il thread principale
    setTimeout(() => {
      this.analytics.trackArticleView(this.article.id, this.article.title);
      this.router.navigate(['/article', this.article.slug]);
    }, 0);
  }

  saveArticle(event: Event): void {
    event.stopPropagation();
    // Usa setTimeout per non bloccare il thread principale
    setTimeout(() => {
      if (this.isSaved()) {
        this.savedArticleService.unsaveArticle(this.article.id);
      } else {
        this.savedArticleService.saveArticle(this.article.id);
        this.analytics.trackArticleSave(this.article.id, this.article.title);
      }
    }, 0);
  }

  shareArticle(event: Event): void {
    event.stopPropagation();
    this.analytics.trackArticleShare(this.article.id, this.article.title);
    
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

  explainArticle(event: Event): void {
    event.stopPropagation();
    
    // Track "Spiegami" click
    this.analytics.trackExplainClick(this.article.id, this.article.title);
    
    // Apre modal con spiegazione a 3 livelli!
    this.dialog.open(ExplainDialogComponent, {
      data: this.article,
      width: '900px',
      maxWidth: '95vw',
      maxHeight: '90vh'
    });
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


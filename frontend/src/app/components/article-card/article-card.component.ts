import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatBadgeModule } from '@angular/material/badge';
import { Article } from '../../models/article.model';
import { SavedArticleService } from '../../services/saved-article.service';
import { AnalyticsService } from '../../services/analytics.service';
import { ScrollPositionService } from '../../services/scroll-position.service';
import { ExplainDialogComponent } from '../explain-dialog/explain-dialog.component';
import { StripHtmlPipe } from '../../pipes/strip-html.pipe';

/**
 * Card di anteprima di un articolo: è il componente più riusato dell'app
 * (lista, ricerca, salvati), quindi non carica dati da solo — riceve l'articolo
 * come @Input e si appoggia solo a servizi di stato locale (salvati, analytics, scroll).
 */
@Component({
  selector: 'app-article-card',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatTooltipModule,
    MatBadgeModule,
    StripHtmlPipe
  ],
  templateUrl: './article-card.component.html',
  styleUrls: ['./article-card.component.scss']
})
export class ArticleCardComponent {
  @Input() article!: Article;

  constructor(
    private router: Router,
    public savedArticleService: SavedArticleService,
    private dialog: MatDialog,
    private analytics: AnalyticsService,
    private scrollPositionService: ScrollPositionService,
    private snackBar: MatSnackBar
  ) {}

  viewArticle(): void {
    this.scrollPositionService.saveScrollPosition('home');

    setTimeout(() => {
      this.analytics.trackArticleView(this.article.id, this.article.title);
      if (this.article.url) {
        window.open(this.article.url, '_blank');
      } else {
        this.router.navigate(['/article', this.article.slug]);
      }
    }, 0);
  }

  saveArticle(event: Event): void {
    event.stopPropagation();
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
      navigator.clipboard.writeText(this.article.url);
      this.snackBar.open('Link copiato negli appunti!', 'Chiudi', { duration: 3000 });
    }
  }

  isSaved(): boolean {
    return this.savedArticleService.isSaved(this.article.id);
  }

  explainArticle(event: Event): void {
    event.stopPropagation();
    this.analytics.trackExplainClick(this.article.id, this.article.title);

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

  getCategoryIcon(): string {
    const icons: { [id: number]: string } = {
      1: 'computer',
      2: 'science',
      3: 'psychology',
      4: 'security',
      5: 'smart_toy',
      6: 'lightbulb',
      7: 'palette',
      8: 'balance',
      9: 'sports_soccer',
      10: 'park',
      11: 'business_center',
      12: 'health_and_safety',
      13: 'gavel',
      14: 'movie'
    };
    return icons[this.article?.category_id || 1] || 'newspaper';
  }

  getCategoryName(): string {
    const names: { [id: number]: string } = {
      1: 'Tecnologia',
      2: 'Scienza',
      3: 'Filosofia',
      4: 'Cybersecurity',
      5: 'AI',
      6: 'Innovazione',
      7: 'Cultura',
      8: 'Etica',
      9: 'Sport',
      10: 'Ambiente',
      11: 'Business',
      12: 'Salute',
      13: 'Politica',
      14: 'Intrattenimento'
    };
    return names[this.article?.category_id || 1] || 'News';
  }
}

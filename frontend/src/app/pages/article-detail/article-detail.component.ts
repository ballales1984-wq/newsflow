import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { SeoService } from '../../services/seo.service';
import { ArticleService } from '../../services/article.service';
import { ScrollPositionService } from '../../services/scroll-position.service';
import { Article } from '../../models/article.model';
import { StripHtmlPipe } from '../../pipes/strip-html.pipe';

/**
 * Pagina di dettaglio dell'articolo, aperta dal route /article/:slug.
 * I dati arrivano da slug: il componente non riceve l'articolo via @Input
 * e quindi deve essere ricaricato a ogni cambio di parametro.
 */
@Component({
  selector: 'app-article-detail',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatChipsModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    StripHtmlPipe
  ],
  templateUrl: './article-detail.component.html',
  styleUrls: ['./article-detail.component.scss']
})
export class ArticleDetailComponent implements OnInit {
  article: Article | null = null;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private location: Location,
    private articleService: ArticleService,
    private scrollPositionService: ScrollPositionService,
    private snackBar: MatSnackBar,
    private seoService: SeoService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const slug = params['slug'];
      if (slug) {
        this.loadArticle(slug);
      }
    });
  }

  loadArticle(slug: string): void {
    this.loading = true;
    this.articleService.getArticleBySlug(slug).subscribe({
      next: (article) => {
        this.article = article;
        this.loading = false;
        this.seoService.updateArticleSeo(article);
      },
      error: (error) => {
        console.error('Error loading article:', error);
        this.loading = false;
        this.router.navigate(['/']);
      }
    });
  }

  goBack(): void {
    this.location.back();
    setTimeout(() => {
      if (this.router.url.includes('/article')) {
        this.router.navigate(['/']);
      }
    }, 100);
  }

  saveArticle(): void {
    if (this.article) {
      const saved = localStorage.getItem('savedArticles');
      const savedIds = saved ? JSON.parse(saved) : [];

      if (!savedIds.includes(this.article.id)) {
        savedIds.push(this.article.id);
        localStorage.setItem('savedArticles', JSON.stringify(savedIds));
        this.snackBar.open('Articolo salvato!', 'Chiudi', { duration: 3000 });
      } else {
        this.snackBar.open('Articolo già salvato!', 'Chiudi', { duration: 3000 });
      }
    }
  }

  shareArticle(): void {
    if (this.article) {
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
  }

  formatDate(date?: string): string {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('it-IT', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getContentParagraphs(content: string): string[] {
    if (!content) return [];
    return content
      .split(/\n\n+|\.\s+(?=[A-Z])/)
      .map(p => p.trim())
      .filter(p => p.length > 0);
  }
}

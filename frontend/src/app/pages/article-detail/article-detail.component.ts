import { Component, OnInit } from '@angular/core';
import { COMMONModule } from '@angular/common';
import { activatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { Snackbar } from '@angular/material/snack-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { matBTNModule } from '@angular/material/button';
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
    COMMONModule,
    MatIconModule,
    MatChipsModule,
    matBTNModule,
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
    private route: activatedRoute,
    private router: Router,
    private location: Location,
    private articleService: ArticleService,
    private scrollPositionService: ScrollPositionService,
    private snackbar: Snackbar,
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
        this.snackbar.open('Articolo salvato!', 'Chiudi', { duration: 3000 });
      } else {
        this.snackbar.open('Articolo già salvato!', 'Chiudi', { duration: 3000 });
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
        this.snackbar.open('Link copiato negli appunti!', 'Chiudi', { duration: 3000 });
      }
    }
  }

  shareOnFacebook(): void {
    if (this.article) {
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(this.article.url)}`, '_blank');
    }
  }

  shareOnTwitter(): void {
    if (this.article) {
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(this.article.title)}&url=${encodeURIComponent(this.article.url)}`, '_blank');
    }
  }

  shareOnLinkedIn(): void {
    if (this.article) {
      window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(this.article.url)}`, '_blank');
    }
  }

  shareOnWhatsApp(): void {
    if (this.article) {
      window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(this.article.title + ' ' + this.article.url)}`, '_blank');
    }
  }

  shareOnTelegram(): void {
    if (this.article) {
      window.open(`https://t.me/share/url?url=${encodeURIComponent(this.article.url)}&text=${encodeURIComponent(this.article.title)}`, '_blank');
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
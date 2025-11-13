import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Location } from '@angular/common';
import { ArticleService } from '../../services/article.service';
import { ScrollPositionService } from '../../services/scroll-position.service';
import { Article } from '../../models/article.model';

@Component({
  selector: 'app-article-detail',
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
    private scrollPositionService: ScrollPositionService
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
      },
      error: (error) => {
        console.error('Error loading article:', error);
        this.loading = false;
        this.router.navigate(['/']);
      }
    });
  }

  goBack(): void {
    // Usa location.back() per mantenere la storia del browser
    // Questo permette di ripristinare automaticamente la posizione scroll
    this.location.back();
    
    // Fallback: se location.back() non funziona, naviga alla home
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
        alert('Articolo salvato!');
      } else {
        alert('Articolo già salvato!');
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
        alert('Link copiato negli appunti!');
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
    // Divide il contenuto in paragrafi (per doppio a capo o punti)
    return content
      .split(/\n\n+|\.\s+(?=[A-Z])/)
      .map(p => p.trim())
      .filter(p => p.length > 0);
  }
}


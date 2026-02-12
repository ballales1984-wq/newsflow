import { Injectable } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';
import { Article } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class SeoService {
  private baseUrl = 'https://newsflow-orcin.vercel.app';

  constructor(
    private meta: Meta,
    private title: Title
  ) {}

  /**
   * Aggiorna meta tag e structured data per un articolo
   */
  updateArticleSeo(article: Article): void {
    if (!article) return;

    const articleUrl = `${this.baseUrl}/article/${article.slug || article.id}`;
    const imageUrl = article.image_url
      ? (article.image_url.startsWith('http') ? article.image_url : `${this.baseUrl}${article.image_url}`)
      : `${this.baseUrl}/assets/icons/icon-512x512.png`;

    // Title
    this.title.setTitle(`${article.title} | NewsFlow`);

    // Meta Description
    const description = article.summary || article.content?.substring(0, 160) || 'Leggi l\'articolo completo su NewsFlow';
    this.meta.updateTag({ name: 'description', content: description });

    // Keywords
    if (article.keywords && article.keywords.length > 0) {
      this.meta.updateTag({ name: 'keywords', content: article.keywords.join(', ') });
    }

    // Canonical URL
    this.meta.updateTag({ rel: 'canonical', href: articleUrl });

    // Open Graph
    this.meta.updateTag({ property: 'og:type', content: 'article' });
    this.meta.updateTag({ property: 'og:url', content: articleUrl });
    this.meta.updateTag({ property: 'og:title', content: article.title });
    this.meta.updateTag({ property: 'og:description', content: description });
    this.meta.updateTag({ property: 'og:image', content: imageUrl });
    this.meta.updateTag({ property: 'og:locale', content: 'it_IT' });
    this.meta.updateTag({ property: 'og:site_name', content: 'NewsFlow' });

    if (article.published_at) {
      this.meta.updateTag({ property: 'article:published_time', content: new Date(article.published_at).toISOString() });
    }
    if (article.author) {
      this.meta.updateTag({ property: 'article:author', content: article.author });
    }
    if (article.category_id) {
      this.meta.updateTag({ property: 'article:section', content: `Categoria ${article.category_id}` });
    }

    // Twitter Card
    this.meta.updateTag({ property: 'twitter:card', content: 'summary_large_image' });
    this.meta.updateTag({ property: 'twitter:url', content: articleUrl });
    this.meta.updateTag({ property: 'twitter:title', content: article.title });
    this.meta.updateTag({ property: 'twitter:description', content: description });
    this.meta.updateTag({ property: 'twitter:image', content: imageUrl });

    // Structured Data (JSON-LD)
    this.addStructuredData(article, articleUrl, imageUrl);
  }

  /**
   * Aggiunge structured data JSON-LD per l'articolo
   */
  private addStructuredData(article: Article, articleUrl: string, imageUrl: string): void {
    // Rimuovi structured data esistente
    const existingScript = document.getElementById('article-structured-data');
    if (existingScript) {
      existingScript.remove();
    }

    const structuredData = {
      '@context': 'https://schema.org',
      '@type': 'NewsArticle',
      'headline': article.title,
      'description': article.summary || article.content?.substring(0, 200) || '',
      'image': imageUrl,
      'datePublished': article.published_at ? new Date(article.published_at).toISOString() : new Date(article.collected_at).toISOString(),
      'dateModified': new Date(article.collected_at).toISOString(),
      'author': {
        '@type': 'Organization',
        'name': article.author || 'NewsFlow',
        'url': this.baseUrl
      },
      'publisher': {
        '@type': 'Organization',
        'name': 'NewsFlow',
        'logo': {
          '@type': 'ImageObject',
          'url': `${this.baseUrl}/assets/icons/icon-512x512.png`
        }
      },
      'mainEntityOfPage': {
        '@type': 'WebPage',
        '@id': articleUrl
      },
      'url': articleUrl,
      'articleSection': article.category_id ? `Categoria ${article.category_id}` : 'Notizie',
      'keywords': article.keywords?.join(', ') || '',
      'inLanguage': article.language || 'it'
    };

    // Aggiungi articleBody se disponibile
    if (article.content) {
      structuredData['articleBody'] = article.content;
    }

    // Crea script tag con JSON-LD
    const script = document.createElement('script');
    script.id = 'article-structured-data';
    script.type = 'application/ld+json';
    script.text = JSON.stringify(structuredData);
    document.head.appendChild(script);
  }

  /**
   * Resetta meta tag alla homepage
   */
  resetToHomepage(): void {
    this.title.setTitle('NewsFlow - Notizie Italiane Aggiornate | Piattaforma Intelligente di Curazione News');
    this.meta.updateTag({ name: 'description', content: 'NewsFlow - Piattaforma intelligente per la curazione di notizie italiane. Aggiornamenti in tempo reale, spiegazioni AI, categorie organizzate e molto altro.' });
    this.meta.updateTag({ property: 'og:type', content: 'website' });
    this.meta.updateTag({ property: 'og:url', content: this.baseUrl });
    this.meta.updateTag({ property: 'og:title', content: 'NewsFlow - Notizie Italiane Aggiornate' });
    this.meta.updateTag({ property: 'og:description', content: 'Piattaforma intelligente per la curazione di notizie italiane. Aggiornamenti in tempo reale, spiegazioni AI e categorie organizzate.' });
    this.meta.updateTag({ property: 'og:image', content: `${this.baseUrl}/assets/icons/icon-512x512.png` });

    // Rimuovi structured data articolo
    const existingScript = document.getElementById('article-structured-data');
    if (existingScript) {
      existingScript.remove();
    }
  }
}


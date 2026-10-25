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
    // Salva la posizione di scroll prima di navigare
    // La chiave 'home' è quella che la home ripristina al ritorno:
    // senza questo salvataggio il ritorno ripartirebbe dall'inizio della pagina.
    this.scrollPositionService.saveScrollPosition('home');

    // Usa setTimeout per non bloccare il thread principale
    // Il click è seguito dall'apertura di una nuova scheda: differendo il lavoro
    // si evita di ritardare l'evento di navigazione e la risposta visiva al click.
    setTimeout(() => {
      this.analytics.trackArticleView(this.article.id, this.article.title);
      // Apri l'URL originale in una nuova scheda
      // Priorità alla fonte originale: la card è un rinvio, l'articolo si legge sul sito di origine.
      if (this.article.url) {
        window.open(this.article.url, '_blank');
      } else {
        // Fallback alla pagina interna se non c'è URL
        this.router.navigate(['/article', this.article.slug]);
      }
    }, 0);
  }

  saveArticle(event: Event): void {
    // stopPropagation: senza, il click sul bottone salirebbe alla card
    // e aprirebbe anche l'articolo originale.
    event.stopPropagation();
    // Usa setTimeout per non bloccare il thread principale
    setTimeout(() => {
      // Il servizio salva gli id in localStorage e notifica savedArticles$,
      // così il badge dei salvati nell'header si aggiorna da solo.
      if (this.isSaved()) {
        this.savedArticleService.unsaveArticle(this.article.id);
      } else {
        this.savedArticleService.saveArticle(this.article.id);
        this.analytics.trackArticleSave(this.article.id, this.article.title);
      }
    }, 0);
  }

  shareArticle(event: Event): void {
    // Come per il salvataggio: va fermata la propagazione verso la card.
    event.stopPropagation();
    this.analytics.trackArticleShare(this.article.id, this.article.title);

    const url = this.article.url || window.location.origin + '/article/' + this.article.slug;
    const title = this.article.title;
    const text = this.article.summary || title;

    if (navigator.share) {
      // Web Share API: mobile/desktop la mostrano nativamente, senza UI custom.
      navigator.share({
        title: title,
        text: text,
        url: url
      }).catch(() => {
        // Fallback se l'utente annulla o c'è un errore
        this.openShareMenu(url, title, text);
      });
    } else {
      this.openShareMenu(url, title, text);
    }
  }

  private openShareMenu(url: string, title: string, text: string): void {
    const encodedUrl = encodeURIComponent(url);
    const encodedTitle = encodeURIComponent(title);
    const encodedText = encodeURIComponent(text);

    const shareOptions = [
      { name: 'Facebook', url: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}` },
      { name: 'Twitter', url: `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}` },
      { name: 'LinkedIn', url: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}` },
      { name: 'WhatsApp', url: `https://wa.me/?text=${encodedTitle}%20${encodedUrl}` },
      { name: 'Telegram', url: `https://t.me/share/url?url=${encodedUrl}&text=${encodedTitle}` },
      { name: 'Copia link', action: 'copy' }
    ];

    const choice = prompt(
      'Condividi su:\n' +
      '1. Facebook\n' +
      '2. Twitter/X\n' +
      '3. LinkedIn\n' +
      '4. WhatsApp\n' +
      '5. Telegram\n' +
      '6. Copia link\n\n' +
      'Inserisci il numero (1-6):'
    );

    if (!choice) return;

    const index = parseInt(choice) - 1;
    if (index >= 0 && index < shareOptions.length) {
      const option = shareOptions[index];
      if (option.action === 'copy') {
        navigator.clipboard.writeText(url);
        alert('Link copiato negli appunti!');
      } else if (option.url) {
        window.open(option.url, '_blank', 'width=600,height=400');
      }
    }
  }
  }

  isSaved(): boolean {
    // Lettura dallo stato in memoria del servizio: riflette subito i salvataggi
    // fatti da altre card senza dover rileggere il localStorage.
    return this.savedArticleService.isSaved(this.article.id);
  }

  explainArticle(event: Event): void {
    event.stopPropagation();

    // Track "Spiegami" click
    this.analytics.trackExplainClick(this.article.id, this.article.title);

    // Apre modal con spiegazione a 3 livelli!
    // L'articolo completo viene passato come dati del dialog: il dialog è così
    // autosufficiente e non deve rifare la fetch dell'articolo.
    this.dialog.open(ExplainDialogComponent, {
      data: this.article,
      width: '900px',
      maxWidth: '95vw',
      maxHeight: '90vh'
    });
  }

  getQualityColor(score?: number): string {
    // Soglie del quality score (0..1) tradotte nei colori Material del chip:
    // il colore dà il giudizio di qualità senza dover leggere la percentuale.
    if (!score) return 'accent';
    if (score >= 0.8) return 'primary';
    if (score >= 0.6) return 'accent';
    return 'warn';
  }

  formatDate(date?: string): string {
    // Data assente: si restituisce stringa vuota così il template può omettere
    // il separatore senza mostrare "Invalid Date".
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('it-IT', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  }

  getCategoryIcon(): string {
    // Mappa category_id -> icona Material, usata dal banner di fallback
    // quando l'articolo non ha immagine (vedi template).
    // Le chiavi devono restare allineate alle 14 categorie del backend.
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
    // Fallback generico: id sconosciuto o articolo senza categoria.
    return icons[this.article?.category_id || 1] || 'newspaper';
  }

  getCategoryName(): string {
    // Stesse chiavi di getCategoryIcon(): etichetta italiana della categoria,
    // mostrata nella pill del banner di fallback.
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


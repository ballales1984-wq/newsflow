import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, Subscription } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

interface DigestArticle {
  title: string;
  description: string;
}

interface DigestCategory {
  category: string;
  articles: DigestArticle[];
}

interface DailyDigest {
  date: string;
  digest: DigestCategory[];
}

/**
 * Pagina del riepilogo giornaliero ("Digest"): mostra i titoli e le descrizioni
 * delle notizie raggruppate per categoria.
 * I dati vengono dal backend con un fallback su file JSON statico, così la
 * pagina resta leggibile anche se l'API non è disponibile.
 */
@Component({
  selector: 'app-digest',
  templateUrl: './digest.component.html',
  styleUrls: ['./digest.component.scss']
})
export class DigestComponent implements OnInit, OnDestroy {
  digest: DailyDigest | null = null;
  loading = false;
  error: string | null = null;
  // La sottoscrizione viene conservata per poterla chiudere alla distruzione:
  // senza, una risposta tardiva aggiornerebbe un componente già rimosso.
  private subscription?: Subscription;
  private digestUrl = `${environment.apiUrl}/digest`;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    console.log('📰 Pagina Digest caricata');
    this.loadDigest();
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  loadDigest(): void {
    // Ogni caricamento riparte da zero: loading attivo, errore precedente azzerato.
    this.loading = true;
    this.error = null;

    // Prova prima a caricare dal backend, poi fallback su file statico
    // Catena di fallback: API -> /assets/digest.json -> null (nessun digest).
    // L'ultimo valore null è trasformato in un messaggio leggibile dal template.
    this.subscription = this.http.get<DailyDigest>(this.digestUrl).pipe(
      catchError(error => {
        console.warn('⚠️ Errore nel caricamento digest dal backend, provo file statico:', error);
        return this.http.get<DailyDigest>('/assets/digest.json').pipe(
          catchError(err => {
            console.error('❌ Errore nel caricamento digest da file statico:', err);
            return of(null);
          })
        );
      }),
      map(digest => {
        if (digest) {
          console.log('✅ Digest caricato:', digest.date);
        }
        return digest;
      })
    ).subscribe({
      next: (digest) => {
        this.digest = digest;
        this.loading = false;
        // digest null = nessuna fonte disponibile (backend e file statico
        // hanno fallito): si mostra un avviso invece di una pagina vuota.
        if (!digest) {
          this.error = 'Nessun digest disponibile per oggi';
        }
      },
      error: (err) => {
        console.error('❌ Errore nel caricamento digest:', err);
        this.error = 'Errore nel caricamento del digest';
        this.loading = false;
      }
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    return date.toLocaleDateString('it-IT', options);
  }

  getCategoryEmoji(category: string): string {
    // Le etichette delle categorie nel digest non coincidono sempre con le
    // chiavi della mappa, quindi il confronto è "contiene" in entrambe le
    // direzioni; in mancanza di match si usa l'emoji generica.
    const emojiMap: { [key: string]: string } = {
      'Cybersecurity': '🔒',
      'Intelligenza Artificiale & Tecnologia': '🤖',
      'Tecnologia': '💻',
      'Scienza': '🔬',
      'Filosofia': '📚',
      'Innovazione': '💡',
      'Cultura': '🎭',
      'Etica': '⚖️',
      'Sport': '⚽',
      'Ambiente': '🌱',
      'Business': '💼',
      'Salute': '🏥',
      'Politica': '🏛️',
      'Intrattenimento': '🎬'
    };

    for (const [key, emoji] of Object.entries(emojiMap)) {
      if (category.toLowerCase().includes(key.toLowerCase()) || 
          key.toLowerCase().includes(category.toLowerCase())) {
        return emoji;
      }
    }

    return '📰';
  }
}

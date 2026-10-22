import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { SavedArticleService } from '../../services/saved-article.service';
import { WeatherService, WeatherData } from '../../services/weather.service';

/**
 * Header dell'app: data e ora, meteo, scorciatoie verso le sezioni principali
 * e menu utente.
 * Non carica articoli: si limita a riflettere lo stato dei servizi (utente
 * autenticato, articoli salvati) e a navigare.
 */
@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnDestroy {
  searchQuery = '';
  currentUser: User | null = null;
  savedCount = 0;
  currentDate = '';
  currentTime = '';
  weatherData: WeatherData | null = null;
  private dateTimeInterval: any;

  constructor(
    // Esposti pubblicamente perché il template ne legge lo stato (menu utente, badge).
    public authService: AuthService,
    public savedArticleService: SavedArticleService,
    private weatherService: WeatherService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Subscribe to user changes
    // currentUser$ è un BehaviorSubject: emette subito lo stato corrente e poi
    // ogni cambio (login, logout, refresh del profilo) senza che l'header
    // debba conoscere l'origine dell'aggiornamento.
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    // Subscribe to saved articles count
    // Il badge dell'header si aggiorna da solo quando un articolo viene
    // salvato o rimosso da qualsiasi pagina.
    this.savedArticleService.savedArticles$.subscribe((articles: number[]) => {
      this.savedCount = articles.length;
    });

    // Aggiorna data e ora immediatamente e poi ogni secondo
    // Il primo aggiornamento è sincrono, altrimenti l'orologio resterebbe vuoto
    // per un secondo dopo il render.
    this.updateDateTime();
    this.dateTimeInterval = setInterval(() => {
      this.updateDateTime();
    }, 1000);

    // Carica meteo
    this.loadWeather();
  }

  ngOnDestroy(): void {
    // Pulisci l'intervallo quando il componente viene distrutto
    // Senza clearInterval l'orologio continuerebbe a girare anche a componenti distrutti.
    if (this.dateTimeInterval) {
      clearInterval(this.dateTimeInterval);
    }
  }

  updateDateTime(): void {
    const now = new Date();
    
    // Formatta la data: "Mercoledì 13 Novembre 2024"
    const optionsDate: Intl.DateTimeFormatOptions = {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    };
    this.currentDate = now.toLocaleDateString('it-IT', optionsDate);
    
    // Formatta l'ora: "14:30:45"
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    this.currentTime = `${hours}:${minutes}:${seconds}`;
  }

  onSearch(): void {
    // Nota: il template attuale espone la ricerca come link a /search,
    // quindi questo metodo non è più richiamato dalla UI.
    if (this.searchQuery.trim()) {
      this.router.navigate(['/search'], {
        queryParams: { q: this.searchQuery }
      });
      // Reset dopo navigazione
      // this.searchQuery = '';
    }
  }

  loadWeather(): void {
    // Il servizio fa geolocalizzazione via IP e poi chiama Open-Meteo:
    // il risultato è mostrato in header, quindi non deve bloccare il render.
    this.weatherService.getCurrentWeather().subscribe({
      next: (weather) => {
        this.weatherData = weather;
        console.log('✅ Meteo caricato:', weather);
      },
      error: (error) => {
        console.error('❌ Errore caricamento meteo:', error);
        // Fallback: dati di default
        // Il meteo è decorativo: in caso di errore si mostra un placeholder
        // invece di lasciare spazio vuoto nell'header.
        this.weatherData = {
          temperature: 20,
          condition: 'Parzialmente nuvoloso',
          conditionCode: 2,
          city: 'Italia',
          icon: 'wb_cloudy'
        };
      }
    });
  }

  logout(): void {
    // logout() invalida la sessione lato server (best-effort) e pulisce
    // token e utente dal localStorage; l'header si aggiorna da solo
    // perché currentUser$ notifica il nuovo stato (null).
    this.authService.logout();
    this.router.navigate(['/']);
  }
}


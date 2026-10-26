import { Component, OnInit, OnDestroy, NgZone, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { SavedArticleService } from '../../services/saved-article.service';
import { WeatherService, WeatherData } from '../../services/weather.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
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
    public themeService: ThemeService,
    private weatherService: WeatherService,
    private router: Router,
    private ngZone: NgZone,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    // Subscribe to user changes
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      this.cdr.markForCheck();
    });

    // Subscribe to saved articles count
    this.savedArticleService.savedArticles$.subscribe((articles: number[]) => {
      this.savedCount = articles.length;
      this.cdr.markForCheck();
    });

    // Aggiorna data e ora immediatamente e poi ogni secondo
    this.updateDateTime();
    this.ngZone.runOutsideAngular(() => {
      this.dateTimeInterval = setInterval(() => {
        this.ngZone.run(() => {
          this.updateDateTime();
          this.cdr.markForCheck();
        });
      }, 1000);
    });

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
        this.cdr.markForCheck();
      },
      error: (error) => {
        // Fallback: dati di default
        this.weatherData = {
          temperature: 20,
          condition: 'Parzialmente nuvoloso',
          conditionCode: 2,
          city: 'Italia',
          icon: 'wb_cloudy'
        };
        this.cdr.markForCheck();
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


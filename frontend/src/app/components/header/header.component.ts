import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { SavedArticleService } from '../../services/saved-article.service';
import { WeatherService, WeatherData } from '../../services/weather.service';

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
    public authService: AuthService,
    public savedArticleService: SavedArticleService,
    private weatherService: WeatherService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Subscribe to user changes
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    // Subscribe to saved articles count
    this.savedArticleService.savedArticles$.subscribe((articles: number[]) => {
      this.savedCount = articles.length;
    });

    // Aggiorna data e ora immediatamente e poi ogni secondo
    this.updateDateTime();
    this.dateTimeInterval = setInterval(() => {
      this.updateDateTime();
    }, 1000);

    // Carica meteo
    this.loadWeather();
  }

  ngOnDestroy(): void {
    // Pulisci l'intervallo quando il componente viene distrutto
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
    if (this.searchQuery.trim()) {
      this.router.navigate(['/search'], {
        queryParams: { q: this.searchQuery }
      });
      // Reset dopo navigazione
      // this.searchQuery = '';
    }
  }

  loadWeather(): void {
    this.weatherService.getCurrentWeather().subscribe({
      next: (weather) => {
        this.weatherData = weather;
        console.log('✅ Meteo caricato:', weather);
      },
      error: (error) => {
        console.error('❌ Errore caricamento meteo:', error);
        // Fallback: dati di default
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
}


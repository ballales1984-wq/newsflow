import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';

export interface WeatherData {
  temperature: number;
  condition: string;
  conditionCode: number;
  city: string;
  region?: string;
  icon?: string;
}

@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  private readonly IP_GEOLOCATION_API = 'https://ipapi.co/json/';
  private readonly WEATHER_API_BASE = 'https://api.open-meteo.com/v1/forecast';

  constructor(private http: HttpClient) {}

  /**
   * Ottiene la posizione dell'utente tramite IP geolocation
   */
  getUserLocation(): Observable<{ lat: number; lon: number; city: string; region?: string }> {
    return this.http.get<any>(this.IP_GEOLOCATION_API).pipe(
      map((data: any) => ({
        lat: data.latitude,
        lon: data.longitude,
        city: data.city || 'Sconosciuta',
        region: data.region || data.region_code || undefined
      })),
      catchError(() => {
        // Fallback: usa posizione di default (Roma, Italia)
        console.warn('⚠️ Impossibile ottenere posizione, uso default (Roma)');
        return of({
          lat: 41.9028,
          lon: 12.4964,
          city: 'Roma',
          region: 'Lazio'
        });
      })
    );
  }

  /**
   * Ottiene le condizioni meteo per una posizione specifica
   */
  getWeather(lat: number, lon: number, city: string, region?: string): Observable<WeatherData> {
    const url = `${this.WEATHER_API_BASE}?latitude=${lat}&longitude=${lon}&current=temperature_2m,weather_code&timezone=auto&forecast_days=1`;
    
    return this.http.get<any>(url).pipe(
      map((data: any) => {
        const current = data.current;
        const weatherCode = current.weather_code;
        const temperature = Math.round(current.temperature_2m);
        
        return {
          temperature,
          condition: this.getWeatherCondition(weatherCode),
          conditionCode: weatherCode,
          city,
          region,
          icon: this.getWeatherIcon(weatherCode)
        };
      }),
      catchError((error) => {
        console.error('❌ Errore chiamata meteo:', error);
        // Fallback: dati di default
        return of({
          temperature: 20,
          condition: 'Parzialmente nuvoloso',
          conditionCode: 2,
          city,
          region
        });
      })
    );
  }

  /**
   * Ottiene meteo completo (posizione + condizioni)
   */
  getCurrentWeather(): Observable<WeatherData> {
    return this.getUserLocation().pipe(
      switchMap(location => 
        this.getWeather(location.lat, location.lon, location.city, location.region)
      )
    );
  }

  /**
   * Converte codice meteo WMO in descrizione italiana
   */
  private getWeatherCondition(code: number): string {
    const conditions: { [key: number]: string } = {
      0: 'Sereno',
      1: 'Prevalentemente sereno',
      2: 'Parzialmente nuvoloso',
      3: 'Nuvoloso',
      45: 'Nebbia',
      48: 'Nebbia ghiacciata',
      51: 'Pioggerella leggera',
      53: 'Pioggerella moderata',
      55: 'Pioggerella intensa',
      56: 'Pioggerella gelata leggera',
      57: 'Pioggerella gelata intensa',
      61: 'Pioggia leggera',
      63: 'Pioggia moderata',
      65: 'Pioggia intensa',
      66: 'Pioggia gelata leggera',
      67: 'Pioggia gelata intensa',
      71: 'Neve leggera',
      73: 'Neve moderata',
      75: 'Neve intensa',
      77: 'Granelli di neve',
      80: 'Rovesci leggeri',
      81: 'Rovesci moderati',
      82: 'Rovesci intensi',
      85: 'Rovesci di neve leggeri',
      86: 'Rovesci di neve intensi',
      95: 'Temporale',
      96: 'Temporale con grandine',
      99: 'Temporale intenso con grandine'
    };
    
    return conditions[code] || 'Sconosciuto';
  }

  /**
   * Ottiene icona Material per codice meteo
   */
  private getWeatherIcon(code: number): string {
    if (code === 0) return 'wb_sunny';
    if (code <= 2) return 'partly_cloudy_day';
    if (code === 3) return 'cloud';
    if (code >= 45 && code <= 48) return 'foggy';
    if (code >= 51 && code <= 67) return 'grain';
    if (code >= 71 && code <= 77) return 'ac_unit';
    if (code >= 80 && code <= 86) return 'grain';
    if (code >= 95 && code <= 99) return 'thunderstorm';
    return 'wb_cloudy';
  }
}


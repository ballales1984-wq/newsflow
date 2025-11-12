import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { interval, Subscription, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class KeepAliveService {
  private apiUrl = `${environment.apiUrl.replace('/api/v1', '')}/api/health`;
  private subscription?: Subscription;
  private readonly PING_INTERVAL = 10 * 60 * 1000; // 10 minuti

  constructor(private http: HttpClient) {}

  /**
   * Avvia il servizio di keep-alive
   * Fa ping al backend ogni 10 minuti per mantenerlo sveglio
   */
  start(): void {
    if (this.subscription) {
      return; // Già avviato
    }

    console.log('🔄 Servizio Keep-Alive avviato');
    
    // Ping immediato
    this.pingBackend();

    // Ping periodico ogni 10 minuti
    this.subscription = interval(this.PING_INTERVAL).subscribe(() => {
      this.pingBackend();
    });
  }

  /**
   * Ferma il servizio di keep-alive
   */
  stop(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
      this.subscription = undefined;
      console.log('⏹️ Servizio Keep-Alive fermato');
    }
  }

  /**
   * Esegue un ping al backend
   */
  private pingBackend(): void {
    // Usa catchError per evitare che gli errori interferiscano con altre richieste
    this.http.get(this.apiUrl, { 
      timeout: 30000,
      observe: 'response'
    }).pipe(
      catchError(() => {
        // Ignora silenziosamente gli errori del keep-alive
        return of(null);
      })
    ).subscribe({
      next: (response) => {
        if (response) {
          console.log('✅ Backend sveglio');
        }
      },
      error: () => {
        // Errore già gestito dal catchError
      }
    });
  }
}


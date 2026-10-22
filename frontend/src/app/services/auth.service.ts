import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, timeout } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  avatar_url?: string;
  preferences?: UserPreferences;
  reading_mode: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

export interface UserPreferences {
  theme: string;
  language: string;
  reading_mode: string;
  digest_enabled: boolean;
  digest_time: string;
  categories_preferred: string[];
  notifications_enabled: boolean;
  push_notifications: boolean;
  email_notifications: boolean;
}

export interface AuthResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

// Chiavi localStorage usate per persistere i token e l'utente tra i refresh di pagina.
// Sono costanti per evitare errori di battitura e per permettere a altri servizi
// di leggere gli stessi valori (es. interceptor per il Bearer).
const TOKEN_KEY = 'newsflow_token';
const REFRESH_TOKEN_KEY = 'newsflow_refresh_token';
const USER_KEY = 'newsflow_user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/users`;
  // Stato dell'utente corrente in memoria: null quando non è loggato,
// l'oggetto User quando lo è. È un BehaviorSubject, quindi i componenti
// che si iscrivono a `currentUser$` ricevono aggiornamenti in tempo reale
// (es. aggiornamento del profilo o logout da un altro tab).
private currentUserSubject = new BehaviorSubject<User | null>(null);
  
  currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadStoredUser();
  }

  // Al costruttore legge l'utente dal localStorage: permette di mantenere la
// sessione anche dopo un refresh di pagina. Se il JSON è corrotto, fa logout.
private loadStoredUser(): void {
    const storedUser = localStorage.getItem(USER_KEY);
    if (storedUser) {
      try {
        this.currentUserSubject.next(JSON.parse(storedUser));
      } catch {
        this.logout();
      }
    }
  }

  // Restituisce l'access_token JWT corrente, o null se non è loggato.
// Usato dall'interceptor per autenticare le richieste protette.
getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  // True se esiste un token in localStorage; non ne verifica la validità.
// Usato per mostrare/nascondere il menu di autenticazione senza chiamate API.
isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Flusso di login: invia email/password al backend, salva i token e l'utente
// tramite handleAuthResponse. L'errore viene rilanciato (throw) così il
// chiamante può mostrare un messaggio di errore specifico; il catch non
// restituisce un Observable di successo, interrompe la catena.
login(email: string, password: string): Observable<AuthResponse> {
    const loginData = { email, password };
    console.log('🔐 Login attempt:', email, loginData);
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, JSON.stringify(loginData), {
      headers: { 'Content-Type': 'application/json' }
    }).pipe(
      tap(response => {
        console.log('✅ Login success:', response);
        this.handleAuthResponse(response);
      }),
      catchError(error => {
        console.error('❌ Login error:', error);
        throw error;
      })
    );
  }

  register(data: RegisterRequest): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}/register`, data);
  }

  // Logout: chiama il backend per invalidare la sessione (best-effort,
// gli errori vengono ignorati) e pulisce localStorage + Subject.
// Non aspetta la risposta del server per disconnettere l'utente.
logout(): void {
    if (this.getToken()) {
      this.http.post(`${this.apiUrl}/logout`, {}, {
        headers: this.getHeaders()
      }).subscribe({
        error: () => {}
      });
    }
    
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUserSubject.next(null);
  }

  // Rinnova il token usando il refresh_token salvato in localStorage.
// Il backend emette un nuovo access_token (e un nuovo refresh_token
// opzionale) prima della scadenza; questo metodo permette di evitare
// il re-login dell'utente quando l'access_token scade.
refreshToken(): Observable<AuthResponse> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    return this.http.post<AuthResponse>(`${this.apiUrl}/refresh`, {
      refresh_token: refreshToken
    }).pipe(
      tap(response => this.handleAuthResponse(response))
    );
  }

  getProfile(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/me`, {
      headers: this.getHeaders()
    });
  }

  updateProfile(data: Partial<User>): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/me`, data, {
      headers: this.getHeaders()
    });
  }

  updatePreferences(prefs: UserPreferences): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/me/preferences`, prefs, {
      headers: this.getHeaders()
    });
  }

  getPreferences(): Observable<UserPreferences> {
    return this.http.get<UserPreferences>(`${this.apiUrl}/me/preferences`, {
      headers: this.getHeaders()
    });
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  // Costruisce l'header Authorization con il Bearer token corrente.
// Usato da tutti i metodi che richiedono autenticazione (me, preferences, logout).
getHeaders(): HttpHeaders {
    const token = this.getToken();
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  // Salva i token e l'utente in localStorage e notifica il Subject.
// Chiamato sia da login che da refresh: garantisce che lo stato sia
// coerente indipendentemente da quale flusso abbia generato la risposta.
private handleAuthResponse(response: AuthResponse): void {
    localStorage.setItem(TOKEN_KEY, response.access_token);
    if (response.refresh_token) {
      localStorage.setItem(REFRESH_TOKEN_KEY, response.refresh_token);
    }
    localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    this.currentUserSubject.next(response.user);
  }
}
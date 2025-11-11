import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface User {
  id: number;
  name: string;
  fingerprint: string;
  created_at: string;
  last_seen: string;
  is_new?: boolean;
}

export interface AuthResponse {
  success: boolean;
  authenticated: boolean;
  user: User;
  message?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    // Auto-login on init
    this.whoami().subscribe();
  }

  whoami(): Observable<AuthResponse> {
    return this.http.get<AuthResponse>(`${this.apiUrl}/whoami`).pipe(
      tap(response => {
        if (response.success && response.user) {
          this.currentUserSubject.next(response.user);
          
          // Show welcome message for new users
          if (response.user.is_new && response.message) {
            console.log(response.message);
          }
        }
      })
    );
  }

  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  isAuthenticated(): boolean {
    return this.currentUserSubject.value !== null;
  }
}


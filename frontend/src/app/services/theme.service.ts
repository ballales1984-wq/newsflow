import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private darkMode = new BehaviorSubject<boolean>(false);
  public darkMode$: Observable<boolean> = this.darkMode.asObservable();

  constructor() {
    // Check local storage for saved theme
    const savedTheme = localStorage.getItem('darkMode');
    if (savedTheme) {
      this.darkMode.next(savedTheme === 'true');
      this.applyTheme(savedTheme === 'true');
    } else {
      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      this.darkMode.next(prefersDark);
      this.applyTheme(prefersDark);
    }
  }

  toggleTheme(): void {
    const newValue = !this.darkMode.value;
    this.darkMode.next(newValue);
    this.applyTheme(newValue);
    localStorage.setItem('darkMode', newValue.toString());
  }

  private applyTheme(isDark: boolean): void {
    if (isDark) {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }

  get isDarkMode(): boolean {
    return this.darkMode.value;
  }
}


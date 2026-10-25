import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ScrollPositionService {
  // Mappa route -> posizione di scroll (in pixel). Usata come cache in memoria
  // per il caso in cui sessionStorage non sia disponibile (es. navigator.cookieEnabled=false).
  private scrollPositions: { [key: string]: number } = {};

  /**
   * Salva la posizione di scroll corrente per una route
   */
  saveScrollPosition(route: string = 'home'): void {
    const scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
    this.scrollPositions[route] = scrollY;
    // Salva anche in sessionStorage per persistenza tra navigazioni
    sessionStorage.setItem(`scroll_${route}`, scrollY.toString());
    console.log(`💾 Posizione scroll salvata per ${route}: ${scrollY}px`);
  }

  /**
   * Ripristina la posizione di scroll per una route
   */
  restoreScrollPosition(route: string = 'home'): void {
    // Prima prova sessionStorage, poi memoria
    const savedPosition = sessionStorage.getItem(`scroll_${route}`);
    const position = savedPosition 
      ? parseInt(savedPosition, 10) 
      : this.scrollPositions[route] || 0;
    
    if (position > 0) {
      // Usa requestAnimationFrame per assicurarsi che il DOM sia pronto
      requestAnimationFrame(() => {
        window.scrollTo({
          top: position,
          behavior: 'auto' // Comportamento istantaneo, non smooth
        });
        console.log(`📍 Posizione scroll ripristinata per ${route}: ${position}px`);
      });
    }
  }

  /**
   * Rimuove la posizione salvata
   */
  clearScrollPosition(route: string = 'home'): void {
    delete this.scrollPositions[route];
    sessionStorage.removeItem(`scroll_${route}`);
  }

  /**
   * Scorre verso un elemento DOM con retry automatico se l'elemento non è
   * ancora nel DOM (es. dopo un caricamento asincrono di articoli).
   * Offsets in pixel per compensare header fissi.
   */
  scrollToElement(elementId: string, offset: number = 80, maxAttempts: number = 5): void {
    let attempts = 0;

    const tryScroll = () => {
      attempts++;
      const element = document.getElementById(elementId);

      if (element) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
          top: Math.max(0, offsetPosition),
          behavior: 'smooth'
        });
      } else if (attempts < maxAttempts) {
        setTimeout(tryScroll, 200);
      }
    };

    tryScroll();
  }
}


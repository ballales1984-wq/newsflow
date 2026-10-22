import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

/**
 * Banner di consenso cookie (GDPR).
 * La scelta viene salvata nel localStorage: la chiave 'cookieConsent' con i valori
 * 'accepted' o 'rejected'. Se la chiave manca (prima visita, dati cancellati)
 * il banner ricompare, perché in assenza di una scelta registrata il consenso
 * non può essere considerato prestato.
 */
@Component({
  selector: 'app-cookie-banner',
  templateUrl: './cookie-banner.component.html',
  styleUrls: ['./cookie-banner.component.scss']
})
export class CookieBannerComponent implements OnInit {
  showBanner: boolean = false;

  constructor(private router: Router) {}

  ngOnInit() {
    // Controlla se l'utente ha già accettato i cookie
    const cookieConsent = localStorage.getItem('cookieConsent');
    if (!cookieConsent) {
      // Mostra banner dopo un breve delay per UX migliore
      // Il ritardo lascia completare il primo rendering: il banner non deve
      // coprire il contenuto mentre la pagina si sta ancora popolando.
      setTimeout(() => {
        this.showBanner = true;
      }, 1000);
    }
  }

  acceptCookies() {
    // La scelta e la data sono entrambe persistite: la data serve a dimostrare
    // quando il consenso è stato accordato.
    localStorage.setItem('cookieConsent', 'accepted');
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    this.showBanner = false;
    
    // Abilita Google Analytics e AdSense
    this.enableTracking();
  }

  rejectCookies() {
    // Stessa struttura del consenso positivo: la scelta "rifiuta" è anch'essa
    // una decisione da registrare, non un'assenza di scelta.
    localStorage.setItem('cookieConsent', 'rejected');
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    this.showBanner = false;
    
    // Disabilita tracking
    this.disableTracking();
  }

  private enableTracking() {
    // Abilita Google Analytics e AdSense tramite Consent Mode
    // Se lo script GA non è ancora in pagina non c'è nulla da aggiornare:
    // il flag nel localStorage è comunque la fonte di verità per il banner.
    if (typeof (window as any).gtag !== 'undefined') {
      (window as any).gtag('consent', 'update', {
        'ad_storage': 'granted',
        'ad_user_data': 'granted',
        'ad_personalization': 'granted',
        'analytics_storage': 'granted'
      });
    }
  }

  private disableTracking() {
    // Disabilita Google Analytics e AdSense tramite Consent Mode
    if (typeof (window as any).gtag !== 'undefined') {
      (window as any).gtag('consent', 'update', {
        'ad_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied',
        'analytics_storage': 'denied'
      });
    }
  }
}


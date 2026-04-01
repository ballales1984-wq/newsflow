import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

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
      setTimeout(() => {
        this.showBanner = true;
      }, 1000);
    }
  }

  acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    this.showBanner = false;
    
    // Abilita Google Analytics e AdSense
    this.enableTracking();
  }

  rejectCookies() {
    localStorage.setItem('cookieConsent', 'rejected');
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    this.showBanner = false;
    
    // Disabilita tracking
    this.disableTracking();
  }

  private enableTracking() {
    // Abilita Google Analytics e AdSense tramite Consent Mode
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


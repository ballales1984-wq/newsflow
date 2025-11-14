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
    // Abilita Google Analytics
    if (typeof (window as any).gtag !== 'undefined') {
      (window as any).gtag('consent', 'update', {
        'analytics_storage': 'granted',
        'ad_storage': 'granted'
      });
    }

    // Abilita AdSense
    if (typeof (window as any).adsbygoogle !== 'undefined') {
      // Gli ads verranno caricati automaticamente
    }
  }

  private disableTracking() {
    // Disabilita Google Analytics
    if (typeof (window as any).gtag !== 'undefined') {
      (window as any).gtag('consent', 'update', {
        'analytics_storage': 'denied',
        'ad_storage': 'denied'
      });
    }
  }
}


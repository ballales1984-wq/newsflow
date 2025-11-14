import { Component, OnInit, Input, OnDestroy, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-ad-banner',
  templateUrl: './ad-banner.component.html',
  styleUrls: ['./ad-banner.component.scss']
})
export class AdBannerComponent implements OnInit, AfterViewInit, OnDestroy {
  @Input() adId: string = 'ad-banner';
  @Input() adClient: string = 'ca-pub-2145959534306055'; // Publisher ID: pub-2145959534306055 (già configurato!)
  @Input() adSlot: string = '1234567890'; // Sostituisci con il tuo Ad Slot dopo approvazione sito web
  @Input() adFormat: string = 'auto'; // auto, horizontal, vertical, rectangle
  @Input() adLayout?: string; // Per ads responsive
  @Input() fullWidth: boolean = true;
  @Input() adStyle?: string; // Stile personalizzato

  private adLoaded: boolean = false;
  private adScriptLoaded: boolean = false;

  ngOnInit() {
    // Verifica se AdSense è già caricato
    if (typeof (window as any).adsbygoogle !== 'undefined') {
      this.adScriptLoaded = true;
    } else {
      this.loadAdSenseScript();
    }
  }

  ngAfterViewInit() {
    // Aspetta che lo script sia caricato prima di inizializzare ads
    if (this.adScriptLoaded) {
      this.initializeAd();
    } else {
      // Controlla periodicamente se lo script è stato caricato
      const checkInterval = setInterval(() => {
        if (typeof (window as any).adsbygoogle !== 'undefined') {
          this.adScriptLoaded = true;
          clearInterval(checkInterval);
          this.initializeAd();
        }
      }, 100);

      // Timeout dopo 5 secondi
      setTimeout(() => {
        clearInterval(checkInterval);
        if (!this.adScriptLoaded) {
          console.warn('AdSense script non caricato entro il timeout');
        }
      }, 5000);
    }
  }

  ngOnDestroy() {
    // Cleanup se necessario
  }

  private loadAdSenseScript() {
    // Verifica se lo script è già presente
    if (document.querySelector('script[src*="adsbygoogle"]')) {
      this.adScriptLoaded = true;
      return;
    }

    // Carica script AdSense
    const script = document.createElement('script');
    script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + this.adClient;
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.onload = () => {
      this.adScriptLoaded = true;
      this.initializeAd();
    };
    script.onerror = () => {
      console.error('Errore nel caricamento dello script AdSense');
    };
    document.head.appendChild(script);
  }

  private initializeAd() {
    if (this.adLoaded) {
      return;
    }

    try {
      // Inizializza AdSense
      ((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({
        google_ad_client: this.adClient,
        enable_page_level_ads: false
      });
      this.adLoaded = true;
    } catch (e) {
      console.error('Errore nell\'inizializzazione di AdSense:', e);
    }
  }

  // Metodo per ricaricare l'ad (utile dopo cambi di route)
  reloadAd() {
    this.adLoaded = false;
    setTimeout(() => {
      this.initializeAd();
    }, 100);
  }
}


import { Component, OnInit, Input, OnDestroy, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * Banner pubblicitario AdSense.
 *
 * Lo script di terze parti è caricato in modo asincrono e solo quando serve:
 * la pubblicità non deve mai ritardare il rendering dei contenuti, quindi
 * nessuna operazione qui è bloccante per il resto della pagina.
 */
@Component({
  selector: 'app-ad-banner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ad-banner.component.html',
  styleUrls: ['./ad-banner.component.scss']
})
export class AdBannerComponent implements OnInit, AfterViewInit, OnDestroy {
  @Input() adId: string = 'ad-banner';
  // Publisher ID pubblico di AdSense (non è una chiave segreta: è visibile nel markup).
  @Input() adClient: string = 'ca-pub-2145959534306055'; // Publisher ID: pub-2145959534306055 (già configurato!)
  @Input() adSlot: string = '1234567890'; // Sostituisci con il tuo Ad Slot dopo approvazione sito web
  @Input() adFormat: string = 'auto'; // auto, horizontal, vertical, rectangle
  @Input() adLayout?: string; // Per ads responsive
  @Input() fullWidth: boolean = true;
  @Input() adStyle?: string; // Stile personalizzato

  // Garantisce che lo script venga iniettato una sola volta per componente.
  private adLoaded: boolean = false;
  private adScriptLoaded: boolean = false;

  ngOnInit() {
    // Verifica se AdSense è già caricato
    // Se lo script è già in pagina (o è già stato caricato da un altro banner)
    // non lo si reinietta: si riusa quello esistente.
    if (typeof (window as any).adsbygoogle !== 'undefined') {
      this.adScriptLoaded = true;
    } else {
      this.loadAdSenseScript();
    }
  }

  ngAfterViewInit() {
    if (this.adScriptLoaded) {
      this.initializeAd();
      return;
    }
    setTimeout(() => {
      if (!this.adScriptLoaded && typeof (window as any).adsbygoogle !== 'undefined') {
        this.adScriptLoaded = true;
        this.initializeAd();
      }
    }, 500);
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
    // async = true: il download non blocca il parsing HTML né il primo paint.
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
    if (this.adLoaded || (window as any).__adsenseInitialized) {
      return;
    }

    let attempts = 0;
    const maxAttempts = 3;

    const run = () => {
      try {
        if (this.adLoaded || (window as any).__adsenseInitialized) {
          return;
        }
        attempts++;
        const container = document.getElementById(this.adId);
        if (!container || container.clientWidth === 0) {
          if (attempts < maxAttempts) {
            requestAnimationFrame(run);
          }
          return;
        }
        ((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({
          google_ad_client: this.adClient
        });
        (window as any).__adsenseInitialized = true;
        this.adLoaded = true;
      } catch (e) {
        // Silently fail
      }
    };

    requestAnimationFrame(run);
  }

  // Metodo per ricaricare l'ad (utile dopo cambi di route)
  // Nota: al momento non è richiamato da nessun template.
  reloadAd() {
    this.adLoaded = false;
    setTimeout(() => {
      this.initializeAd();
    }, 100);
  }
}

import { Component, OnInit, Input, OnDestroy, AfterViewInit } from '@angular/core';

/**
 * Banner pubblicitario AdSense.
 *
 * Lo script di terze parti è caricato in modo asincrono e solo quando serve:
 * la pubblicità non deve mai ritardare il rendering dei contenuti, quindi
 * nessuna operazione qui è bloccante per il resto della pagina.
 */
@Component({
  selector: 'app-ad-banner',
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
    // Aspetta che lo script sia caricato prima di inizializzare ads
    if (this.adScriptLoaded) {
      this.initializeAd();
    } else {
      // Controlla periodicamente se lo script è stato caricato
      // Polling ogni 100ms: lo script è esterno e non offre un callback affidabile
      // quando è già in volo, quindi si preferisce sondare lo stato globale.
      const checkInterval = setInterval(() => {
        if (typeof (window as any).adsbygoogle !== 'undefined') {
          this.adScriptLoaded = true;
          clearInterval(checkInterval);
          this.initializeAd();
        }
      }, 100);

      // Timeout dopo 5 secondi
      // Un annuncio che non arriva non deve essere un errore applicativo:
      // si limita a segnalarlo e il banner resta vuoto.
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
    // Doppio avvio possibile (onload dello script + polling): il flag evita
    // di inserire due volte la stessa richiesta nella coda.
    if (this.adLoaded) {
      return;
    }

    try {
      // Inizializza AdSense
      // Push sulla coda globale adsbygoogle: lo script AdSense la svuota al caricamento.
      // enable_page_level_ads resta disattivato: gli annunci devono comparire solo
      // dove il template dichiara le unità, non automaticamente su tutta la pagina.
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
  // Nota: al momento non è richiamato da nessun template.
  reloadAd() {
    this.adLoaded = false;
    setTimeout(() => {
      this.initializeAd();
    }, 100);
  }
}


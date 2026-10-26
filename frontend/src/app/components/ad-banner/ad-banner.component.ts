import { Component, OnInit, Input, OnDestroy, AfterViewInit, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ad-banner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ad-banner.component.html',
  styleUrls: ['./ad-banner.component.scss']
})
export class AdBannerComponent implements OnInit, AfterViewInit, OnDestroy {
  @Input() adId: string = 'ad-banner';
  @Input() adClient: string = 'ca-pub-2145959534306055';
  @Input() adSlot: string = '1234567890';
  @Input() adFormat: string = 'auto';
  @Input() adLayout?: string;
  @Input() fullWidth: boolean = true;
  @Input() adStyle?: string;

  private adLoaded: boolean = false;
  private adScriptLoaded: boolean = false;
  private observer?: IntersectionObserver;
  private initialized: boolean = false;

  constructor(private el: ElementRef) {}

  ngOnInit() {
    if (typeof (window as any).adsbygoogle !== 'undefined') {
      this.adScriptLoaded = true;
    }
  }

  ngAfterViewInit() {
    if (typeof IntersectionObserver === 'undefined') {
      if (this.adScriptLoaded) {
        this.initializeAd();
      } else {
        this.loadAdSenseScript();
      }
      return;
    }

    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !this.initialized) {
          this.initialized = true;
          this.loadAdSenseScript();
          this.observer?.disconnect();
        }
      });
    }, { rootMargin: '150px' });

    this.observer.observe(this.el.nativeElement);
  }

  ngOnDestroy() {
    this.observer?.disconnect();
  }

  private loadAdSenseScript() {
    if (this.adScriptLoaded) {
      this.initializeAd();
      return;
    }

    if (document.querySelector('script[src*="adsbygoogle"]')) {
      this.adScriptLoaded = true;
      this.initializeAd();
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + this.adClient;
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.onload = () => {
      this.adScriptLoaded = true;
      this.initializeAd();
    };
    document.head.appendChild(script);
  }

  private initializeAd() {
    if (this.adLoaded || (window as any).__adsenseInitialized) {
      return;
    }

    let attempts = 0;
    const maxAttempts = 2;

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

  reloadAd() {
    this.adLoaded = false;
    setTimeout(() => {
      this.initializeAd();
    }, 100);
  }
}

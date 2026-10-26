import { Injectable, NgZone, OnDestroy } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SpeechService implements OnDestroy {
  private isSupported = false;
  private hasSpoken = false;
  private voicesLoaded = false;
  private voicesCheckInterval: any = null;
  private synth: SpeechSynthesis | undefined;

  // Al costruttore verifica se il browser supporta speechSynthesis.
  // Se non è supportato, isSupported rimane false e tutti i metodi
  // restituiscono immediatamente senza errori in console.
  // Le voci possono non essere disponibili immediatamente all'avvio
  // (caricate in background): si registra onvoiceschanged per quando
  // saranno pronte. Se non ci sono voci al momento, il codice che
  // chiama speak() aspetta con un polling di 100ms fino a un timeout di 2s.
  constructor(private ngZone: NgZone) {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      this.synth = window.speechSynthesis;
      this.isSupported = true;
      
      if (this.synth.getVoices().length > 0) {
        this.voicesLoaded = true;
      } else {
        this.synth.onvoiceschanged = () => {
          this.voicesLoaded = true;
        };
      }
    }
  }

  /**
   * Riproduce un messaggio vocale con voce femminile italiana
   */
  speak(text: string, force: boolean = false): void {
    if (!this.isSupported || !this.synth) {
      return;
    }

    if (this.hasSpoken && !force) {
      return;
    }

    const doSpeak = () => {
      try {
        this.synth!.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'it-IT';
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        utterance.volume = 0.8;

        const voices = this.synth!.getVoices();
        const italianFemaleVoice = voices.find((voice: SpeechSynthesisVoice) => 
          voice.lang.startsWith('it') && 
          (voice.name.toLowerCase().includes('female') || 
           voice.name.toLowerCase().includes('zira') ||
           voice.name.toLowerCase().includes('elena') ||
           voice.name.toLowerCase().includes('silvia') ||
           voice.name.toLowerCase().includes('paola') ||
           voice.name.toLowerCase().includes('chiara'))
        );

        if (italianFemaleVoice) {
          utterance.voice = italianFemaleVoice;
        } else {
          const italianVoice = voices.find((voice: SpeechSynthesisVoice) => voice.lang.startsWith('it'));
          if (italianVoice) {
            utterance.voice = italianVoice;
          }
        }

        utterance.onend = () => {
          this.hasSpoken = true;
        };

        utterance.onerror = (event: any) => {
          if (event?.error === 'not-allowed') {
            return;
          }
          this.hasSpoken = true;
        };

        this.synth!.speak(utterance);
      } catch (error) {
        this.hasSpoken = true;
      }
    };

    if (this.voicesLoaded || this.synth.getVoices().length > 0) {
      this.voicesLoaded = true;
      doSpeak();
      return;
    }

    if (this.voicesCheckInterval) {
      return;
    }

    this.ngZone.runOutsideAngular(() => {
      this.voicesCheckInterval = setInterval(() => {
        if (this.synth!.getVoices().length > 0 || this.voicesLoaded) {
          if (this.voicesCheckInterval) {
            clearInterval(this.voicesCheckInterval);
            this.voicesCheckInterval = null;
          }
          this.voicesLoaded = true;
          this.ngZone.run(() => doSpeak());
        }
      }, 100);
    });

    setTimeout(() => {
      if (this.voicesCheckInterval) {
        clearInterval(this.voicesCheckInterval);
        this.voicesCheckInterval = null;
      }
      this.ngZone.run(() => doSpeak());
    }, 1000);
  }

  /**
   * Riproduce il messaggio di benvenuto
   */
  speakWelcome(): void {
    this.speak('Ecco le tue notizie da NewsFlow', false);
  }

  /**
   * Ferma la riproduzione corrente
   */
  // Ferma la riproduzione corrente.
  // cancel() interrompe il messaggio in coda e il corrente; non restituisce
  // uno stato, quindi non si sa se il messaggio era iniziato o no.
  stop(): void {
    if (this.synth) {
      this.synth.cancel();
    }
  }

  reset(): void {
    this.hasSpoken = false;
  }

  isAvailable(): boolean {
    return this.isSupported;
  }

  ngOnDestroy(): void {
    if (this.voicesCheckInterval) {
      clearInterval(this.voicesCheckInterval);
      this.voicesCheckInterval = null;
    }
    if (this.synth) {
      try {
        this.synth.cancel();
      } catch (e) {}
    }
  }
}


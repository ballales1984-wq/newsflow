import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SpeechService {
  private synth: SpeechSynthesis | null = null;
  private isSupported = false;
  private hasSpoken = false; // Flag per evitare di ripetere il messaggio

  constructor() {
    if ('speechSynthesis' in window) {
      this.synth = window.speechSynthesis;
      this.isSupported = true;
      console.log('✅ Speech Synthesis supportato');
      
      // Le voci possono non essere disponibili immediatamente
      // Aspetta che siano caricate
      if (this.synth.getVoices().length === 0) {
        this.synth.onvoiceschanged = () => {
          console.log('✅ Voci caricate:', this.synth?.getVoices().length);
        };
      }
    } else {
      console.warn('⚠️ Speech Synthesis non supportato dal browser');
    }
  }

  /**
   * Riproduce un messaggio vocale con voce femminile italiana
   */
  speak(text: string, force: boolean = false): void {
    if (!this.isSupported || !this.synth) {
      console.warn('⚠️ Speech Synthesis non disponibile');
      return;
    }

    // Se già pronunciato e non forzato, non ripetere
    if (this.hasSpoken && !force) {
      return;
    }

    // Funzione per riprodurre il messaggio
    const doSpeak = () => {
      // Annulla eventuali messaggi in coda
      this.synth!.cancel();

      // Crea utterance
      const utterance = new SpeechSynthesisUtterance(text);
      
      // Imposta lingua italiana
      utterance.lang = 'it-IT';
      
      // Velocità e volume
      utterance.rate = 0.9; // Leggermente più lento per chiarezza
      utterance.pitch = 1.1; // Leggermente più acuto per suono più femminile
      utterance.volume = 0.8; // Volume moderato

      // Cerca una voce femminile italiana
      const voices = this.synth!.getVoices();
      const italianFemaleVoice = voices.find(voice => 
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
        console.log('✅ Voce femminile italiana trovata:', italianFemaleVoice.name);
      } else {
        // Fallback: cerca qualsiasi voce italiana
        const italianVoice = voices.find(voice => voice.lang.startsWith('it'));
        if (italianVoice) {
          utterance.voice = italianVoice;
          console.log('✅ Voce italiana trovata:', italianVoice.name);
        } else {
          console.warn('⚠️ Nessuna voce italiana trovata, uso default');
        }
      }

      // Eventi
      utterance.onstart = () => {
        console.log('🔊 Inizio riproduzione vocale');
      };

      utterance.onend = () => {
        console.log('✅ Fine riproduzione vocale');
        this.hasSpoken = true;
      };

      utterance.onerror = (event) => {
        console.error('❌ Errore riproduzione vocale:', event);
      };

      // Riproduci
      try {
        this.synth!.speak(utterance);
      } catch (error) {
        console.error('❌ Errore chiamata speechSynthesis:', error);
      }
    };

    // Se le voci non sono ancora caricate, aspetta
    if (this.synth.getVoices().length === 0) {
      console.log('⏳ Voci non ancora caricate, aspetto...');
      const checkVoices = setInterval(() => {
        if (this.synth!.getVoices().length > 0) {
          clearInterval(checkVoices);
          console.log('✅ Voci caricate, riproduco messaggio');
          doSpeak();
        }
      }, 100);
      
      // Timeout dopo 2 secondi
      setTimeout(() => {
        clearInterval(checkVoices);
        if (this.synth!.getVoices().length === 0) {
          console.warn('⚠️ Timeout caricamento voci, riproduco comunque');
        }
        doSpeak();
      }, 2000);
    } else {
      doSpeak();
    }
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
  stop(): void {
    if (this.synth) {
      this.synth.cancel();
    }
  }

  /**
   * Resetta il flag per permettere di riprodurre di nuovo
   */
  reset(): void {
    this.hasSpoken = false;
  }

  /**
   * Verifica se il supporto è disponibile
   */
  isAvailable(): boolean {
    return this.isSupported;
  }
}


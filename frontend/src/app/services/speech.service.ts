import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SpeechService {
private synth: SpeechSynthesis | null = null;
  private isSupported = false;
  // Flag per evitare di ripetere il messaggio di benvenuto più volte di seguito.
  // Viene messo a true alla fine di `onend` e reso false da reset().
  // Permette di riprodurre lo stesso testo solo dopo un reset manuale o un force.
  private hasSpoken = false; // Flag per evitare di ripetere il messaggio

  // Al costruttore verifica se il browser supporta speechSynthesis.
  // Se non è supportato, isSupported rimane false e tutti i metodi
  // restituiscono immediatamente senza errori in console.
  // Le voci possono non essere disponibili immediatamente all'avvio
  // (caricate in background): si registra onvoiceschanged per quando
  // saranno pronte. Se non ci sono voci al momento, il codice che
  // chiama speak() aspetta con un polling di 100ms fino a un timeout di 2s.
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

    // Se già pronunciato e non forzato, non ripetere.
    // Il flag hasSpoken impedisce di riascoltare il benvenuto più volte
    // senza un intervento esplicito (reset() o force=true).
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
      
      // Velocità e volume: rate=0.9 (più lento per chiarezza), pitch=1.1
      // (più acuto per suono "femminile"), volume=0.8 (moderato).
      utterance.rate = 0.9; // Leggermente più lento per chiarezza
      utterance.pitch = 1.1; // Leggermente più acuto per suono più femminile
      utterance.volume = 0.8; // Volume moderato

      // Selezione voce per lingua: cerca prima una voce italiana "femminile"
      // (name contiene female/Zira/Elena/Silvia/Paola/Chiara). Se non la trova,
      // cerca qualsiasi voce con lang che inizia per 'it'. Se nemmeno quella
      // esiste, usa la voce di default del browser (nessun utterance.voice).
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

      // Eventi: onstart/onend/onerror forniscono feedback per il debugging
      // e permettono di gestire lo stato (es. hasSpoken = true in onend).
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

    // Se le voci non sono ancora caricate, aspetta con un polling di 100ms.
    // Timeout di 2s: se dopo 2 secondi non ci sono voci, riproduce comunque
    // con la voce di default (potrebbe non essere italiana).
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
  // Ferma la riproduzione corrente.
  // cancel() interrompe il messaggio in coda e il corrente; non restituisce
  // uno stato, quindi non si sa se il messaggio era iniziato o no.
  stop(): void {
    if (this.synth) {
      this.synth.cancel();
    }
  }

  /**
   * Resetta il flag per permettere di riprodurre di nuovo
   */
  // Resetta il flag per permettere di riprodurre di nuovo.
  // Dopo un reset, speak() può riprodurre lo stesso testo anche se già pronunciato.
  reset(): void {
    this.hasSpoken = false;
  }

  /**
   * Verifica se il supporto è disponibile
   */
  // Verifica se il supporto è disponibile.
  // Restituisce isSupported, che è true solo se window.speechSynthesis esiste.
  isAvailable(): boolean {
    return this.isSupported;
  }
}


import { Component, OnInit, OnDestroy } from '@angular/core';
import { ThemeService } from './services/theme.service';
import { KeepAliveService } from './services/keep-alive.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
/**
 * Componente radice: resta vivo per l'intera sessione e ospita header,
 * router-outlet e cookie banner.
 * È quindi il punto naturale per avviare i servizi che devono durare quanto l'app
 * (keep-alive del backend) e per fermarli alla chiusura.
 */
export class AppComponent implements OnInit, OnDestroy {
  title = 'NewsFlow';

  constructor(
    // Iniettare il tema qui forza la sua creazione al bootstrap: il servizio,
    // nel suo costruttore, decide chiaro/scuro leggendo 'darkMode' dal localStorage
    // e, se assente, la preferenza di sistema (prefers-color-scheme).
    // Nota: toggleTheme() non è richiamato da nessun template, quindi lo switch
    // chiaro/scuro non è ancora esposto all'utente.
    public themeService: ThemeService,
    private keepAliveService: KeepAliveService
  ) {
    console.log('🏗️ AppComponent constructor');
  }

  ngOnInit(): void {
    console.log('🎯 AppComponent ngOnInit');
    // Avvia il servizio keep-alive per mantenere il backend sveglio
    // Il ping al backend è best-effort: se il servizio non parte (backend irraggiungibile)
    // l'app deve comunque rendersi, quindi l'errore viene solo loggato e non propagato.
    try {
      this.keepAliveService.start();
      console.log('✅ Keep-alive service started');
    } catch (error) {
      console.error('❌ Error starting keep-alive:', error);
    }
  }

  ngOnDestroy(): void {
    // Ferma il servizio quando l'app si chiude
    // stop() annulla l'intervallo di ping: senza, il timer sopravvive alla chiusura
    // della tab e continuerebbe a interrogare il backend inutilmente.
    this.keepAliveService.stop();
  }
}


import { Component, OnInit, OnDestroy } from '@angular/core';
import { ThemeService } from './services/theme.service';
import { KeepAliveService } from './services/keep-alive.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'NewsFlow';

  constructor(
    public themeService: ThemeService,
    private keepAliveService: KeepAliveService
  ) {
    console.log('🏗️ AppComponent constructor');
  }

  ngOnInit(): void {
    console.log('🎯 AppComponent ngOnInit');
    // Avvia il servizio keep-alive per mantenere il backend sveglio
    try {
      this.keepAliveService.start();
      console.log('✅ Keep-alive service started');
    } catch (error) {
      console.error('❌ Error starting keep-alive:', error);
    }
  }

  ngOnDestroy(): void {
    // Ferma il servizio quando l'app si chiude
    this.keepAliveService.stop();
  }
}


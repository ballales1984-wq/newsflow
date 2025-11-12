import { Component, OnInit, OnDestroy, AfterViewInit, ViewChild, HostListener } from '@angular/core';
import { MatDrawer } from '@angular/material/sidenav';
import { ThemeService } from './services/theme.service';
import { KeepAliveService } from './services/keep-alive.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy, AfterViewInit {
  title = 'NewsFlow';
  @ViewChild('drawer') drawer!: MatDrawer;
  isMobile = false;
  drawerOpened = true; // Inizia sempre aperto, poi si chiude su mobile

  constructor(
    public themeService: ThemeService,
    private keepAliveService: KeepAliveService
  ) {
    console.log('🏗️ AppComponent constructor');
    this.checkScreenSize();
  }

  ngAfterViewInit(): void {
    // Assicurati che il drawer sia nello stato corretto dopo che la view è inizializzata
    setTimeout(() => {
      if (this.drawer) {
        if (this.isMobile) {
          // Su mobile: chiudi e usa overlay
          this.drawer.mode = 'over';
          this.drawer.close();
          this.drawerOpened = false;
        } else {
          // Su desktop: FORZA apertura e modalità side
          this.drawer.mode = 'side';
          this.drawer.open();
          this.drawerOpened = true;
          // Forza aggiornamento dopo apertura
          setTimeout(() => {
            if (this.drawer && !this.drawer.opened) {
              this.drawer.open();
              this.drawerOpened = true;
            }
          }, 200);
        }
      }
    }, 100);
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.checkScreenSize();
  }

  checkScreenSize() {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;
    
    // Se passa da mobile a desktop o viceversa, aggiorna il drawer
    if (this.drawer) {
      if (this.isMobile) {
        // Su mobile: chiudi e usa overlay
        this.drawer.mode = 'over';
        if (this.drawer.opened) {
          this.drawer.close();
        }
        this.drawerOpened = false;
      } else {
        // Su desktop: apri e usa side
        this.drawer.mode = 'side';
        if (!this.drawer.opened) {
          this.drawer.open();
        }
        this.drawerOpened = true;
      }
    }
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

  toggleSidebar() {
    if (this.drawer) {
      this.drawer.toggle();
    }
  }
}


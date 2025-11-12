import { Component, OnInit, OnDestroy, ViewChild, HostListener } from '@angular/core';
import { MatDrawer } from '@angular/material/sidenav';
import { ThemeService } from './services/theme.service';
import { KeepAliveService } from './services/keep-alive.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'NewsFlow';
  @ViewChild('drawer') drawer!: MatDrawer;
  isMobile = false;

  constructor(
    public themeService: ThemeService,
    private keepAliveService: KeepAliveService
  ) {
    this.checkScreenSize();
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.checkScreenSize();
    // Aggiorna lo stato del drawer quando cambia la dimensione dello schermo
    if (this.drawer) {
      if (this.isMobile && this.drawer.opened) {
        this.drawer.close();
      } else if (!this.isMobile && !this.drawer.opened) {
        this.drawer.open();
      }
    }
  }

  checkScreenSize() {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;
    
    // Se passa da mobile a desktop o viceversa, aggiorna il drawer
    if (this.drawer && wasMobile !== this.isMobile) {
      if (this.isMobile) {
        this.drawer.close();
      } else {
        this.drawer.open();
      }
    }
  }

  ngOnInit(): void {
    // Avvia il servizio keep-alive per mantenere il backend sveglio
    this.keepAliveService.start();
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


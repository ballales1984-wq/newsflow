import { NgModule, isDevMode } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgrokInterceptor } from './interceptors/ngrok.interceptor';

// Material imports
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatMenuModule } from '@angular/material/menu';
import { MatBadgeModule } from '@angular/material/badge';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule } from '@angular/material/dialog';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { SidebarComponent } from './components/sidebar/sidebar.component';
import { ExplainDialogComponent } from './components/explain-dialog/explain-dialog.component';
import { DigestComponent } from './pages/digest/digest.component';
import { PrivacyComponent } from './pages/privacy/privacy.component';
import { TermsComponent } from './pages/terms/terms.component';
import { AuthComponent } from './pages/auth/auth.component';
import { CookieBannerComponent } from './components/cookie-banner/cookie-banner.component';
import { ServiceWorkerModule } from '@angular/service-worker';

/**
 * Modulo radice dell'applicazione (architettura a modulo unico, senza componenti standalone).
 * I componenti della home (HomeComponent, ArticleListComponent, ArticleCardComponent,
 * CategoryFilterComponent, AdBannerComponent) sono ora standalone e caricati in lazy
 * tramite il router, quindi non vanno dichiarati qui.
 */
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SidebarComponent,
    ExplainDialogComponent,
    PrivacyComponent,
    TermsComponent,
    AuthComponent,
    CookieBannerComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    // Le animazioni di Angular devono essere abilite: i componenti Material
    // (dialog, menu, paginator) dipendono da di esse e falliscono senza.
    BrowserAnimationsModule,
    HttpClientModule,
    // FormsModule serve nei template con [(ngModel)], ReactiveFormsModule nei form
    // costruiti con FormBuilder (login, ricerca, filtri).
    FormsModule,
    ReactiveFormsModule,
    // Un modulo Material per ogni widget realmente usato nei template:
    // importare MaterialModule per intero farebbe crescere inutilmente il bundle.
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatCardModule,
    MatChipsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatPaginatorModule,
    MatMenuModule,
    MatBadgeModule,
    MatTooltipModule,
    MatSnackBarModule,
    MatDialogModule,
    MatTabsModule,
    MatDividerModule,
    // Service worker attivo solo in produzione (isDevMode()): in sviluppo la cache
    // servirebbe a mascherare le modifiche locali.
    // La registrazione avviene a app stabile o dopo 30 secondi, così non compete
    // con il primo rendering.
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: !isDevMode(),
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000'
    })
  ],
  providers: [
    {
      // L'interceptor aggiunge l'header che fa saltare la pagina di avviso di ngrok
      // quando il backend è esposto tramite tunnel: senza, il browser blocca la risposta.
      // multi: true perché gli interceptor HTTP sono una catena, non un valore singolo.
      provide: HTTP_INTERCEPTORS,
      useClass: NgrokInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }


import { FooterModule } from './components/footer/footer.module';

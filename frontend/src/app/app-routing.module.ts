import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ArticleDetailComponent } from './pages/article-detail/article-detail.component';
import { SearchComponent } from './pages/search/search.component';
import { SavedComponent } from './pages/saved/saved.component';
import { DigestComponent } from './pages/digest/digest.component';
import { PrivacyComponent } from './pages/privacy/privacy.component';
import { TermsComponent } from './pages/terms/terms.component';
import { AuthComponent } from './pages/auth/auth.component';

/**
 * Routing dell'applicazione: tutte le rotte sono dichiarate qui in un unico modulo.
 *
 * Nota: nessuna rotta usa loadChildren, quindi tutti i componenti vengono caricati
 * eager nel bundle principale. Per un sito di queste dimensioni va bene; se il bundle
 * cresce, le pagine meno usate (saved, digest, privacy, terms) sarebbero le prime
 * candidate per un caricamento lazy.
 */
const routes: Routes = [
  { path: '', component: HomeComponent },
  // Login e registrazione condividono lo stesso componente: la modalità è decisa
  // dentro AuthComponent, non dal path.
  { path: 'login', component: AuthComponent },
  { path: 'register', component: AuthComponent },
  // :slug è l'identificativo con cui l'articolo viene cercato nel backend.
  { path: 'article/:slug', component: ArticleDetailComponent },
  { path: 'search', component: SearchComponent },
  { path: 'saved', component: SavedComponent },
  { path: 'digest', component: DigestComponent },
  { path: 'privacy', component: PrivacyComponent },
  { path: 'terms', component: TermsComponent },
  // Rotta jolly: qualunque URL sconosciuto riporta alla home.
  { path: '**', redirectTo: '' }
];

@NgModule({
  // forRoot() registra il router come provider singleton e attiva la navigazione;
  // export[] lo rende disponibile anche ai template dei componenti dichiarati
  // (routerLink, router-outlet).
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }


import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', loadComponent: () => import('./pages/auth/auth.component').then(m => m.AuthComponent) },
  { path: 'register', loadComponent: () => import('./pages/auth/auth.component').then(m => m.AuthComponent) },
  { path: 'article/:slug', loadComponent: () => import('./pages/article-detail/article-detail.component').then(m => m.ArticleDetailComponent) },
  { path: 'search', loadComponent: () => import('./pages/search/search.component').then(m => m.SearchComponent) },
  { path: 'saved', loadComponent: () => import('./pages/saved/saved.component').then(m => m.SavedComponent) },
  { path: 'digest', loadComponent: () => import('./pages/digest/digest.component').then(m => m.DigestComponent) },
  { path: 'privacy', loadComponent: () => import('./pages/privacy/privacy.component').then(m => m.PrivacyComponent) },
  { path: 'terms', loadComponent: () => import('./pages/terms/terms.component').then(m => m.TermsComponent) },
  { path: 'normative', loadComponent: () => import('./pages/normative/normative.component').then(m => m.NormativeComponent) },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ArticleDetailComponent } from './pages/article-detail/article-detail.component';
import { SearchComponent } from './pages/search/search.component';
import { SavedComponent } from './pages/saved/saved.component';
import { DigestComponent } from './pages/digest/digest.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'article/:slug', component: ArticleDetailComponent },
  { path: 'search', component: SearchComponent },
  { path: 'saved', component: SavedComponent },
  { path: 'digest', component: DigestComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }


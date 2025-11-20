import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { Article, ArticleList, ArticleSearch } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private apiUrl = `${environment.apiUrl}/articles`;
  
  // Header per bypassare warning ngrok (se necessario)
  private headers = new HttpHeaders({
    'ngrok-skip-browser-warning': 'true'
  });

  constructor(private http: HttpClient) {}

  getArticles(
    page: number = 1,
    size: number = 20,
    filters?: Partial<ArticleSearch>
  ): Observable<ArticleList> {
    // IMPORTANTE: Prova PRIMA a caricare dal file statico, poi fallback all'API
    console.log('📡 Tentativo caricamento articoli da file statico...');
    
    return this.http.get<ArticleList>('/assets/final_news_italian.json').pipe(
      catchError(staticError => {
        console.warn('⚠️ Errore caricamento da file statico, provo API:', staticError);
        
        // Fallback all'API se il file statico non è disponibile
        let params = new HttpParams()
          .set('skip', ((page - 1) * size).toString())
          .set('limit', size.toString());

        if (filters) {
          if (filters.category_id) {
            params = params.set('category_id', filters.category_id.toString());
          }
          if (filters.source_id) {
            params = params.set('source_id', filters.source_id.toString());
          }
          if (filters.language) {
            params = params.set('language', filters.language);
          }
          if (filters.date_from) {
            params = params.set('date_from', filters.date_from);
          }
          if (filters.min_quality_score) {
            params = params.set('min_quality_score', filters.min_quality_score.toString());
          }
        }

        console.log('📡 API Request:', { url: this.apiUrl, params: params.toString() });
        return this.http.get<ArticleList>(this.apiUrl, { params, headers: this.headers }).pipe(
          catchError(apiError => {
            console.error('❌ Errore anche dall\'API:', apiError);
            // Se anche l'API fallisce, restituisci array vuoto
            return of({
              items: [],
              total: 0,
              page: page,
              size: size,
              pages: 1
            });
          })
        );
      }),
      map(articles => {
        // Applica filtri localmente se caricato da file statico
        if (filters && articles.items && articles.items.length > 0) {
          let filtered = articles.items;
          
          if (filters.category_id) {
            filtered = filtered.filter(a => a.category_id === filters.category_id);
          }
          if (filters.source_id) {
            filtered = filtered.filter(a => a.source_id === filters.source_id);
          }
          if (filters.language) {
            filtered = filtered.filter(a => a.language === filters.language);
          }
          
          // Applica paginazione
          const skip = (page - 1) * size;
          const paginated = filtered.slice(skip, skip + size);
          
          return {
            items: paginated,
            total: filtered.length,
            page: page,
            size: size,
            pages: Math.ceil(filtered.length / size)
          };
        }
        
        // Se non ci sono filtri, applica solo paginazione
        if (articles.items && articles.items.length > 0) {
          const skip = (page - 1) * size;
          const paginated = articles.items.slice(skip, skip + size);
          
          return {
            items: paginated,
            total: articles.total || articles.items.length,
            page: page,
            size: size,
            pages: Math.ceil((articles.total || articles.items.length) / size)
          };
        }
        
        return articles;
      })
    );
  }

  getArticle(id: number): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/${id}`, { headers: this.headers });
  }

  getArticleBySlug(slug: string): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/slug/${slug}`, { headers: this.headers });
  }

  searchArticles(
    search: ArticleSearch,
    page: number = 1,
    size: number = 20
  ): Observable<ArticleList> {
    const params = new HttpParams()
      .set('skip', ((page - 1) * size).toString())
      .set('limit', size.toString());

    return this.http.post<ArticleList>(`${this.apiUrl}/search`, search, { params, headers: this.headers });
  }

  getFeaturedArticles(limit: number = 10): Observable<Article[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<Article[]>(`${this.apiUrl}/featured/list`, { params, headers: this.headers });
  }

  getRecentArticles(days: number = 7, limit: number = 20): Observable<Article[]> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString());
    return this.http.get<Article[]>(`${this.apiUrl}/recent/list`, { params, headers: this.headers });
  }
}


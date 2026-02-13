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
    // Prova prima l'API dinamica, poi fallback su file statico
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

    console.log('📡 API Request: - article.service.ts:49', { url: this.apiUrl, params: params.toString() });
    
    return this.http.get<ArticleList>(this.apiUrl, { params, headers: this.headers }).pipe(
      catchError(error => {
        console.warn('⚠️ API non disponibile, uso fallback su file statico: - article.service.ts:53', error);
        // Fallback: carica da file JSON statico
        return this.http.get<any>('/assets/final_news_italian.json').pipe(
          catchError(err => {
            console.error('❌ Anche file statico non disponibile: - article.service.ts:57', err);
            return of({
              items: [],
              total: 0,
              page: page,
              size: size,
              pages: 1
            });
          }),
          map((data: any) => {
            // Converti formato file statico in ArticleList
            const items = data.items || data || [];
            return {
              items: items.slice(0, size),
              total: items.length,
              page: page,
              size: size,
              pages: Math.ceil(items.length / size)
            };
          })
        );
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


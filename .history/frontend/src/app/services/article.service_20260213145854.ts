import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
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


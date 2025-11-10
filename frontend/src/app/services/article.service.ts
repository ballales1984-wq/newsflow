import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Article, ArticleList, ArticleSearch } from '../models/article.model';

@Injectable({
  providedIn: 'root'
})
export class ArticleService {
  private apiUrl = `${environment.apiUrl}/articles`;

  constructor(private http: HttpClient) {}

  getArticles(
    page: number = 1,
    size: number = 20,
    filters?: Partial<ArticleSearch>
  ): Observable<ArticleList> {
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

    return this.http.get<ArticleList>(this.apiUrl, { params });
  }

  getArticle(id: number): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/${id}`);
  }

  getArticleBySlug(slug: string): Observable<Article> {
    return this.http.get<Article>(`${this.apiUrl}/slug/${slug}`);
  }

  searchArticles(
    search: ArticleSearch,
    page: number = 1,
    size: number = 20
  ): Observable<ArticleList> {
    const params = new HttpParams()
      .set('skip', ((page - 1) * size).toString())
      .set('limit', size.toString());

    return this.http.post<ArticleList>(`${this.apiUrl}/search`, search, { params });
  }

  getFeaturedArticles(limit: number = 10): Observable<Article[]> {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get<Article[]>(`${this.apiUrl}/featured/list`, { params });
  }

  getRecentArticles(days: number = 7, limit: number = 20): Observable<Article[]> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString());
    return this.http.get<Article[]>(`${this.apiUrl}/recent/list`, { params });
  }
}


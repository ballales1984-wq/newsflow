import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, BehaviorSubject } from 'rxjs';
import { environment } from '../../environments/environment';
import { SavedArticle } from '../models/saved-article.model';

@Injectable({
  providedIn: 'root'
})
export class SavedArticleService {
  private apiUrl = `${environment.apiUrl}/saved`;
  // Stato salvato in memoria: array di ID articoli.
    // È duplicato in localStorage (chiave 'savedArticles') per persistere tra
    // i refresh di pagina; il Subject notifica i componenti delle variazioni.
private savedArticles: number[] = []; // IDs articoli salvati (localStorage)
  private savedArticlesSubject = new BehaviorSubject<number[]>([]);
  public savedArticles$ = this.savedArticlesSubject.asObservable();

  constructor(private http: HttpClient) {
    // Al costruttore legge gli ID salvati dal localStorage.
    // Se il JSON è corrotto, JSON.parse lancia e l'errore non è gestito:
    // l'app potrebbe crashare all'avvio. È un caso di errore non gestito.
    const saved = localStorage.getItem('savedArticles');
    if (saved) {
      this.savedArticles = JSON.parse(saved);
      this.savedArticlesSubject.next(this.savedArticles);
    }
  }

  saveArticle(articleId: number): Observable<any> {
    if (!this.savedArticles.includes(articleId)) {
      this.savedArticles.push(articleId);
      this.saveToLocalStorage();
      this.savedArticlesSubject.next(this.savedArticles);
    }
    return of({ message: 'Article saved!' });
  }

  unsaveArticle(articleId: number): Observable<any> {
    this.savedArticles = this.savedArticles.filter(id => id !== articleId);
    this.saveToLocalStorage();
    this.savedArticlesSubject.next(this.savedArticles);
    return of({ message: 'Article removed!' });
  }

  isSaved(articleId: number): boolean {
    return this.savedArticles.includes(articleId);
  }

  getSavedArticles(): number[] {
    return this.savedArticles;
  }

  private saveToLocalStorage(): void {
    localStorage.setItem('savedArticles', JSON.stringify(this.savedArticles));
  }
}


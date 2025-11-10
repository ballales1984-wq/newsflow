import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Source } from '../models/source.model';

@Injectable({
  providedIn: 'root'
})
export class SourceService {
  private apiUrl = `${environment.apiUrl}/sources`;

  constructor(private http: HttpClient) {}

  getSources(isActive?: boolean): Observable<Source[]> {
    let params = new HttpParams();
    if (isActive !== undefined) {
      params = params.set('is_active', isActive.toString());
    }
    return this.http.get<Source[]>(this.apiUrl, { params });
  }

  getSource(id: number): Observable<Source> {
    return this.http.get<Source>(`${this.apiUrl}/${id}`);
  }
}


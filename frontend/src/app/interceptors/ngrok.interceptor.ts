import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable()
export class NgrokInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Aggiungi header ngrok solo se l'URL contiene ngrok-free.dev
    if (req.url.includes('ngrok-free.dev') || req.url.includes('ngrok-free.app')) {
      const clonedReq = req.clone({
        setHeaders: {
          'ngrok-skip-browser-warning': 'true'
        }
      });
      return next.handle(clonedReq);
    }
    
    return next.handle(req);
  }
}


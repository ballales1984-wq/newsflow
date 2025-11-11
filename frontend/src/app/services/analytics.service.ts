import { Injectable } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

declare let gtag: Function;

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  
  constructor(private router: Router) {
    this.initRouteTracking();
  }

  /**
   * Inizializza tracking automatico route changes
   */
  private initRouteTracking(): void {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.trackPageView(event.urlAfterRedirects);
    });
  }

  /**
   * Track page view
   */
  trackPageView(url: string): void {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'page_view', {
        page_path: url,
        page_title: document.title
      });
    }
  }

  /**
   * Track custom event
   */
  trackEvent(action: string, category: string, label?: string, value?: number): void {
    if (typeof gtag !== 'undefined') {
      gtag('event', action, {
        event_category: category,
        event_label: label,
        value: value
      });
    }
  }

  /**
   * Track article view
   */
  trackArticleView(articleId: number, articleTitle: string): void {
    this.trackEvent('view_article', 'Articles', articleTitle, articleId);
  }

  /**
   * Track article save
   */
  trackArticleSave(articleId: number, articleTitle: string): void {
    this.trackEvent('save_article', 'Articles', articleTitle, articleId);
  }

  /**
   * Track article share
   */
  trackArticleShare(articleId: number, articleTitle: string): void {
    this.trackEvent('share_article', 'Articles', articleTitle, articleId);
  }

  /**
   * Track "Spiegami" click
   */
  trackExplainClick(articleId: number, articleTitle: string): void {
    this.trackEvent('explain_article', 'AI Features', articleTitle, articleId);
  }

  /**
   * Track "Spiegami" tab change
   */
  trackExplainTab(level: string): void {
    this.trackEvent('explain_tab_change', 'AI Features', level);
  }

  /**
   * Track category filter
   */
  trackCategoryFilter(categoryName: string): void {
    this.trackEvent('filter_category', 'Navigation', categoryName);
  }

  /**
   * Track user login
   */
  trackUserLogin(userName: string, isNew: boolean): void {
    this.trackEvent('user_login', 'Auth', isNew ? 'New User' : 'Returning User');
  }

  /**
   * Track theme change
   */
  trackThemeChange(theme: string): void {
    this.trackEvent('theme_change', 'Settings', theme);
  }
}


import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ThemeService } from '../../services/theme.service';
import { AuthService, User } from '../../services/auth.service';
import { SavedArticleService } from '../../services/saved-article.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  searchQuery = '';
  currentUser: User | null = null;
  savedCount = 0;

  constructor(
    public themeService: ThemeService,
    public authService: AuthService,
    public savedArticleService: SavedArticleService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Subscribe to user changes
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    // Subscribe to saved articles count
    this.savedArticleService.savedArticles$.subscribe((articles: number[]) => {
      this.savedCount = articles.length;
    });
  }

  onSearch(): void {
    if (this.searchQuery.trim()) {
      this.router.navigate(['/search'], {
        queryParams: { q: this.searchQuery }
      });
      // Reset dopo navigazione
      // this.searchQuery = '';
    }
  }

  toggleTheme(): void {
    this.themeService.toggleTheme();
  }
}


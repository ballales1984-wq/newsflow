import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})
export class AuthComponent {
  isLoginMode = true;
  isLoading = false;
  authForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar,
    private themeService: ThemeService
  ) {
    this.authForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      username: [''],
      fullName: ['']
    });
  }

  toggleMode(): void {
    this.isLoginMode = !this.isLoginMode;
    this.authForm.reset();
  }

  onSubmit(): void {
    if (this.authForm.invalid) {
      return;
    }

    this.isLoading = true;
    const { email, password, username, fullName } = this.authForm.value;

    if (this.isLoginMode) {
      this.authService.login(email, password).subscribe({
        next: (response) => {
          this.snackBar.open(`Benvenuto, ${response.user.username}!`, 'Chiudi', { duration: 3000 });
          this.router.navigate(['/']);
        },
        error: (error) => {
          this.isLoading = false;
          this.snackBar.open(
            error.error?.detail || 'Login fallito',
            'Chiudi',
            { duration: 3000 }
          );
        }
      });
    } else {
      this.authService.register({ email, username, password, full_name: fullName }).subscribe({
        next: () => {
          this.snackBar.open('Registrazione completata! Effettua il login.', 'Chiudi', { duration: 3000 });
          this.isLoginMode = true;
          this.authForm.get('password')?.reset();
        },
        error: (error) => {
          this.isLoading = false;
          this.snackBar.open(
            error.error?.detail || 'Registrazione fallita',
            'Chiudi',
            { duration: 3000 }
          );
        }
      });
    }
  }
}
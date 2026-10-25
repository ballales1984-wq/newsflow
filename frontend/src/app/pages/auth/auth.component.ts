import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { SeoService } from '../../services/seo.service';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';

/**
 * Pagina unica per login e registrazione: cambia solo la modalità del form.
 * I due flussi condividono lo stesso FormGroup, con i campi della registrazione
 * (username, nome completo) usati solo in modalità "Registrati".
 */
@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})
export class AuthComponent {
  // Nota: la modalità non viene derivata dalla rotta (login e register usano
  // lo stesso componente): si parte sempre dal login e si passa alla
  // registrazione con il bottone in fondo al form.
  isLoginMode = true;
  isLoading = false;
  authForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar,
    private themeService: ThemeService,
    private seoService: SeoService
  ) {
    this.seoService.updateAuthSeo(true);
    this.authForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      // Nota: il validatore richiede 6 caratteri, mentre il messaggio del
      // template ne richiama 8: i due criteri non coincidono.
      password: ['', [Validators.required, Validators.minLength(6)]],
      // Nota: 'username' non ha validatori, quindi i messaggi di errore
      // 'required'/'minlength' previsti dal template non possono mai comparire.
      username: [''],
      fullName: ['']
    });
  }

  toggleMode(): void {
    // Il form viene resettato: le credenziali inserite in una modalità
    // non devono restare visibili nell'altra.
    this.isLoginMode = !this.isLoginMode;
    this.seoService.updateAuthSeo(this.isLoginMode);
    this.authForm.reset();
  }

  onSubmit(): void {
    // Invio bloccato se il form non è valido: il bottone è comunque disabilitato
    // dal template, il controllo qui evita submit via tastiera o script.
    if (this.authForm.invalid) {
      return;
    }

    this.isLoading = true;
    const { email, password, username, fullName } = this.authForm.value;

    if (this.isLoginMode) {
      // Login: il servizio salva token e utente nel localStorage e notifica
      // currentUser$, che fa comparire il menu utente nell'header.
      this.authService.login(email, password).subscribe({
        next: (response) => {
          this.snackBar.open(`Benvenuto, ${response.user.username}!`, 'Chiudi', { duration: 3000 });
          this.router.navigate(['/']);
        },
        error: (error) => {
          this.isLoading = false;
          // error.error?.detail è il messaggio del backend (FastAPI);
          // il testo di fallback copre risposte senza body JSON.
          this.snackBar.open(
            error.error?.detail || 'Login fallito',
            'Chiudi',
            { duration: 3000 }
          );
        }
      });
    } else {
      // Registrazione: il backend si aspetta il nome completo in snake_case.
      this.authService.register({ email, username, password, full_name: fullName }).subscribe({
        next: () => {
          this.snackBar.open('Registrazione completata! Effettua il login.', 'Chiudi', { duration: 3000 });
          this.isLoginMode = true;
          this.authForm.get('password')?.reset();
          // Nota: isLoading non viene riportato a false qui, quindi il bottone
          // resta nello stato di caricamento dopo la registrazione.
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
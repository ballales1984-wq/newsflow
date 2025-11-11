/**
 * Test End-to-End per NewsFlow Frontend
 * Testa tutte le funzionalità principali
 */

describe('NewsFlow E2E Tests', () => {
  const baseUrl = 'http://localhost:4200';

  beforeEach(() => {
    cy.visit(baseUrl);
  });

  describe('Homepage', () => {
    it('dovrebbe caricare la homepage', () => {
      cy.contains('NewsFlow').should('be.visible');
      cy.get('app-header').should('exist');
      cy.get('app-sidebar').should('exist');
    });

    it('dovrebbe mostrare almeno 10 notizie', () => {
      cy.get('app-article-card').should('have.length.at.least', 10);
    });

    it('dovrebbe mostrare categorie nella sidebar', () => {
      cy.contains('Categorie').should('be.visible');
      cy.contains('Technology').should('be.visible');
      cy.contains('Science').should('be.visible');
      cy.contains('Cybersecurity').should('be.visible');
    });
  });

  describe('Funzionalità Card Notizia', () => {
    it('dovrebbe avere pulsante Salva', () => {
      cy.get('app-article-card').first().within(() => {
        cy.get('button[mattooltip="Salva"]').should('exist');
      });
    });

    it('dovrebbe avere pulsante Condividi', () => {
      cy.get('app-article-card').first().within(() => {
        cy.get('button[mattooltip="Condividi"]').should('exist');
      });
    });

    it('dovrebbe avere pulsante Spiegami', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Spiegami').should('exist');
      });
    });

    it('dovrebbe avere pulsante Leggi', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Leggi').should('exist');
      });
    });
  });

  describe('Salvataggio Articoli', () => {
    it('dovrebbe salvare un articolo', () => {
      cy.get('app-article-card').first().within(() => {
        cy.get('button[mattooltip="Salva"]').click();
      });
      
      // Verifica icona cambiata
      cy.get('app-article-card').first().within(() => {
        cy.get('mat-icon').contains('bookmark').should('exist');
      });
    });

    it('dovrebbe mostrare articoli salvati', () => {
      // Salva articolo
      cy.get('app-article-card').first().within(() => {
        cy.get('button[mattooltip="Salva"]').click();
      });
      
      // Vai a Salvati
      cy.contains('Salvati').click();
      cy.url().should('include', '/saved');
      cy.get('app-article-card').should('have.length.at.least', 1);
    });
  });

  describe('Modal Spiegami', () => {
    it('dovrebbe aprire modal quando si clicca Spiegami', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Spiegami').click();
      });
      
      cy.get('mat-dialog-container').should('be.visible');
      cy.contains('Spiegami questa notizia').should('be.visible');
    });

    it('dovrebbe avere 3 tab di spiegazione', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Spiegami').click();
      });
      
      cy.contains('30 secondi').should('be.visible');
      cy.contains('3 minuti').should('be.visible');
      cy.contains('Approfondimento').should('be.visible');
    });

    it('dovrebbe cambiare contenuto tra tab', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Spiegami').click();
      });
      
      // Click su tab diversi
      cy.contains('30 secondi').click();
      cy.contains('IN BREVE').should('be.visible');
      
      cy.contains('3 minuti').click();
      cy.contains('CONTESTO').should('be.visible');
      
      cy.contains('Approfondimento').click();
      cy.contains('ANALISI APPROFONDITA').should('be.visible');
    });
  });

  describe('Dettaglio Articolo', () => {
    it('dovrebbe aprire pagina dettaglio', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Leggi').click();
      });
      
      cy.url().should('include', '/article/');
      cy.get('.article-title').should('be.visible');
    });

    it('dovrebbe mostrare contenuto completo', () => {
      cy.get('app-article-card').first().within(() => {
        cy.contains('Leggi').click();
      });
      
      cy.get('.article-title').should('exist');
      cy.get('.article-info').should('exist');
      cy.get('.article-body').should('exist');
    });
  });

  describe('Ricerca', () => {
    it('dovrebbe cercare notizie', () => {
      cy.get('input[placeholder*="Cerca"]').type('AI{enter}');
      cy.url().should('include', '/search');
    });
  });

  describe('Tema Chiaro/Scuro', () => {
    it('dovrebbe cambiare tema', () => {
      cy.get('button[mattooltip*="theme"]').click();
      cy.get('body').should('have.class', 'dark-theme');
      
      cy.get('button[mattooltip*="theme"]').click();
      cy.get('body').should('not.have.class', 'dark-theme');
    });
  });
});


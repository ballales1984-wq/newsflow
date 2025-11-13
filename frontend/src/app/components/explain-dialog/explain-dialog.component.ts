import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Article } from '../../models/article.model';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-explain-dialog',
  templateUrl: './explain-dialog.component.html',
  styleUrls: ['./explain-dialog.component.scss']
})
export class ExplainDialogComponent implements OnInit {
  selectedTabIndex = 1; // Start con tab "3 minuti"
  
  // Cache per spiegazioni AI
  explanations: { [key: string]: string } = {};
  loading: { [key: string]: boolean } = {};
  aiUsed: string = '';

  constructor(
    public dialogRef: MatDialogRef<ExplainDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public article: Article,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    // Pre-carica spiegazione standard quando si apre il dialog
    this.loadExplanation('standard');
  }

  // Carica spiegazione AI dall'API
  loadExplanation(type: 'quick' | 'standard' | 'deep'): void {
    const cacheKey = type;
    
    // Se già in cache, usa quella
    if (this.explanations[cacheKey]) {
      return;
    }
    
    // Se già in caricamento, aspetta
    if (this.loading[cacheKey]) {
      return;
    }
    
    this.loading[cacheKey] = true;
    
    // Chiama API per spiegazione AI
    const apiUrl = environment.apiUrl.replace('/v1', '/v1/articles/explain');
    this.http.post<any>(apiUrl, {
      article_id: this.article.id,
      slug: this.article.slug,
      explanation_type: type
    }).subscribe({
      next: (response) => {
        if (response.success) {
          this.explanations[cacheKey] = response.explanation;
          this.aiUsed = response.ai_used || 'Static';
        } else {
          // Fallback a spiegazione statica
          this.explanations[cacheKey] = this.getStaticExplanation(type);
        }
        this.loading[cacheKey] = false;
      },
      error: (error) => {
        console.error('Errore caricamento spiegazione AI:', error);
        // Fallback a spiegazione statica
        this.explanations[cacheKey] = this.getStaticExplanation(type);
        this.loading[cacheKey] = false;
      }
    });
  }

  // Spiegazione rapida (30 secondi) - ora usa AI
  getQuickExplanation(): string {
    if (!this.explanations['quick']) {
      this.loadExplanation('quick');
      return this.getStaticExplanation('quick');
    }
    return this.explanations['quick'];
  }

  // Spiegazione standard (3 minuti) - ora usa AI
  getStandardExplanation(): string {
    if (!this.explanations['standard']) {
      this.loadExplanation('standard');
      return this.getStaticExplanation('standard');
    }
    return this.explanations['standard'];
  }

  // Spiegazione approfondita - ora usa AI
  getDeepExplanation(): string {
    if (!this.explanations['deep']) {
      this.loadExplanation('deep');
      return this.getStaticExplanation('deep');
    }
    return this.explanations['deep'];
  }

  // Spiegazione statica migliorata (fallback)
  getStaticExplanation(type: 'quick' | 'standard' | 'deep'): string {
    if (type === 'quick') {
      return `🎯 IN BREVE:

${this.article.title}

${this.article.summary?.substring(0, 250)}...

📍 PERCHÉ È IMPORTANTE:
Questa notizia tratta di ${this.article.keywords?.join(', ')} ed è rilevante per il settore ${this.getCategory()}.

⭐ Quality Score: ${this.getQualityPercent()}%
⏱️ Tempo lettura completa: ${this.article.reading_time_minutes} minuti

🔗 Fonte: ${this.article.author}`;
    }
    
    if (type === 'standard') {
      return `📰 CONTESTO:

${this.article.title}

${this.article.summary}

🔍 COSA SIGNIFICA:

Questa notizia riguarda ${this.article.keywords?.slice(0, 3).join(', ')}. 
È stata pubblicata da ${this.article.author} e selezionata per la sua alta qualità (${this.getQualityPercent()}%).

👥 CHI È COINVOLTO:

• Autore: ${this.article.author}
• Fonte: ${this.getSourceFromUrl()}
• Data: ${this.formatDate()}
• Categoria: ${this.getCategory()}
• Lingua: ${this.article.language?.toUpperCase()}

📊 ANALISI QUALITÀ:

• Quality Score: ${this.getQualityPercent()}% - ${this.getQualityText()}
• Tempo lettura: ${this.article.reading_time_minutes} minuti
• Verificato: ${this.article.is_verified ? 'Sì ✓' : 'In revisione'}

🎓 PAROLE CHIAVE:
${this.article.keywords?.join(' • ')}

🌍 IMPATTO:

Questa notizia è stata selezionata perché supera i nostri standard di qualità 
e tratta temi rilevanti nell'attuale panorama ${this.getCategory()}.

🔗 PER APPROFONDIRE:
Leggi l'articolo completo su: ${this.article.url}`;
    }
    
    // deep
    return `📚 ANALISI APPROFONDITA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

${this.article.title}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 SINTESI COMPLETA:

${this.article.summary}

${this.article.content ? '\n📄 CONTENUTO:\n\n' + this.article.content.substring(0, 800) + '...' : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 CONTESTO E BACKGROUND:

${this.getContextualBackground()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 ATTORI E STAKEHOLDER:

• Autore/Fonte: ${this.article.author}
• Piattaforma: ${this.getSourceFromUrl()}
• Target audience: Lettori interessati a ${this.getCategory()}
• Impatto: ${this.getImpactDescription()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 CONSEGUENZE E IMPLICAZIONI:

${this.getConsequences()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 GLOSSARIO TERMINI:

${this.getGlossary()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 METRICHE DI QUALITÀ:

• Quality Score: ${this.getQualityPercent()}%
• Valutazione: ${this.getQualityText()}
• Tempo lettura stimato: ${this.article.reading_time_minutes} minuti
• Lingua originale: ${this.article.language?.toUpperCase()}
• Status: ${this.article.is_verified ? 'Verificato ✓' : 'In revisione'}
• Featured: ${this.article.is_featured ? 'Sì (In evidenza)' : 'No'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 FONTI E RIFERIMENTI:

• Articolo originale: ${this.article.url}
• Autore: ${this.article.author}
• Data pubblicazione: ${this.formatDate()}
• Raccolta: ${new Date(this.article.collected_at).toLocaleDateString('it-IT')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 PERCHÉ LEGGERE QUESTO ARTICOLO:

Questa notizia è stata curata e selezionata dal nostro sistema di news 
intelligence perché rappresenta contenuto di alta qualità (${this.getQualityPercent()}%) 
su temi di ${this.getCategory()} rilevanti per i lettori di NewsFlow.

Raccomandiamo la lettura a chi vuole approfondire: ${this.article.keywords?.join(', ')}.`;
  }

  // Helper methods
  getCategory(): string {
    if (!this.article.keywords || this.article.keywords.length === 0) {
      return 'informazione generale';
    }
    return this.article.keywords[0].toLowerCase();
  }

  getQualityPercent(): number {
    return Math.round((this.article.quality_score || 0.7) * 100);
  }

  getQualityText(): string {
    const score = this.article.quality_score || 0.7;
    if (score >= 0.85) return 'Eccellente';
    if (score >= 0.75) return 'Molto buona';
    if (score >= 0.65) return 'Buona';
    return 'Discreta';
  }

  getSourceFromUrl(): string {
    try {
      const url = new URL(this.article.url);
      return url.hostname.replace('www.', '');
    } catch {
      return 'Fonte non disponibile';
    }
  }

  formatDate(): string {
    if (!this.article.published_at) return 'Data non disponibile';
    const date = new Date(this.article.published_at);
    return date.toLocaleDateString('it-IT', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getContextualBackground(): string {
    const keyword = this.article.keywords?.[0]?.toLowerCase() || '';
    
    if (keyword.includes('ai') || keyword.includes('artificial')) {
      return 'L\'intelligenza artificiale sta attraversando una fase di rapida evoluzione, con investimenti miliardari, questioni etiche emergenti e un impatto crescente su tutti i settori della società.';
    }
    if (keyword.includes('cybersecurity') || keyword.includes('security') || keyword.includes('hack')) {
      return 'Gli attacchi informatici sono in costante aumento, con nuove vulnerabilità scoperte quotidianamente. La cybersecurity è diventata una priorità strategica per governi e aziende.';
    }
    if (keyword.includes('quantum')) {
      return 'Il quantum computing rappresenta la prossima frontiera tecnologica, con potenziale rivoluzionario ma anche rischi per la sicurezza attuale.';
    }
    if (keyword.includes('climate') || keyword.includes('energy')) {
      return 'La transizione energetica e la lotta al cambiamento climatico sono temi centrali nel dibattito globale contemporaneo.';
    }
    
    return 'Questa notizia si inserisce nel contesto dell\'evoluzione tecnologica e sociale contemporanea, con rilevanza per diversi settori.';
  }

  getImpactDescription(): string {
    const category = this.getCategory();
    if (category.includes('ai') || category.includes('technology')) {
      return 'Aziende tech, sviluppatori, policy makers e cittadini';
    }
    if (category.includes('security') || category.includes('cybersecurity')) {
      return 'Professionisti IT, aziende, utenti finali e istituzioni';
    }
    return 'Stakeholder del settore e pubblico interessato';
  }

  getConsequences(): string {
    return `Le implicazioni di questa notizia potrebbero influenzare:

• Policy makers e regolatori (nuove normative)
• Aziende del settore (strategie e investimenti)
• Professionisti e sviluppatori (competenze richieste)
• Utenti finali e cittadini (impatto quotidiano)

L'evoluzione di questa situazione andrà monitorata nei prossimi mesi per comprenderne 
l'impatto a medio-lungo termine.`;
  }

  getGlossary(): string {
    const glossary: {[key: string]: string} = {
      'AI': 'Intelligenza Artificiale - sistemi che simulano capacità cognitive umane',
      'OpenAI': 'Azienda di ricerca AI, creatore di ChatGPT e GPT-4',
      'ChatGPT': 'Chatbot basato su AI generativa sviluppato da OpenAI',
      'Quantum': 'Tecnologia basata su meccanica quantistica per calcolo avanzato',
      'Cybersecurity': 'Protezione di sistemi, reti e dati da attacchi digitali',
      'NLP': 'Natural Language Processing - elaborazione linguaggio naturale',
      'RSS': 'Really Simple Syndication - formato per distribuzione contenuti',
      'API': 'Application Programming Interface - interfaccia per comunicazione software',
      'Cloud': 'Infrastruttura IT distribuita accessibile via internet',
      'GDPR': 'General Data Protection Regulation - regolamento europeo privacy'
    };

    let result = '';
    const title = this.article.title.toLowerCase();
    const summary = (this.article.summary || '').toLowerCase();
    
    for (const [term, definition] of Object.entries(glossary)) {
      if (title.includes(term.toLowerCase()) || summary.includes(term.toLowerCase())) {
        result += `• ${term}: ${definition}\n`;
      }
    }
    
    return result || '• Nessun termine tecnico specifico rilevato in questa notizia';
  }

  onTabChange(event: any): void {
    // Ottimizzazione: usa requestAnimationFrame per migliorare performance
    requestAnimationFrame(() => {
      const tabIndex = event.index;
      if (tabIndex === 0 && !this.explanations['quick']) {
        this.loadExplanation('quick');
      } else if (tabIndex === 1 && !this.explanations['standard']) {
        this.loadExplanation('standard');
      } else if (tabIndex === 2 && !this.explanations['deep']) {
        this.loadExplanation('deep');
      }
    });
  }

  isLoading(type: string): boolean {
    return this.loading[type] || false;
  }

  close(): void {
    this.dialogRef.close();
  }
}


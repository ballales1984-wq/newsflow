import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Article } from '../../models/article.model';

export interface ExplainLevel {
  title: string;
  content: string;
  duration: string;
}

@Component({
  selector: 'app-explain-dialog',
  templateUrl: './explain-dialog.component.html',
  styleUrls: ['./explain-dialog.component.scss']
})
export class ExplainDialogComponent {
  selectedLevel: 'quick' | 'standard' | 'deep' = 'standard';
  selectedTabIndex = 1; // 0=quick, 1=standard, 2=deep
  
  explanations: Record<'quick' | 'standard' | 'deep', ExplainLevel> = {
    quick: {
      title: 'Spiegazione Rapida (30 secondi)',
      content: this.generateQuickExplanation(),
      duration: '30 sec'
    },
    standard: {
      title: 'Spiegazione Standard (3 minuti)',
      content: this.generateStandardExplanation(),
      duration: '3 min'
    },
    deep: {
      title: 'Approfondimento Completo',
      content: this.generateDeepExplanation(),
      duration: '10 min'
    }
  };

  constructor(
    public dialogRef: MatDialogRef<ExplainDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public article: Article
  ) {}

  generateQuickExplanation(): string {
    return `
🎯 IN BREVE:

${this.article.title}

${this.article.summary?.substring(0, 200)}...

📍 PERCHÉ È IMPORTANTE:
Questa notizia è rilevante perché tocca temi di ${this.article.keywords?.join(', ')} che influenzano ${this.getCategoryContext()}.

🔗 LEGGI L'ORIGINALE: ${this.article.url}
    `.trim();
  }

  generateStandardExplanation(): string {
    return `
📰 CONTESTO:

${this.article.title}

${this.article.summary}

🔍 COSA SIGNIFICA:

Questa notizia parla di ${this.article.keywords?.[0]} e riguarda ${this.getCategoryContext()}.

👥 CHI È COINVOLTO:

• Fonte: ${this.article.author}
• Pubblicato: ${new Date(this.article.published_at || '').toLocaleDateString('it-IT')}
• Categoria: ${this.getCategoryName()}

📊 IMPATTO:

Questa notizia ha un quality score di ${((this.article.quality_score || 0) * 100).toFixed(0)}%, 
indicando contenuti ${this.article.quality_score && this.article.quality_score > 0.8 ? 'di alta qualità' : 'verificati'}.

🎓 PAROLE CHIAVE:
${this.article.keywords?.join(' • ')}

🔗 APPROFONDISCI:
Leggi l'articolo completo su: ${this.article.url}
    `.trim();
  }

  generateDeepExplanation(): string {
    return `
📚 ANALISI APPROFONDITA:

${this.article.title}

📝 SINTESI COMPLETA:

${this.article.summary}

${this.article.content ? '\n' + this.article.content.substring(0, 500) + '...' : ''}

🧠 CONTESTO STORICO:

${this.getHistoricalContext()}

👥 ATTORI COINVOLTI:

${this.getActors()}

🌍 CONSEGUENZE POSSIBILI:

${this.getConsequences()}

📖 GLOSSARIO:

${this.getGlossary()}

📊 ANALISI SEMANTICA:

• Quality Score: ${((this.article.quality_score || 0) * 100).toFixed(0)}%
• Tempo di lettura: ${this.article.reading_time_minutes} minuti
• Lingua: ${this.article.language?.toUpperCase()}
• Verificato: ${this.article.is_verified ? 'Sì ✓' : 'In revisione'}

🔗 FONTI E APPROFONDIMENTI:

• Articolo originale: ${this.article.url}
• Autore: ${this.article.author}
• Data pubblicazione: ${new Date(this.article.published_at || '').toLocaleDateString('it-IT', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    })}

💡 PERCHÉ DOVRESTI LEGGERLO:

Questa notizia è stata selezionata perché supera i nostri standard di qualità (${((this.article.quality_score || 0) * 100).toFixed(0)}%) 
e tratta temi rilevanti per chi si interessa di ${this.article.keywords?.slice(0, 3).join(', ')}.
    `.trim();
  }

  getCategoryContext(): string {
    const contexts: Record<string, string> = {
      'technology': 'il settore tecnologico e l\'innovazione digitale',
      'cybersecurity': 'la sicurezza informatica e la protezione dei dati',
      'science': 'la ricerca scientifica e le scoperte accademiche',
      'philosophy': 'la riflessione critica e il dibattito culturale',
      'ai': 'l\'intelligenza artificiale e il machine learning'
    };
    
    const keyword = this.article.keywords?.[0]?.toLowerCase() || 'general';
    return contexts[keyword] || 'l\'informazione di qualità';
  }

  getCategoryName(): string {
    return this.article.keywords?.[0] || 'General';
  }

  getHistoricalContext(): string {
    if (this.article.keywords?.includes('ai') || this.article.keywords?.includes('AI')) {
      return 'L\'intelligenza artificiale sta attraversando un momento di rapida evoluzione, con investimenti miliardari e questioni etiche emergenti.';
    }
    if (this.article.keywords?.includes('cybersecurity')) {
      return 'Gli attacchi informatici sono in costante aumento, con nuove vulnerabilità scoperte quotidianamente.';
    }
    return 'Questa notizia si inserisce nel contesto dell\'evoluzione tecnologica e sociale contemporanea.';
  }

  getActors(): string {
    return `• ${this.article.author}\n• Fonte: ${this.article.url.split('/')[2]}\n• Lettori e stakeholder del settore`;
  }

  getConsequences(): string {
    return 'Le implicazioni di questa notizia potrebbero influenzare policy makers, aziende tech e utenti finali nei prossimi mesi.';
  }

  getGlossary(): string {
    const terms: Record<string, string> = {
      'AI': 'Intelligenza Artificiale - sistemi che simulano capacità cognitive umane',
      'OpenAI': 'Azienda di ricerca AI creata nel 2015, sviluppatore di ChatGPT',
      'Cybersecurity': 'Insieme di pratiche per proteggere sistemi e dati da attacchi',
      'RSS': 'Really Simple Syndication - formato per distribuire contenuti web',
      'NLP': 'Natural Language Processing - elaborazione del linguaggio naturale'
    };
    
    let glossary = '';
    for (const [term, definition] of Object.entries(terms)) {
      if (this.article.title?.includes(term) || this.article.summary?.includes(term)) {
        glossary += `• ${term}: ${definition}\n`;
      }
    }
    
    return glossary || '• Termini tecnici rilevanti non rilevati in questa notizia';
  }

  onTabChange(index: number): void {
    if (index === 0) this.selectedLevel = 'quick';
    else if (index === 1) this.selectedLevel = 'standard';
    else this.selectedLevel = 'deep';
  }

  close(): void {
    this.dialogRef.close();
  }
}


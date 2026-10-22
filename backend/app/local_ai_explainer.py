"""
AI Locale integrata per generare spiegazioni approfondite degli articoli
Usa modelli NLP pre-addestrati (T5, GPT-2, DistilBERT) completamente locali
Nessuna chiamata API esterna - tutto funziona offline!

Esiste come fallback offline per evitare i cold start delle funzioni serverless, coprire interruzioni dei provider remoti
e azzerare i costi di chiamata: i modelli vengono caricati una sola volta per processo e poi riutilizzati dalla cache.
"""
import os
import re
from typing import Optional, Dict
import warnings
warnings.filterwarnings('ignore')

# Import opzionali - installa solo se necessario
# Le dipendenze sono opzionali: se assenti il modulo si degrada graziosamente alla spiegazione statica.
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ transformers non installato. Installa con: pip install transformers torch")

try:
    import torch
    TORCH_AVAILABLE = True
    # Verifica se CUDA è disponibile per GPU: l'inferenza su GPU riduce drasticamente i tempi di generazione.
    CUDA_AVAILABLE = torch.cuda.is_available()
    if CUDA_AVAILABLE:
        print(f"✅ GPU disponibile: {torch.cuda.get_device_name(0)}")
        print(f"   Memoria GPU: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    else:
        print("⚠️ CUDA non disponibile, userà CPU")
except ImportError:
    TORCH_AVAILABLE = False
    CUDA_AVAILABLE = False
    print("⚠️ torch non installato. Installa con: pip install torch")

# Cache per modelli caricati (evita ricaricare ogni volta)
# I modelli T5/GPT-2 pesano centinaia di MB e impiegano 1-2 minuti a caricarsi: tenerli in cache per processo
# evita un cold start su ogni articolo (critico in ambienti serverless).
_model_cache = {}
_tokenizer_cache = {}


def _load_t5_model():
    """Carica modello T5-small per text-to-text generation"""
    if 't5' in _model_cache:
        return _model_cache['t5'], _tokenizer_cache['t5']
    
    if not TRANSFORMERS_AVAILABLE or not TORCH_AVAILABLE:
        return None, None
    
    try:
        print("📥 Caricamento modello T5-small (prima volta, può richiedere 1-2 minuti)...")
        # t5-small (~240MB) è un modello seq2seq leggero, adatto a summarization anche su CPU.
        model_name = "t5-small"  # Modello leggero (~240MB)
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Sposta modello su GPU se disponibile (fin dall'inizio)
        if CUDA_AVAILABLE:
            model = model.to("cuda")
            print(f"✅ Modello T5 caricato su GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️ Modello T5 caricato su CPU (GPU non disponibile)")
        
        # Metti in modalità eval per inferenza più veloce
        model.eval()
        
        # Cache
        _model_cache['t5'] = model
        _tokenizer_cache['t5'] = tokenizer
        
        print("✅ Modello T5-small caricato!")
        return model, tokenizer
    except Exception as e:
        print(f"❌ Errore caricamento T5: {e}")
        return None, None


def _load_gpt2_model():
    """Carica modello GPT-2 per text generation"""
    if 'gpt2' in _model_cache:
        return _model_cache['gpt2'], _tokenizer_cache['gpt2']
    
    if not TRANSFORMERS_AVAILABLE or not TORCH_AVAILABLE:
        return None, None
    
    try:
        print("📥 Caricamento modello GPT-2 (prima volta, può richiedere 1-2 minuti)...")
        # gpt2 (~500MB) è un modello causale: genera testo in avanti, meno adatto alla summarization di T5 ma utile come fallback.
        model_name = "gpt2"  # Modello leggero (~500MB)
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Sposta modello su GPU se disponibile (fin dall'inizio)
        if CUDA_AVAILABLE:
            model = model.to("cuda")
            print(f"✅ Modello GPT-2 caricato su GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️ Modello GPT-2 caricato su CPU (GPU non disponibile)")
        
        # Metti in modalità eval
        model.eval()
        
        # Cache
        _model_cache['gpt2'] = model
        _tokenizer_cache['gpt2'] = tokenizer
        
        print("✅ Modello GPT-2 caricato!")
        return model, tokenizer
    except Exception as e:
        print(f"❌ Errore caricamento GPT-2: {e}")
        return None, None


def _generate_with_t5(prompt: str, max_length: int = 200) -> Optional[str]:
    """Genera testo usando T5-small"""
    model, tokenizer = _load_t5_model()
    if not model or not tokenizer:
        return None
    
    try:
        # T5 richiede un prefisso che indichi il task ("summarize:"); senza di esso l'output è inutilizzabile.
        input_text = f"summarize: {prompt}"
        
        # Tokenizza con truncation a 512 token: testi più lunghi vengono tagliati per stare nei limiti del modello T5.
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        
        # Modello è già su GPU se disponibile (caricato all'inizio)
        # Sposta solo gli input
        device = "cuda" if CUDA_AVAILABLE else "cpu"
        inputs = inputs.to(device)
        
        # Genera: num_beams=4 per output più coerente, no_repeat_ngram_size=2 contro le ripetizioni,
        # temperature 0.7 per varietà controllata, do_sample True per campionazione stoccastica;
        # max_length limita la lunghezza totale della generazione (default 200 token).
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=max_length,
                min_length=50,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2,
                temperature=0.7,
                do_sample=True
            )
        
        # Decodifica rimuovendo i token speciali (skip_special_tokens).
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.strip()
    except Exception as e:
        print(f"Errore generazione T5: {e}")
        return None


def _generate_with_gpt2(prompt: str, max_length: int = 200) -> Optional[str]:
    """Genera testo usando GPT-2"""
    model, tokenizer = _load_gpt2_model()
    if not model or not tokenizer:
        return None
    
    try:
        # Tokenizza con truncation a 400 token per l'input del prompt.
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=400, truncation=True)
        
        # Modello è già su GPU se disponibile (caricato all'inizio)
        # Sposta solo gli input
        device = "cuda" if CUDA_AVAILABLE else "cpu"
        inputs = inputs.to(device)
        
        # Genera: num_beams=4 per output più coerente, no_repeat_ngram_size=2 contro le ripetizioni,
        # temperature 0.7 per varietà controllata, do_sample True per campionazione stoccastica;
        # max_length limita la lunghezza totale della generazione (default 200 token).
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                # max_length qui è addizionale alla lunghezza del prompt (output totale = input + max_length).
                # pad_token_id sotto è impostato a eos_token_id per evitare avvisi di padding su GPT-2.
                max_length=inputs.shape[1] + max_length,
                min_length=inputs.shape[1] + 50,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=2,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decodifica (rimuovi il prompt originale)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Rimuovi il prompt originale dal risultato: GPT-2 rigenera anche il prompt iniziale, va scartato.
        if prompt in generated_text:
            generated_text = generated_text.replace(prompt, "").strip()
        
        return generated_text.strip()
    except Exception as e:
        print(f"Errore generazione GPT-2: {e}")
        return None


def _create_structured_explanation(article: Dict, explanation_type: str, base_text: str) -> str:
    """Crea spiegazione strutturata usando il testo generato dall'AI"""
    # Layout fisso attorno al testo del modello: le sezioni (cosa è successo, perché importante, impatto)
    # vengono riempite con slice di base_text a confini fissi (200/400/300/600 caratteri). Approccio euristico:
    # i modelli locali producono output brevi e non strutturati, quindi il confezionamento è fatto lato codice
    # invece che dal modello.
    
    title = article.get('title', '')
    summary = article.get('summary', '')
    keywords = article.get('keywords', [])
    author = article.get('author', 'Sconosciuto')
    quality_score = int((article.get('quality_score', 0.7) * 100))
    reading_time = article.get('reading_time_minutes', 3)
    
    if explanation_type == "quick":
        return f"""🎯 IN BREVE:

{title}

{base_text[:200] if base_text else summary[:200]}

📍 PERCHÉ È IMPORTANTE:
{base_text[200:400] if len(base_text) > 200 else 'Questa notizia tratta di ' + ', '.join(keywords[:3]) + ' ed è rilevante per il settore.'}

⭐ Quality Score: {quality_score}%
⏱️ Tempo lettura: {reading_time} minuti
🔗 Fonte: {author}"""
    
    elif explanation_type == "standard":
        return f"""📰 CONTESTO:

{title}

{summary}

🔍 COSA SIGNIFICA:

{base_text[:300] if base_text else 'Questa notizia riguarda ' + ', '.join(keywords[:3]) + '.'}

👥 CHI È COINVOLTO:

• Autore: {author}
• Fonte: {article.get('url', '').split('/')[2] if article.get('url') else 'Non disponibile'}
• Categoria: {keywords[0] if keywords else 'Generale'}
• Lingua: {article.get('language', 'it').upper()}

📊 ANALISI QUALITÀ:

• Quality Score: {quality_score}% - {'Eccellente' if quality_score >= 85 else 'Molto buona' if quality_score >= 75 else 'Buona'}
• Tempo lettura: {reading_time} minuti
• Verificato: {'Sì ✓' if article.get('is_verified') else 'In revisione'}

🎓 PAROLE CHIAVE:
{', '.join(keywords) if keywords else 'Nessuna'}

🌍 IMPATTO:

{base_text[300:600] if len(base_text) > 300 else 'Questa notizia è stata selezionata perché supera i nostri standard di qualità e tratta temi rilevanti.'}

🔗 PER APPROFONDIRE:
Leggi l'articolo completo su: {article.get('url', '')}"""
    
    else:  # deep
        content = article.get('content', '')[:800] if article.get('content') else summary[:800]
        
        return f"""📚 ANALISI APPROFONDITA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{title}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 SINTESI COMPLETA:

{summary}

{content + '...' if content else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 ANALISI AI GENERATA:

{base_text if base_text else 'Analisi in corso...'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 ATTORI E STAKEHOLDER:

• Autore/Fonte: {author}
• Piattaforma: {article.get('url', '').split('/')[2] if article.get('url') else 'Non disponibile'}
• Target audience: Lettori interessati a {keywords[0] if keywords else 'informazione'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 CONSEGUENZE E IMPLICAZIONI:

Le implicazioni di questa notizia potrebbero influenzare:
• Policy makers e regolatori (nuove normative)
• Aziende del settore (strategie e investimenti)
• Professionisti e sviluppatori (competenze richieste)
• Utenti finali e cittadini (impatto quotidiano)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 METRICHE DI QUALITÀ:

• Quality Score: {quality_score}%
• Tempo lettura: {reading_time} minuti
• Lingua: {article.get('language', 'it').upper()}
• Status: {'Verificato ✓' if article.get('is_verified') else 'In revisione'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 PERCHÉ LEGGERE QUESTO ARTICOLO:

Questa notizia è stata curata e selezionata dal nostro sistema perché rappresenta 
contenuto di alta qualità ({quality_score}%) su temi di {keywords[0] if keywords else 'informazione'} 
rilevanti per i lettori di NewsFlow."""


def generate_explanation_local_ai(article: Dict, explanation_type: str = "quick") -> str:
    """
    Genera spiegazione usando AI locale integrata (T5 o GPT-2)
    
    Args:
        article: Dizionario con dati dell'articolo
        explanation_type: "quick" (30s), "standard" (3min), "deep" (approfondito)
    
    Returns:
        Spiegazione generata con AI locale
    """
    if not TRANSFORMERS_AVAILABLE or not TORCH_AVAILABLE:
        return _generate_fallback_explanation(article, explanation_type)
    
    # Prepara prompt in base al tipo
    # I campi dell'articolo vengono troncati (summary 800, content 1000, summary 400 per quick) per stare
    # nei limiti di lunghezza di input dei modelli locali (T5 accetta al massimo 512 token).
    title = article.get('title', '')
    summary = article.get('summary', '')[:800]
    keywords = ', '.join(article.get('keywords', [])[:5])
    content = article.get('content', '')[:1000] if article.get('content') else summary[:1000]
    
    if explanation_type == "quick":
        prompt = f"""Spiega brevemente questa notizia in italiano:

Titolo: {title}
Riassunto: {summary[:400]}

Cosa è successo e perché è importante?"""
        max_length = 150
    
    elif explanation_type == "standard":
        prompt = f"""Spiega in dettaglio questa notizia in italiano:

Titolo: {title}
Riassunto: {summary}
Parole chiave: {keywords}

Fornisci contesto, chi è coinvolto e l'impatto."""
        max_length = 300
    
    else:  # deep
        prompt = f"""Fornisci un'analisi approfondita di questa notizia in italiano:

Titolo: {title}
Riassunto: {summary}
Contenuto: {content}
Parole chiave: {keywords}

Analizza il contesto storico, gli attori coinvolti, le conseguenze e le prospettive future."""
        max_length = 500
    
    # Prova prima T5 (migliore per summarization grazie al task "summarize:")
    generated_text = _generate_with_t5(prompt, max_length)
    
    # Fallback a GPT-2 se T5 non funziona o produce testo troppo breve (< 50 caratteri).
    if not generated_text or len(generated_text) < 50:
        print("⚠️ T5 non ha generato testo sufficiente, provo GPT-2...")
        generated_text = _generate_with_gpt2(prompt, max_length)
    
    # Se ancora nulla, usa fallback statico puramente heuristico (nessun modello, nessuna rete).
    if not generated_text or len(generated_text) < 50:
        print("⚠️ AI locale non disponibile, uso spiegazione statica")
        return _generate_fallback_explanation(article, explanation_type)
    
    # Crea spiegazione strutturata
    return _create_structured_explanation(article, explanation_type, generated_text)


def _generate_fallback_explanation(article: Dict, explanation_type: str) -> str:
    """Fallback a spiegazione statica se AI non disponibile"""
    # Spiegazione puramente heuristica costruita dai campi dell'articolo: nessun modello, nessuna rete,
    # usata quando transformers/torch mancano o i modelli locali non producono output valido.
    title = article.get('title', '')
    summary = article.get('summary', '')
    keywords = article.get('keywords', [])
    author = article.get('author', 'Sconosciuto')
    quality_score = int((article.get('quality_score', 0.7) * 100))
    reading_time = article.get('reading_time_minutes', 3)
    
    if explanation_type == "quick":
        return f"""🎯 IN BREVE:

{title}

{summary[:250]}...

📍 PERCHÉ È IMPORTANTE:
Questa notizia tratta di {', '.join(keywords[:3]) if keywords else 'informazione'} ed è rilevante.

⭐ Quality Score: {quality_score}%
⏱️ Tempo lettura: {reading_time} minuti
🔗 Fonte: {author}"""
    
    elif explanation_type == "standard":
        return f"""📰 CONTESTO:

{title}

{summary}

🔍 COSA SIGNIFICA:

Questa notizia riguarda {', '.join(keywords[:3]) if keywords else 'informazione'}.

👥 CHI È COINVOLTO:
• Autore: {author}
• Categoria: {keywords[0] if keywords else 'Generale'}

📊 ANALISI QUALITÀ:
• Quality Score: {quality_score}%
• Tempo lettura: {reading_time} minuti"""
    
    else:  # deep
        return f"""📚 ANALISI APPROFONDITA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{title}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 SINTESI COMPLETA:

{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 PERCHÉ LEGGERE QUESTO ARTICOLO:

Questa notizia è stata curata perché rappresenta contenuto di alta qualità ({quality_score}%) 
su temi di {keywords[0] if keywords else 'informazione'} rilevanti per i lettori di NewsFlow."""


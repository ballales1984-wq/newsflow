"""
Servizio AI per generare spiegazioni approfondite degli articoli
Supporta versioni GRATUITE di:
- Ollama (locale, completamente gratuito) ⭐ CONSIGLIATO
- Hugging Face Inference API (gratuita)
- DeepSeek (tier gratuito)
- ChatGPT (opzionale, se API key disponibile)
"""
import os
import requests
import json
from typing import Optional, Dict

# Configurazione API Keys (opzionali per servizi gratuiti)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Opzionale
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Opzionale (tier gratuito disponibile)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")  # Opzionale (gratuita con account)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # Locale, completamente gratuito

# Nessuna chiave API richiesta per Ollama: punta all'istanza locale dell'utente (default localhost:11434).
# OPENAI_API_KEY, DEEPSEEK_API_KEY e HUGGINGFACE_API_KEY vengono lette solo da variabili d'ambiente;
# quando mancano il relativo provider restituisce None e la catena di fallback prova il provider successivo.


def generate_explanation_with_chatgpt(article: Dict, explanation_type: str = "quick") -> Optional[str]:
    """
    Genera spiegazione usando ChatGPT (OpenAI)
    
    Args:
        article: Dizionario con dati dell'articolo
        explanation_type: "quick" (30s), "standard" (3min), "deep" (approfondito)
    
    Returns:
        Spiegazione generata o None se errore
    """
    if not OPENAI_API_KEY:
        return None  # Nessuna chiave: salta il provider, il caller proverà il successivo nella catena di fallback
    
    try:
        # Prepara prompt in base al tipo
        if explanation_type == "quick":
            prompt = f"""Spiega questa notizia in modo breve e chiaro (max 150 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:500]}

Fornisci:
- Cosa è successo (in 2-3 frasi)
- Perché è importante
- Impatto principale

Rispondi in italiano, in modo chiaro e accessibile."""
        
        elif explanation_type == "standard":
            prompt = f"""Spiega questa notizia in modo dettagliato (max 400 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:800]}
Keywords: {', '.join(article.get('keywords', [])[:5])}

Fornisci:
1. CONTESTO: Cosa è successo e perché è importante
2. CHI È COINVOLTO: Attori principali e stakeholder
3. IMPATTO: Conseguenze immediate e a medio termine
4. PERCHÉ LEGGERE: Perché questa notizia è rilevante

Rispondi in italiano, ben strutturato e informativo."""
        
        else:  # deep
            prompt = f"""Fornisci un'analisi approfondita di questa notizia (max 800 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:1000]}
Contenuto: {article.get('content', '')[:1500] if article.get('content') else article.get('summary', '')[:1000]}
Keywords: {', '.join(article.get('keywords', []))}
Categoria: {article.get('keywords', [''])[0] if article.get('keywords') else 'Generale'}

Fornisci un'analisi completa con:
1. CONTESTO STORICO: Background e precedenti rilevanti
2. ANALISI DETTAGLIATA: Cosa significa questa notizia nel contesto più ampio
3. ATTORI E STAKEHOLDER: Chi è coinvolto e perché
4. CONSEGUENZE E IMPLICAZIONI: Impatto a breve, medio e lungo termine
5. PROSPETTIVE FUTURE: Cosa potrebbe succedere dopo
6. GLOSSARIO: Spiega i termini tecnici chiave
7. PERCHÉ È IMPORTANTE: Perché questa notizia merita attenzione

Rispondi in italiano, ben strutturato, professionale ma accessibile."""
        
        # Endpoint OpenAI Chat Completions (https://api.openai.com/v1/chat/completions); autenticazione Bearer tramite OPENAI_API_KEY.
        # Il ruolo system fissa il tono (giornalista esperto) e vincola la risposta all'italiano (non c'è un passo di traduzione esplicito);
        # il ruolo user passa l'articolo con la struttura richiesta: cosa è successo, perché è importante, impatto principale.
        # gpt-4o-mini: modello a basso costo adatto a sintesi di notizie. temperature 0.7 bilancia coerenza e varietà.
        # max_tokens scalato per tipo (quick 1000, standard 2000, deep 3000) per rispettare i vincoli di lunghezza del prompt.
        # timeout 30s: oltre tale limite la richiesta si interrompe e il caller prova il provider successivo.
        # Chiamata API OpenAI
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",  # Modello economico ma efficace
            "messages": [
                {
                    "role": "system",
                    "content": "Sei un giornalista esperto che spiega notizie in modo chiaro, accurato e accessibile. Rispondi sempre in italiano."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000 if explanation_type == "quick" else (2000 if explanation_type == "standard" else 3000)
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            # Estrazione difensiva: chiavi mancanti restituiscono default vuoti invece di sollevare eccezione.
            # Risposta malformata (es. choices vuoto) restituisce stringa vuota: il caller la tratta come assenza di spiegazione
            # e prosegue con il provider successivo nella catena di fallback.
            return data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            print(f"Errore OpenAI: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Errore chiamata ChatGPT: {e}")
        return None  # Eccezione assorbita senza fallback interno: il chiamante gestisce il passaggio al provider successivo


def generate_explanation_with_huggingface(article: Dict, explanation_type: str = "quick") -> Optional[str]:
    """
    Genera spiegazione usando Hugging Face Inference API (GRATUITA)
    
    Usa modelli gratuiti come:
    - meta-llama/Llama-3.2-3B-Instruct
    - microsoft/Phi-3-mini-4k-instruct
    - mistralai/Mistral-7B-Instruct-v0.2
    
    Args:
        article: Dizionario con dati dell'articolo
        explanation_type: "quick" (30s), "standard" (3min), "deep" (approfondito)
    
    Returns:
        Spiegazione generata o None se errore
    """
    # Hugging Face è gratuito ma richiede API key (gratuita da ottenere)
    if not HUGGINGFACE_API_KEY:
        return None  # Nessuna chiave: salta il provider
    
    try:
        # Prepara prompt
        if explanation_type == "quick":
            prompt = f"""Spiega questa notizia in modo breve e chiaro (max 150 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:500]}

Fornisci:
- Cosa è successo (in 2-3 frasi)
- Perché è importante
- Impatto principale

Rispondi in italiano, in modo chiaro e accessibile."""
        
        elif explanation_type == "standard":
            prompt = f"""Spiega questa notizia in modo dettagliato (max 400 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:800]}
Keywords: {', '.join(article.get('keywords', [])[:5])}

Fornisci:
1. CONTESTO: Cosa è successo e perché è importante
2. CHI È COINVOLTO: Attori principali e stakeholder
3. IMPATTO: Conseguenze immediate e a medio termine
4. PERCHÉ LEGGERE: Perché questa notizia è rilevante

Rispondi in italiano, ben strutturato e informativo."""
        
        else:  # deep
            prompt = f"""Fornisci un'analisi approfondita di questa notizia (max 800 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:1000]}
Contenuto: {article.get('content', '')[:1500] if article.get('content') else article.get('summary', '')[:1000]}
Keywords: {', '.join(article.get('keywords', []))}
Categoria: {article.get('keywords', [''])[0] if article.get('keywords') else 'Generale'}

Fornisci un'analisi completa con:
1. CONTESTO STORICO: Background e precedenti rilevanti
2. ANALISI DETTAGLIATA: Cosa significa questa notizia nel contesto più ampio
3. ATTORI E STAKEHOLDER: Chi è coinvolto e perché
4. CONSEGUENZE E IMPLICAZIONI: Impatto a breve, medio e lungo termine
5. PROSPETTIVE FUTURE: Cosa potrebbe succedere dopo
6. GLOSSARIO: Spiega i termini tecnici chiave
7. PERCHÉ È IMPORTANTE: Perché questa notizia merita attenzione

Rispondi in italiano, ben strutturato, professionale ma accessibile."""
        
        # Usa modello gratuito di Hugging Face
        # Prova prima con Llama 3.2 (gratuito e potente)
        # Catena di fallback tra modelli: se uno fallisce o non è caricato si passa al successivo.
        models = [
            "meta-llama/Llama-3.2-3B-Instruct",
            "microsoft/Phi-3-mini-4k-instruct",
            "mistralai/Mistral-7B-Instruct-v0.2"
        ]
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Endpoint Inference API: https://api-inference.huggingface.co/models/{model};
        # timeout 60s perché i modelli gratuiti possono impiegare tempo a caricarsi a freddo.
        
        for model in models:
            try:
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 500 if explanation_type == "quick" else (1000 if explanation_type == "standard" else 2000),
                        "temperature": 0.7,
                        "return_full_text": False
                    }
                }
                
                response = requests.post(
                    f"https://api-inference.huggingface.co/models/{model}",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # La risposta può essere lista o dict a seconda del modello; entrambe le forme vengono gestite.
                    # generated_text vuoto o assente significa risposta non valida: si prova il modello successivo.
                    if isinstance(data, list) and len(data) > 0:
                        result = data[0].get('generated_text', '')
                        if result:
                            return result
                    elif isinstance(data, dict):
                        result = data.get('generated_text', '')
                        if result:
                            return result
                elif response.status_code == 503:
                    # Modello ancora in caricamento sull'infrastruttura gratuita: prova il prossimo modello invece di fallire.
                    continue
                else:
                    print(f"Errore Hugging Face ({model}): {response.status_code}")
                    continue
                    
            except Exception as e:
                print(f"Errore con modello {model}: {e}")
                continue
        
        return None  # Tutti i modelli Hugging Face hanno fallito: il caller tenta il provider successivo
            
    except Exception as e:
        print(f"Errore chiamata Hugging Face: {e}")
        return None


def generate_explanation_with_ollama(article: Dict, explanation_type: str = "quick") -> Optional[str]:
    """
    Genera spiegazione usando Ollama (LOCALE, COMPLETAMENTE GRATUITO)
    
    Richiede Ollama installato localmente:
    - Download: https://ollama.ai
    - Modelli gratuiti: llama3.2, mistral, phi3, etc.
    
    Args:
        article: Dizionario con dati dell'articolo
        explanation_type: "quick" (30s), "standard" (3min), "deep" (approfondito)
    
    Returns:
        Spiegazione generata o None se errore
    """
    try:
        # Prepara prompt OTTIMIZZATI per velocità (più brevi e diretti)
        if explanation_type == "quick":
            # Prompt molto breve per risposta rapida
            prompt = f"""Spiega brevemente in italiano (max 3 frasi):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:300]}

Cosa è successo e perché è importante?"""
        
        elif explanation_type == "standard":
            # Prompt medio, strutturato ma conciso
            prompt = f"""Spiega in italiano:

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:500]}
Keywords: {', '.join(article.get('keywords', [])[:3])}

Fornisci brevemente: cosa è successo, chi è coinvolto, perché è importante."""
        
        else:  # deep
            # Prompt più completo ma ancora ottimizzato
            prompt = f"""Analisi approfondita in italiano:

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:600]}
Keywords: {', '.join(article.get('keywords', [])[:5])}

Fornisci: contesto, attori coinvolti, conseguenze, perché è importante."""
        
        # Prova modelli Ollama comuni (in ordine di preferenza)
        # Ordine dal modello più piccolo/veloce a quelli più grandi: il primo disponibile viene usato,
        # evitando di attendere modelli pesanti su macchine con poche risorse.
        models = ["gemma3:1b", "phi3", "llama3.2", "mistral", "llama3"]
        
        # Riduci drasticamente i token per risposte più veloci (l'inferenza locale su CPU è lenta)
        max_tokens = {
            "quick": 100,      # Ridotto da 500 a 100
            "standard": 200,   # Ridotto da 1000 a 200
            "deep": 400        # Ridotto da 2000 a 400
        }
        
        for model in models:
            try:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": max_tokens.get(explanation_type, 200),
                        "top_p": 0.9,
                        "top_k": 40,
                        "repeat_penalty": 1.1
                    }
                }
                
                response = requests.post(
                    f"{OLLAMA_URL}/api/generate",
                    json=payload,
                    timeout=30  # Ridotto da 120 a 30 secondi per non bloccare la richiesta HTTP
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data.get('response', '')
                    if result:
                        return result
                else:
                    # Modello non caricato su questa istanza Ollama: prova il prossimo della lista.
                    continue
                    
            except requests.exceptions.ConnectionError:
                # Ollama non è in esecuzione: inutile provare altri modelli locali, esce subito.
                return None
            except Exception as e:
                print(f"Errore con modello Ollama {model}: {e}")
                continue
        
        return None  # Nessun modello Ollama disponibile: il caller passa al provider successivo
            
    except Exception as e:
        print(f"Errore chiamata Ollama: {e}")
        return None


def generate_explanation_with_deepseek(article: Dict, explanation_type: str = "quick") -> Optional[str]:
    """
    Genera spiegazione usando DeepSeek
    
    Args:
        article: Dizionario con dati dell'articolo
        explanation_type: "quick" (30s), "standard" (3min), "deep" (approfondito)
    
    Returns:
        Spiegazione generata o None se errore
    """
    if not DEEPSEEK_API_KEY:
        return None  # Nessuna chiave: salta il provider
    
    try:
        # Stesso prompt di ChatGPT
        if explanation_type == "quick":
            prompt = f"""Spiega questa notizia in modo breve e chiaro (max 150 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:500]}

Fornisci:
- Cosa è successo (in 2-3 frasi)
- Perché è importante
- Impatto principale

Rispondi in italiano, in modo chiaro e accessibile."""
        
        elif explanation_type == "standard":
            prompt = f"""Spiega questa notizia in modo dettagliato (max 400 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:800]}
Keywords: {', '.join(article.get('keywords', [])[:5])}

Fornisci:
1. CONTESTO: Cosa è successo e perché è importante
2. CHI È COINVOLTO: Attori principali e stakeholder
3. IMPATTO: Conseguenze immediate e a medio termine
4. PERCHÉ LEGGERE: Perché questa notizia è rilevante

Rispondi in italiano, ben strutturato e informativo."""
        
        else:  # deep
            prompt = f"""Fornisci un'analisi approfondita di questa notizia (max 800 parole):

Titolo: {article.get('title', '')}
Riassunto: {article.get('summary', '')[:1000]}
Contenuto: {article.get('content', '')[:1500] if article.get('content') else article.get('summary', '')[:1000]}
Keywords: {', '.join(article.get('keywords', []))}
Categoria: {article.get('keywords', [''])[0] if article.get('keywords') else 'Generale'}

Fornisci un'analisi completa con:
1. CONTESTO STORICO: Background e precedenti rilevanti
2. ANALISI DETTAGLIATA: Cosa significa questa notizia nel contesto più ampio
3. ATTORI E STAKEHOLDER: Chi è coinvolto e perché
4. CONSEGUENZE E IMPLICAZIONI: Impatto a breve, medio e lungo termine
5. PROSPETTIVE FUTURE: Cosa potrebbe succedere dopo
6. GLOSSARIO: Spiega i termini tecnici chiave
7. PERCHÉ È IMPORTANTE: Perché questa notizia merita attenzione

Rispondi in italiano, ben strutturato, professionale ma accessibile."""
        
        # Chiamata API DeepSeek (https://api.deepseek.com/v1/chat/completions); modello deepseek-chat.
        # Stesse regole di system/user di ChatGPT (giornalista esperto, risposta sempre in italiano).
        # temperature 0.7 e max_tokens scalati per tipo (quick 1000, standard 2000, deep 3000);
        # timeout 30s, oltre il quale il caller tenta il provider successivo.
        # Chiamata API DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Sei un giornalista esperto che spiega notizie in modo chiaro, accurato e accessibile. Rispondi sempre in italiano."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000 if explanation_type == "quick" else (2000 if explanation_type == "standard" else 3000)
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            print(f"Errore DeepSeek: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Errore chiamata DeepSeek: {e}")
        return None  # Eccezione assorbita: il chiamante gestisce il fallback al provider successivo


def generate_explanation(article: Dict, explanation_type: str = "quick") -> str:
    """
    Genera spiegazione usando servizi AI GRATUITI con fallback automatico
    
    Ordine di priorità (tutti gratuiti):
    1. Ollama (locale, completamente gratuito) ⭐ PRIMA SCELTA - GIÀ INSTALLATO!
    2. AI Locale Integrata (T5/GPT-2) - COMPLETAMENTE OFFLINE
    3. Hugging Face (API gratuita) - BUONA QUALITÀ
    4. DeepSeek (tier gratuito) - ALTA QUALITÀ
    5. ChatGPT (solo se API key disponibile) - MIGLIORE QUALITÀ
    
    Args:
        article: Dizionario con dati dell'articolo
        explanation_type: "quick", "standard", "deep"
    
    Returns:
        Spiegazione generata (con fallback a spiegazione statica se AI non disponibile)
    """
    # 1. Prova Ollama (locale, completamente gratuito) - PRIMA SCELTA
    explanation = generate_explanation_with_ollama(article, explanation_type)
    if explanation:
        print("✅ Usato Ollama (locale, gratuito, già installato)")
        return explanation
    
    # 2. Prova AI Locale Integrata (T5/GPT-2) - COMPLETAMENTE OFFLINE
    try:
        from app.local_ai_explainer import generate_explanation_local_ai
        explanation = generate_explanation_local_ai(article, explanation_type)
        # Soglia di 100 caratteri: scarta output troppo brevi per essere utili come spiegazione.
        if explanation and len(explanation) > 100:  # Verifica che sia una spiegazione valida
            print("✅ Usato AI Locale Integrata (T5/GPT-2, completamente offline)")
            return explanation
    except ImportError:
        print("⚠️ AI Locale non disponibile (transformers/torch non installati)")
        # ImportError assorbito: senza dipendenze il fallback chain continua con i provider remoti.
    except Exception as e:
        print(f"⚠️ Errore AI Locale: {e}")
    
    # 3. Prova Hugging Face (API gratuita)
    explanation = generate_explanation_with_huggingface(article, explanation_type)
    if explanation:
        print("✅ Usato Hugging Face (gratuito)")
        return explanation
    
    # 4. Prova DeepSeek (tier gratuito disponibile)
    explanation = generate_explanation_with_deepseek(article, explanation_type)
    if explanation:
        print("✅ Usato DeepSeek (tier gratuito)")
        return explanation
    
    # 5. Prova ChatGPT (solo se API key disponibile, non gratuito)
    explanation = generate_explanation_with_chatgpt(article, explanation_type)
    if explanation:
        print("✅ Usato ChatGPT (richiede API key)")
        return explanation
    
    # Fallback finale: spiegazione statica migliorata
    # Usata quando nessun provider (locale o remoto) è disponibile; garantisce che l'API restituisca sempre una spiegazione.
    print("⚠️ Nessun servizio AI disponibile, uso spiegazione statica")
    return _generate_static_explanation(article, explanation_type)


def _generate_static_explanation(article: Dict, explanation_type: str) -> str:
    """Genera spiegazione statica migliorata come fallback"""
    # Costruita esclusivamente dai campi dell'articolo (titolo, riassunto, keywords, autore): nessun modello,
    # zero latenza e zero costo. quality_score default 0.7 e reading_time default 3 quando i campi mancano.
    if explanation_type == "quick":
        return f"""🎯 IN BREVE:

{article.get('title', '')}

{article.get('summary', '')[:250]}...

📍 PERCHÉ È IMPORTANTE:
Questa notizia tratta di {', '.join(article.get('keywords', [])[:3])} ed è rilevante per il settore {article.get('keywords', [''])[0] if article.get('keywords') else 'informazione'}.

⭐ Quality Score: {int((article.get('quality_score', 0.7) * 100))}%
⏱️ Tempo lettura: {article.get('reading_time_minutes', 3)} minuti
🔗 Fonte: {article.get('author', 'Sconosciuto')}"""
    
    elif explanation_type == "standard":
        return f"""📰 CONTESTO:

{article.get('title', '')}

{article.get('summary', '')}

🔍 COSA SIGNIFICA:

Questa notizia riguarda {', '.join(article.get('keywords', [])[:3])}. 
È stata pubblicata da {article.get('author', 'Sconosciuto')} e selezionata per la sua alta qualità ({int((article.get('quality_score', 0.7) * 100))}%).

👥 CHI È COINVOLTO:
• Autore: {article.get('author', 'Sconosciuto')}
• Fonte: {article.get('url', '').split('/')[2] if article.get('url') else 'Non disponibile'}
• Data: {article.get('published_at', 'Non disponibile')}
• Categoria: {article.get('keywords', [''])[0] if article.get('keywords') else 'Generale'}

📊 ANALISI QUALITÀ:
• Quality Score: {int((article.get('quality_score', 0.7) * 100))}%
• Tempo lettura: {article.get('reading_time_minutes', 3)} minuti
• Verificato: {'Sì ✓' if article.get('is_verified') else 'In revisione'}

🎓 PAROLE CHIAVE:
{', '.join(article.get('keywords', []))}

🌍 IMPATTO:

Questa notizia è stata selezionata perché supera i nostri standard di qualità 
e tratta temi rilevanti nell'attuale panorama {article.get('keywords', [''])[0] if article.get('keywords') else 'informazione'}."""
    
    else:  # deep
        return f"""📚 ANALISI APPROFONDITA:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{article.get('title', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 SINTESI COMPLETA:

{article.get('summary', '')}

{article.get('content', '')[:800] + '...' if article.get('content') else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 CONTESTO E BACKGROUND:

Questa notizia si inserisce nel contesto dell'evoluzione tecnologica e sociale contemporanea, 
con particolare rilevanza per il settore {article.get('keywords', [''])[0] if article.get('keywords') else 'informazione'}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥 ATTORI E STAKEHOLDER:

• Autore/Fonte: {article.get('author', 'Sconosciuto')}
• Piattaforma: {article.get('url', '').split('/')[2] if article.get('url') else 'Non disponibile'}
• Target audience: Lettori interessati a {article.get('keywords', [''])[0] if article.get('keywords') else 'informazione'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌍 CONSEGUENZE E IMPLICAZIONI:

Le implicazioni di questa notizia potrebbero influenzare:
• Policy makers e regolatori (nuove normative)
• Aziende del settore (strategie e investimenti)
• Professionisti e sviluppatori (competenze richieste)
• Utenti finali e cittadini (impatto quotidiano)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 METRICHE DI QUALITÀ:

• Quality Score: {int((article.get('quality_score', 0.7) * 100))}%
• Tempo lettura: {article.get('reading_time_minutes', 3)} minuti
• Lingua: {article.get('language', 'it').upper()}
• Status: {'Verificato ✓' if article.get('is_verified') else 'In revisione'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 PERCHÉ LEGGERE QUESTO ARTICOLO:

Questa notizia è stata curata e selezionata dal nostro sistema perché rappresenta 
contenuto di alta qualità ({int((article.get('quality_score', 0.7) * 100))}%) 
su temi di {article.get('keywords', [''])[0] if article.get('keywords') else 'informazione'} 
rilevanti per i lettori di NewsFlow."""


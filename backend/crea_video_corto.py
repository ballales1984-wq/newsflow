#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script per creare video corto da 2 minuti"""
import sys
import os
import json

# Aggiungi percorso backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from youtube_short_video_generator import create_short_video_2min
    
    # Carica articoli
    news_file = 'final_news_italian.json'
    if not os.path.exists(news_file):
        print(f"❌ File non trovato: {news_file}")
        sys.exit(1)
    
    print("📸 Carico articoli...")
    with open(news_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        articles = data.get('items', [])
    
    print(f"✅ Articoli caricati: {len(articles)}")
    print("📹 Creo video corto da 2 minuti...")
    print("   (Questo richiederà alcuni minuti)")
    print("")
    
    # Crea video
    video_path = create_short_video_2min(articles)
    
    if video_path:
        print("")
        print("✅ VIDEO CREATO CON SUCCESSO!")
        print(f"   File: {video_path}")
        file_size = os.path.getsize(video_path) / (1024 * 1024)
        print(f"   Dimensione: {file_size:.2f} MB")
    else:
        print("")
        print("❌ Errore durante la creazione del video")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ Errore import: {e}")
    print("   Installa le dipendenze: pip install moviepy gtts pillow")
    sys.exit(1)
except Exception as e:
    print(f"❌ Errore: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


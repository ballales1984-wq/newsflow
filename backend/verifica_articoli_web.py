#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verifica articoli e immagini nel file JSON"""
import json
import os
import sys

# Fix encoding per Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verifica_articoli():
    """Verifica articoli e immagini"""
    paths = [
        'final_news_italian.json',
        'api/final_news_italian.json',
        'backend/final_news_italian.json'
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"\n{'='*60}")
            print(f"📁 File: {path}")
            print(f"{'='*60}")
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                articles = data.get('items', [])
                total = len(articles)
                with_img = [a for a in articles if a.get('image_url')]
                without_img = total - len(with_img)
                
                print(f"✅ Totale articoli: {total}")
                print(f"🖼️  Con immagine: {len(with_img)} ({len(with_img)*100//total if total > 0 else 0}%)")
                print(f"❌ Senza immagine: {without_img} ({without_img*100//total if total > 0 else 0}%)")
                
                print(f"\n📋 Prime 5 articoli:")
                for i, article in enumerate(articles[:5], 1):
                    title = article.get('title', 'N/A')[:60]
                    img = article.get('image_url', '')
                    has_img = '✅' if img else '❌'
                    print(f"  {i}. {title}... {has_img}")
                    if img:
                        print(f"     URL: {img[:80]}...")
                
                # Articoli senza immagine
                if without_img > 0:
                    print(f"\n⚠️  Articoli senza immagine (primi 3):")
                    no_img_articles = [a for a in articles if not a.get('image_url')]
                    for i, article in enumerate(no_img_articles[:3], 1):
                        print(f"  {i}. {article.get('title', 'N/A')[:60]}...")
                
            except Exception as e:
                print(f"❌ Errore lettura: {e}")
        else:
            print(f"❌ File non trovato: {path}")

if __name__ == '__main__':
    verifica_articoli()


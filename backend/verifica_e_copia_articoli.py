"""Script per verificare e copiare gli articoli aggiornati"""
import json
import os
import shutil

# Verifica file backend
backend_file = 'final_news_italian.json'
if os.path.exists(backend_file):
    try:
        with open(backend_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('items', [])
            print(f"✅ File backend trovato:")
            print(f"   - Articoli: {len(articles)}")
            print(f"   - Ultimo aggiornamento: {data.get('updated_at', 'N/A')}")
            print(f"\n   Prime 3 notizie:")
            for i, a in enumerate(articles[:3], 1):
                print(f"   {i}. {a.get('title', 'N/A')[:70]}...")
            
            # Copia nella root se necessario
            root_file = os.path.join('..', 'final_news_italian.json')
            if os.path.exists(os.path.dirname(root_file)):
                shutil.copy2(backend_file, root_file)
                print(f"\n✅ File copiato in: {root_file}")
            
            # Copia in api/ se esiste
            api_dir = os.path.join('..', 'api')
            if os.path.exists(api_dir):
                api_file = os.path.join(api_dir, 'final_news_italian.json')
                shutil.copy2(backend_file, api_file)
                print(f"✅ File copiato in: {api_file}")
            
            print(f"\n✨ File pronto per essere utilizzato!")
    except Exception as e:
        print(f"❌ Errore lettura file: {e}")
else:
    print(f"❌ File {backend_file} non trovato in backend/")


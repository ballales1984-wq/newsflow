"""Test immagini nell'API"""
import requests
import json

url = 'https://braccobaldo.pythonanywhere.com/api/v1/articles?limit=10'
print("🧪 Test immagini API PythonAnywhere...")
print(f"URL: {url}\n")

try:
    response = requests.get(url, timeout=15)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        
        print(f"\n📊 Analisi {len(items)} articoli:")
        with_img = [item for item in items if item.get('image_url')]
        without_img = [item for item in items if not item.get('image_url')]
        
        print(f"   ✅ Con immagini: {len(with_img)}")
        print(f"   ❌ Senza immagini: {len(without_img)}")
        
        if with_img:
            print("\n🖼️  Esempi con immagini:")
            for i, item in enumerate(with_img[:3], 1):
                print(f"   {i}. {item.get('title', 'N/A')[:50]}...")
                print(f"      Image: {item.get('image_url', 'N/A')[:80]}...")
        else:
            print("\n⚠️  Nessuna immagine trovata nell'API!")
            print("   Il file su PythonAnywhere potrebbe non essere aggiornato.")
            print("   Esegui: cd ~/newsflow && git pull")
    else:
        print(f"❌ Errore: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
        
except Exception as e:
    print(f"❌ Errore connessione: {e}")


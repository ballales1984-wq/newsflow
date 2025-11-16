"""Test API PythonAnywhere"""
import requests
import json

url = 'https://braccobaldo.pythonanywhere.com/api/v1/articles?limit=1'

print("🧪 Test API PythonAnywhere...")
print(f"URL: {url}\n")

try:
    response = requests.get(url, timeout=15)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API FUNZIONA!")
        print(f"\n📊 Dati ricevuti:")
        print(f"   Total: {data.get('total', 0)} articoli")
        print(f"   Items: {len(data.get('items', []))} articoli nella risposta")
        
        if data.get('items'):
            first = data['items'][0]
            print(f"\n📰 Primo articolo:")
            print(f"   ID: {first.get('id')}")
            print(f"   Titolo: {first.get('title', 'N/A')[:60]}...")
            print(f"   Immagine: {'✅' if first.get('image_url') else '❌'}")
        
        print(f"\n🌐 Backend online e funzionante!")
        print(f"   URL: https://braccobaldo.pythonanywhere.com")
        
    else:
        print(f"❌ Errore: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
        
except Exception as e:
    print(f"❌ Errore connessione: {e}")


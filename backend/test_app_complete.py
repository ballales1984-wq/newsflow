"""Test completo dell'applicazione - Verifica tutto funzioni"""
import requests
import sys

print("🧪 Test Automatico NewsFlow - Completo")
print("=" * 70)

# Configurazione
BACKEND_URL = "https://newsflow-backend-mzw7.onrender.com"
# BACKEND_URL = "http://localhost:8000"  # Usa questo per test locale

test_results = {
    'passed': 0,
    'failed': 0,
    'errors': []
}

def test_endpoint(name, url, expected_keys=None):
    """Test singolo endpoint"""
    print(f"\n🔍 Testing: {name}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code} OK")
            
            data = response.json()
            
            # Verifica chiavi attese
            if expected_keys:
                for key in expected_keys:
                    if key in data or (isinstance(data, list) and len(data) > 0 and key in data[0]):
                        print(f"   ✅ Key '{key}' presente")
                    else:
                        print(f"   ⚠️  Key '{key}' mancante")
                        test_results['errors'].append(f"{name}: chiave '{key}' mancante")
            
            test_results['passed'] += 1
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            test_results['failed'] += 1
            test_results['errors'].append(f"{name}: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"{name}: {str(e)}")
        return False


# Test 1: Root endpoint
test_endpoint(
    "Root Endpoint",
    f"{BACKEND_URL}/",
    expected_keys=['name', 'version', 'status']
)

# Test 2: Health check
test_endpoint(
    "Health Check",
    f"{BACKEND_URL}/api/health",
    expected_keys=['status']
)

# Test 3: Articles list
result = test_endpoint(
    "Articles List",
    f"{BACKEND_URL}/api/v1/articles",
    expected_keys=['items', 'total', 'page']
)

if result:
    # Test 3.1: Verifica numero notizie
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/articles")
        data = response.json()
        num_articles = len(data.get('items', []))
        print(f"   📊 Notizie trovate: {num_articles}")
        
        if num_articles >= 10:
            print(f"   ✅ Numero notizie sufficiente (>= 10)")
            test_results['passed'] += 1
        else:
            print(f"   ⚠️  Poche notizie (< 10)")
            test_results['errors'].append(f"Solo {num_articles} notizie trovate")
            test_results['failed'] += 1
            
        # Test 3.2: Verifica struttura notizie
        if num_articles > 0:
            article = data['items'][0]
            required_fields = ['id', 'title', 'url', 'summary', 'author']
            missing = [f for f in required_fields if f not in article]
            
            if not missing:
                print(f"   ✅ Struttura articoli completa")
                test_results['passed'] += 1
            else:
                print(f"   ⚠️  Campi mancanti: {missing}")
                test_results['errors'].append(f"Campi mancanti: {missing}")
                test_results['failed'] += 1
                
    except Exception as e:
        print(f"   ❌ Errore verifica notizie: {e}")
        test_results['failed'] += 1

# Test 4: Categories
result = test_endpoint(
    "Categories List",
    f"{BACKEND_URL}/api/v1/categories",
    expected_keys=['id', 'name', 'slug']
)

if result:
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/categories")
        categories = response.json()
        num_categories = len(categories)
        print(f"   📊 Categorie trovate: {num_categories}")
        
        if num_categories >= 5:
            print(f"   ✅ Numero categorie sufficiente")
            test_results['passed'] += 1
        else:
            test_results['failed'] += 1
    except:
        test_results['failed'] += 1

# Test 5: Sources
test_endpoint(
    "Sources List",
    f"{BACKEND_URL}/api/v1/sources",
    expected_keys=['id', 'name', 'url']
)

# Test 6: Single article (by ID)
test_endpoint(
    "Single Article (ID)",
    f"{BACKEND_URL}/api/v1/articles/1",
    expected_keys=['id', 'title', 'url']
)

# Test 7: Single article (by slug)
test_endpoint(
    "Single Article (slug)",
    f"{BACKEND_URL}/api/v1/articles/slug/can-openai-keep-pace-with-industrys-soaring-costs",
    expected_keys=['id', 'title', 'url']
)

# Risultati finali
print("\n" + "=" * 70)
print("📊 RISULTATI TEST:")
print(f"   ✅ Passed: {test_results['passed']}")
print(f"   ❌ Failed: {test_results['failed']}")
print(f"   📈 Success Rate: {(test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100):.1f}%")

if test_results['errors']:
    print(f"\n⚠️  ERRORI TROVATI ({len(test_results['errors'])}):")
    for error in test_results['errors']:
        print(f"   - {error}")
else:
    print("\n🎉 NESSUN ERRORE! Tutto funziona perfettamente!")

print("\n" + "=" * 70)

# Exit code
if test_results['failed'] == 0:
    print("✅ TUTTI I TEST PASSATI!")
    sys.exit(0)
else:
    print("❌ ALCUNI TEST FALLITI!")
    sys.exit(1)


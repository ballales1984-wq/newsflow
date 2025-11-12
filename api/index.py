"""
Vercel Serverless Function wrapper per FastAPI backend
Questo file gestisce tutte le routes API come serverless function
"""
import sys
import os

# Aggiungi il path del backend al PYTHONPATH
# Su Vercel, i file sono nella root del progetto
current_dir = os.path.dirname(os.path.abspath(__file__))  # api/
project_root = os.path.dirname(current_dir)  # root del progetto

# Aggiungi backend al PYTHONPATH
backend_path = os.path.join(project_root, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Imposta il working directory per i file JSON
# Su Vercel, la root del progetto è dove sono i file JSON
os.chdir(project_root)

# Debug: stampa i path (solo in sviluppo)
if os.getenv('VERCEL_ENV') != 'production':
    print(f"DEBUG: current_dir={current_dir}")
    print(f"DEBUG: project_root={project_root}")
    print(f"DEBUG: backend_path={backend_path}")
    print(f"DEBUG: cwd={os.getcwd()}")
    print(f"DEBUG: final_news exists={os.path.exists(os.path.join(project_root, 'backend', 'final_news_italian.json'))}")

from mangum import Mangum
from app.main_simple import app

# Crea handler Mangum per Vercel
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """Handler per Vercel serverless functions"""
    return handler(event, context)


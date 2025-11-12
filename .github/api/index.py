"""
Vercel Serverless Function wrapper per FastAPI backend
Questo file gestisce tutte le routes API come serverless function
"""
import sys
import os

# Aggiungi il path del backend al PYTHONPATH
# Su Vercel, i file sono nella root del progetto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Torna alla root del progetto
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

# Imposta il working directory per i file JSON
os.chdir(project_root)

from mangum import Mangum
from app.main_simple import app

# Crea handler Mangum per Vercel
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """Handler per Vercel serverless functions"""
    return handler(event, context)


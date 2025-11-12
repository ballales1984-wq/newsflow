"""
Vercel Serverless Function wrapper per FastAPI backend
Questo file gestisce tutte le routes API come serverless function
"""
import sys
import os

# Aggiungi il path del backend al PYTHONPATH
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from mangum import Mangum
from app.main_simple import app

# Crea handler Mangum per Vercel
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """Handler per Vercel serverless functions"""
    return handler(event, context)


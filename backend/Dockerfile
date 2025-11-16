FROM python:3.12-slim

WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il backend
COPY . .

# Esponi porta (Fly.io usa 8080 di default, ma può essere configurato)
EXPOSE 8080

# Variabile d'ambiente per porta
ENV PORT=8080

# Avvia FastAPI
CMD python -m uvicorn app.main_simple:app --host 0.0.0.0 --port ${PORT:-8080}

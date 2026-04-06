FROM python:3.11-slim

WORKDIR /app

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements minimali
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copia tutto il backend
COPY . .

# Variabili ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Esponi porta (Render usa 10000)
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:10000/api/health || exit 1

# Avvia FastAPI
CMD ["python", "-m", "uvicorn", "app.main_simple:app", "--host", "0.0.0.0", "--port", "10000"]

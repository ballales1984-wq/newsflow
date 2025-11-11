FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements-minimal.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


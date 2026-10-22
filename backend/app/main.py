from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .core.config import settings
from .core.database import engine, Base
from .api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables at import time.
# Questo è un pattern comune in applicazioni FastAPI che non usano migrazioni
# automatiche: assicura che lo schema sia sempre aggiornato quando l'app viene
# caricata. In produzione con più worker, questo può causare race condition
# se due istanze inizializzano contemporaneamente, ma è accettabile per un
# progetto in via di sviluppo o con un singolo worker.
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent News Curation Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS: permette al client browser (di solito su un dominio diverso,
# es. Vercel frontend) di chiamare l'API senza che il browser blocchi le
# richieste cross-origin. allow_credentials=True richiede che si usino
# origin specifici (non "*") in produzione, ma qui si usano gli origini da settings.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API router: tutti i endpoint v1 sono montati sotto /api/v1.
# Il prefix viene applicato qui, non nei singoli router, così che i tag OpenAPI
# rimangano associati al router corretto ma l'URL reale sia /api/v1/articles, etc.
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler.

    Cattura qualsiasi eccezione non gestita nelle route per evitare che
    FastAPI restituisca una risposta HTML di errore di default. Restituisce
    sempre un JSON con status 500 e un messaggio generico, senza i dettagli
    dell'eccezione: questo evita di esporre stack trace o informazioni
    sensibili ai client. I dettagli reali vengono loggati lato server.
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


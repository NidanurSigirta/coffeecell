"""CoffeeCell — FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---------- Uygulama ----------
app = FastAPI(
    title="CoffeeCell API",
    description="Dijital kahve abonelik platformu — Turkcell AI Bootcamp case study",
    version="0.1.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # Alternatif dokümantasyon
)

# ---------- CORS ----------
# Frontend (http://localhost:5173) backend'e istek atabilsin diye.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Health check endpoint ----------
@app.get("/", tags=["Root"])
def root():
    """Root endpoint — uygulamanın ayakta olduğunu doğrulamak için."""
    return {
        "name": "CoffeeCell API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check — Docker/Kubernetes'in servisi canlı mı diye yoklaması için."""
    return {"status": "healthy"}
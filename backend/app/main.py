"""CoffeeCell — FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine


# ---------- Lifespan: startup & shutdown ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Uygulama açılırken ve kapanırken çalışan kod.
    Burada DB'ye bir 'ping' atıyoruz — bağlantı sağlam mı diye.
    """
    # STARTUP
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        print(f"✅ Database connection OK — SELECT 1 → {result.scalar()}")

    yield

    # SHUTDOWN
    await engine.dispose()
    print("👋 Database connection closed")


# ---------- Application ----------
app = FastAPI(
    title=f"{settings.app_name} API",
    description="Dijital kahve abonelik platformu — Turkcell AI Bootcamp case study",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Endpoints ----------
@app.get("/", tags=["Root"])
def root():
    return {
        "name": f"{settings.app_name} API",
        "version": "0.1.0",
        "status": "running",
        "env": settings.app_env,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
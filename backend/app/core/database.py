"""Database engine and session management."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# ---------- Engine ----------
# echo=True → her SQL sorgusu log'a yazılır (development için faydalı)
engine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,
    pool_pre_ping=True,   # bağlantı kopmuşsa otomatik yeniden bağlan
)

# ---------- Session factory ----------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------- Base model ----------
class Base(DeclarativeBase):
    """Tüm SQLAlchemy modellerinin türeyeceği taban sınıf."""
    pass


# ---------- Dependency for FastAPI ----------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI endpoint'lerinde kullanılacak DB session dependency.
    Her request için yeni bir session açar, bitince kapar.
    """
    async with AsyncSessionLocal() as session:
        yield session
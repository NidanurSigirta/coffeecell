"""Shop model — anlaşmalı kahve dükkânları.

Case referansı: 3.3 Dükkân ve Konum Sistemi.
Konum için PostGIS Geography (POINT, SRID 4326 - WGS84, Google Maps uyumlu) kullanıyoruz.
"""
from datetime import time
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Time
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Shop(Base, TimestampMixin):
    """Anlaşmalı kahve dükkânları."""

    __tablename__ = "shops"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)

    # ---------- Konum ----------
    # Geography(POINT, 4326): dünya küresi üzerinde (lng, lat) noktası
    # ST_DWithin, ST_Distance gibi fonksiyonlar metre cinsinden çalışır.
    location: Mapped[str] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=False,
        comment="Dükkânın coğrafi konumu (POINT, SRID 4326 — WGS84/GPS standardı)",
    )

    # ---------- Çalışma saatleri ----------
    opening_time: Mapped[time] = mapped_column(Time, nullable=False)
    closing_time: Mapped[time] = mapped_column(Time, nullable=False)

    # ---------- Değerlendirme ----------
    rating: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
        server_default="0.0",
        comment="0-5 arası ortalama puan",
    )
    rating_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # ---------- Durum ----------
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    # ---------- Sahiplik ----------
    owner_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ---------- İlişkiler ----------
    owner: Mapped["User | None"] = relationship(back_populates="owned_shops")

    def __repr__(self) -> str:
        return f"<Shop id={self.id} name='{self.name}'>"
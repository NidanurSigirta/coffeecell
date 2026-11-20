"""User model — platformun kullanıcı tablosu.

Case referansı: 3.1 Kullanıcı Yönetimi + 5. Veritabanı Şeması (Users Tablosu).
"""
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserRole(str, Enum):
    """Rol bazlı erişim — case 3.1."""
    CUSTOMER = "CUSTOMER"
    SHOP_OWNER = "SHOP_OWNER"
    ADMIN = "ADMIN"


class User(Base):
    """Platform kullanıcıları."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    phone_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
        index=True,
        comment="GSM numarası, E.164 formatında (ör: +905551234567)",
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
    )
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.CUSTOMER,
    )
    preferences: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Kahve tercihleri, alerjen bilgileri vs.",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} phone={self.phone_number} role={self.role.value}>"
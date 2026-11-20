"""Subscription model — abonelik planları.

Case referansı: 3.2 Abonelik Sistemi + 5. Veritabanı Şeması (Subscriptions Tablosu).
Paketler: Starter (10 kahve/ay), Premium (20), Unlimited (sınırsız).
"""
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class PlanType(str, Enum):
    """Abonelik paketleri — case 3.2."""
    STARTER = "STARTER"       # 89.99 TL — 10 kahve/ay
    PREMIUM = "PREMIUM"       # 149.99 TL — 20 kahve/ay + 2 misafir
    UNLIMITED = "UNLIMITED"   # 249.99 TL — sınırsız + 5 misafir + öncelik


class SubscriptionStatus(str, Enum):
    """Abonelik durumları."""
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Subscription(Base, TimestampMixin):
    """Kullanıcı abonelikleri — bir kullanıcının birden fazla geçmiş aboneliği olabilir."""

    __tablename__ = "subscriptions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    plan_type: Mapped[PlanType] = mapped_column(
        SQLEnum(PlanType, name="plan_type_enum"),
        nullable=False,
    )
    remaining_credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Kalan kahve hakkı. -1 = sınırsız (UNLIMITED plan için).",
    )
    status: Mapped[SubscriptionStatus] = mapped_column(
        SQLEnum(SubscriptionStatus, name="subscription_status_enum"),
        nullable=False,
        default=SubscriptionStatus.ACTIVE,
        server_default="ACTIVE",
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ---------- İlişkiler ----------
    user: Mapped["User"] = relationship(back_populates="subscriptions")

    def __repr__(self) -> str:
        return (
            f"<Subscription id={self.id} user={self.user_id} "
            f"plan={self.plan_type.value} status={self.status.value}>"
        )
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy import String, func, Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base
from midas_sales.core.models.smtp_model import Smtp


class PlanType(Enum):
    Free = "Free"
    Silver = "Silver"
    Gold = "Gold"


tenant_addresses = Table(
    "core_tenants_addresses",
    Base.metadata,
    Column("address_id", ForeignKey("core_address.id", ondelete="CASCADE")),
    Column("tenant_id", ForeignKey("core_tenants.id", ondelete="CASCADE")),
)

tenant_smtp = Table(
    "core_tenants_smtp",
    Base.metadata,
    Column("smtp_id", ForeignKey("core_smtp.id", ondelete="CASCADE")),
    Column("tenant_id", ForeignKey("core_tenants.id", ondelete="CASCADE")),
)


class Tenant(Base):
    __tablename__ = "core_tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    cnpj: Mapped[str | None] = mapped_column(String(11))
    name: Mapped[str | None] = mapped_column(String(50))
    fantasy_name: Mapped[str | None] = mapped_column(String(50))
    ie: Mapped[str | None] = mapped_column(String(20))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(100))
    website: Mapped[str | None] = mapped_column(String(100))
    logo_url: Mapped[str | None] = mapped_column(String(100))
    plan: Mapped[PlanType | None] = mapped_column(default=PlanType.Free)
    stripe_id: Mapped[str | None] = mapped_column(String(100))
    data_expire: Mapped[datetime | None] = mapped_column(
        default=lambda: datetime.now() + timedelta(
            days=30))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(
        server_default=func.now(),
        onupdate=func.now())

    smtp: Mapped[list["Smtp"] | None] = relationship(
        secondary=tenant_smtp, lazy="immediate"
    )

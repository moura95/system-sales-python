from datetime import datetime

from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class Address(Base):
    __tablename__ = "core_address"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(11))
    zip_code: Mapped[str | None] = mapped_column(String(50))
    street: Mapped[str | None] = mapped_column(String(50))
    number: Mapped[str | None] = mapped_column(String(50))
    complement: Mapped[str | None] = mapped_column(String(50))
    district: Mapped[str | None] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

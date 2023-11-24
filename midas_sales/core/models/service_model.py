from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class Service(Base):
    __tablename__ = "core_services"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    name: Mapped[str]
    code: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None]
    price: Mapped[float]
    file_url: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

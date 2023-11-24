from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base

if TYPE_CHECKING:
    from midas_sales.core.models.company_model import Company


class Product(Base):
    __tablename__ = "core_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    factory_id: Mapped[int] = mapped_column(
        ForeignKey('core_companies.id', ondelete="CASCADE"), nullable=True)
    name: Mapped[str]
    code: Mapped[str | None]
    bar_code: Mapped[str | None]
    price: Mapped[float]
    cost_value: Mapped[float | None]
    reference: Mapped[str | None]
    unit: Mapped[str | None]
    description: Mapped[str | None]
    image_url: Mapped[str | None]
    minimum_stock: Mapped[int | None]
    maximum_stock: Mapped[int | None]
    current_stock: Mapped[int] = mapped_column(default=0)
    active_pdv: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

    factory: Mapped["Company"] = relationship("Company", lazy="immediate")

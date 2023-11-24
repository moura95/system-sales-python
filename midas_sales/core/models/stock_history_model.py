from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class StockHistory(Base):
    __tablename__ = "core_history_stock"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('core_products.id', ondelete="CASCADE"))
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey('core_users.id', ondelete="CASCADE"))
    reason: Mapped[str] = mapped_column()
    before_stock: Mapped[int] = mapped_column()
    after_stock: Mapped[int] = mapped_column()
    observation: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
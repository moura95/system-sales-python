from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from midas_sales.base.models.base_model import Base


class Customization(Base):
    __tablename__ = "core_customizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    key: Mapped[str]
    value: Mapped[str]
    title: Mapped[str] = mapped_column(default="Generic")
    type: Mapped[str] = mapped_column(default="String")
    changeable: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

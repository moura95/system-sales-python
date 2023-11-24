from datetime import datetime

from sqlalchemy import func, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class Smtp(Base):
    __tablename__ = "core_smtp"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(default=True)
    email: Mapped[str]
    password: Mapped[str]
    server: Mapped[str] = mapped_column(String(100))
    port: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

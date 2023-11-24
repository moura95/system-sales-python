from datetime import datetime

from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from midas_sales.base.models.base_model import Base


class Activity(Base):
    __tablename__ = "core_activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(20))
    reference_url: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('core_users.id', ondelete="CASCADE"))
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

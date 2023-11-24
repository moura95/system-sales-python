from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class File(Base):
    __tablename__ = "core_files"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    name: Mapped[str]
    directory: Mapped[str]
    url_file: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

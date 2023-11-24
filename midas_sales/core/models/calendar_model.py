from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class Calendar(Base):
    __tablename__ = "core_calendars"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    visit_start: Mapped[datetime | None]
    visit_end: Mapped[datetime | None]
    all_day: Mapped[bool | None]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('core_users.id', ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

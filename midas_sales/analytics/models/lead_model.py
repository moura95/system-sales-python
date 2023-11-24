from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class OriginLeadsEnum(Enum):
    Facebook = "Facebook"
    Instagram = "Instagram"
    Whatsapp = "Whatsapp"
    Google = "Google"
    Linkedin = "Linkedin"
    Outros = "Outros"


class Lead(Base):
    __tablename__ = "core_leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    origin: Mapped[OriginLeadsEnum] = mapped_column(
        default=OriginLeadsEnum.Outros)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

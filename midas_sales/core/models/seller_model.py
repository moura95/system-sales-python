from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base

if TYPE_CHECKING:
    from midas_sales.core.models.address_model import Address

seller_addresses = Table(
    "core_sellers_addresses",
    Base.metadata,
    Column("address_id", ForeignKey("core_address.id", ondelete="CASCADE")),
    Column("seller_id", ForeignKey("core_sellers.id", ondelete="CASCADE")),
)


class Seller(Base):
    __tablename__ = "core_sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    cpf: Mapped[str] = mapped_column(String(11))
    name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(100))
    pix: Mapped[str | None] = mapped_column(String(100))
    observation: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

    addresses: Mapped[list["Address"]] = relationship(
        secondary=seller_addresses, lazy="immediate", cascade="delete"
    )

from datetime import datetime

from sqlalchemy import ForeignKey, func, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base
from midas_sales.core.models.address_model import Address

user_addresses = Table(
    "core_users_addresses",
    Base.metadata,
    Column("address_id", ForeignKey("core_address.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("core_users.id", ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = "core_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    is_active: Mapped[bool | None] = mapped_column(default=True)
    last_login: Mapped[datetime] = mapped_column(default=func.now())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

    addresses: Mapped[list["Address"]] = relationship(
        secondary=user_addresses, lazy="immediate"
    )

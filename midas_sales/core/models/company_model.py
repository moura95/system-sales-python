from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base

if TYPE_CHECKING:
    from midas_sales.core.models.address_model import Address


class CompanyTypeEnum(Enum):
    Cliente = "Cliente"
    Transportadora = "Transportadora"
    Fornecedor = "Fornecedor"


company_addresses = Table(
    "core_companies_addresses",
    Base.metadata,
    Column("address_id", ForeignKey("core_address.id", ondelete="CASCADE")),
    Column("company_id", ForeignKey("core_companies.id", ondelete="CASCADE")),
)


class Company(Base):
    __tablename__ = "core_companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    company_type: Mapped[CompanyTypeEnum]
    is_individual: Mapped[bool]
    name: Mapped[str] = mapped_column(String(50))
    cpf_cnpj: Mapped[str | None] = mapped_column(String(11))
    last_fantasy_name: Mapped[str | None] = mapped_column(String(50))
    rg_ie: Mapped[str | None] = mapped_column(String(20))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())

    addresses: Mapped[list["Address"]] = relationship(
        secondary=company_addresses, lazy="immediate"
    )

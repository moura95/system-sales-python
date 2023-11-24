from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, func, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base

if TYPE_CHECKING:
    from midas_sales.core.models.file_model import File
    from midas_sales.core.models.form_payment_model import FormPayment
    from midas_sales.core.models.seller_model import Seller
    from midas_sales.core.models.product_model import Product
    from midas_sales.core.models.service_model import Service
    from midas_sales.core.models.company_model import Company
    from midas_sales.core.models.tenant_model import Tenant


class ShippingEnum(Enum):
    Entrega = "Entrega"
    Retirada = "Retirada"
    Outros = "Outros"


class StatusEnum(Enum):
    Pendente = "Pendente"
    Aprovado = "Aprovada"
    Cancelada = "Cancelada"


order_files = Table(
    "core_orders_files",
    Base.metadata,
    Column("order_id", ForeignKey("core_orders.id", ondelete="CASCADE")),
    Column("file_id", ForeignKey("core_files.id", ondelete="CASCADE")),
)


class OrderProduct(Base):
    __tablename__ = "core_orders_products"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("core_orders.id", ondelete="CASCADE"),
        primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("core_products.id", ondelete="CASCADE"), primary_key=True
    )
    price: Mapped[float]
    quantity: Mapped[int]
    discount: Mapped[float]
    total: Mapped[float]

    details: Mapped["Product"] = relationship("Product", lazy="immediate")


class OrderService(Base):
    __tablename__ = "core_orders_services"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("core_orders.id", ondelete="CASCADE"),
        primary_key=True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("core_services.id", ondelete="CASCADE"), primary_key=True
    )
    price: Mapped[float]
    quantity: Mapped[int]
    discount: Mapped[float]
    total: Mapped[float]

    details: Mapped["Service"] = relationship("Service", lazy="immediate")


class Order(Base):
    __tablename__ = "core_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    customer_id: Mapped[int] = mapped_column(
        ForeignKey('core_companies.id', ondelete="CASCADE"))
    portage_id: Mapped[int] = mapped_column(
        ForeignKey('core_companies.id', ondelete="CASCADE"),
        nullable=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('core_sellers.id',
                                                      ondelete="CASCADE"))
    form_payment_id: Mapped[int] = mapped_column(
        ForeignKey('core_form_payments.id'))
    order_number: Mapped[int] = mapped_column(String(50))
    observation: Mapped[str] = mapped_column(String(255), nullable=True)
    url_pdf: Mapped[str] = mapped_column(String(100), nullable=True)
    buyer: Mapped[str] = mapped_column(String(50), nullable=True)
    shipping: Mapped[ShippingEnum]
    status: Mapped[StatusEnum]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 server_onupdate=func.now())
    expired_at: Mapped[datetime] = mapped_column(nullable=True)
    contact_date: Mapped[datetime] = mapped_column(nullable=True)
    delivery_date: Mapped[datetime] = mapped_column(nullable=True)
    total_services: Mapped[float | None]
    total_products: Mapped[float | None]
    total: Mapped[float | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    tenant: Mapped["Tenant"] = relationship("Tenant", lazy="immediate")
    form_payment: Mapped["FormPayment"] = relationship("FormPayment",
                                                       lazy="immediate")
    seller: Mapped["Seller"] = relationship("Seller", lazy="immediate")
    customer: Mapped["Company"] = relationship(
        "Company",
        lazy="immediate",
        foreign_keys=[customer_id],
    )
    portage: Mapped["Company"] = relationship(
        "Company",
        lazy="immediate",
        foreign_keys=[portage_id],
    )
    files: Mapped[list["File"]] = relationship(
        secondary=order_files, lazy="immediate"
    )
    products: Mapped[list["OrderProduct"]] = relationship(lazy="selectin")
    services: Mapped[list["OrderService"]] = relationship(lazy="selectin")

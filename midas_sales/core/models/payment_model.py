from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from midas_sales.base.models.base_model import Base
from midas_sales.core.models.file_model import File

if TYPE_CHECKING:
    from midas_sales.core.models.form_payment_model import FormPayment


class PaymentTypeEnum(Enum):
    Pagamento = "Pagamento"
    Recebimento = "Recebimento"


class PaymentReceiptStatusEnum(Enum):
    Pendente = "Pendente"
    Pago = "Pago"
    Cancelado = "Cancelado"


payment_files = Table(
    "core_payments_files",
    Base.metadata,
    Column("payment_id",
           ForeignKey("core_payments.id", ondelete="CASCADE")),
    Column("file_id", ForeignKey("core_files.id", ondelete="CASCADE")))


class Payment(Base):
    __tablename__ = "core_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    type_payment: Mapped[PaymentTypeEnum]
    status: Mapped[PaymentReceiptStatusEnum]
    description: Mapped[str | None] = mapped_column(String(150))
    amount: Mapped[float]
    expiration_date: Mapped[datetime | None]
    payment_date: Mapped[datetime | None]
    doc_number: Mapped[str | None] = mapped_column(String(50))
    recipient: Mapped[str | None] = mapped_column(String(50))
    form_payment_id: Mapped[int] = mapped_column(
        ForeignKey('core_form_payments.id', onupdate="CASCADE"))
    is_active: Mapped[bool] = mapped_column(default=True)
    installment: Mapped[int] = mapped_column(default=1)
    numbers_installments: Mapped[int] = mapped_column(default=1)
    interval_days: Mapped[int] = mapped_column(default=30)
    additional_info: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())
    files: Mapped[list[File]] = relationship(
        secondary=payment_files, lazy="immediate"
    )

    form_payment: Mapped["FormPayment"] = relationship("FormPayment",
                                                       lazy="immediate")

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from midas_sales.base.models.base_model import Base


class FormPayment(Base):
    __tablename__ = "core_form_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey('core_tenants.id', ondelete="CASCADE"))
    name: Mapped[str]

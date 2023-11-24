from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from midas_sales.core.models.payment_model import PaymentTypeEnum, \
    PaymentReceiptStatusEnum


class PaymentReceiptBase(BaseModel):
    description: str | None
    amount: float
    status: PaymentReceiptStatusEnum
    expiration_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    doc_number: str | None = None
    recipient: str
    form_payment: int
    additional_info: str | None = None
    installment: Optional[int] = 1
    type_payment: PaymentTypeEnum


class PaymentReceiptBalanceCashier(BaseModel):
    balance: float
    balance_to_receive: float
    balance_to_pay: float


class PaymentReceiptCreate(PaymentReceiptBase):
    numbers_installments: int | None
    interval_days: int | None


class PaymentReceiptUpdate(BaseModel):
    description: str | None
    amount: float
    status: PaymentReceiptStatusEnum
    expiration_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    doc_number: str | None = None
    recipient: str | None = None
    form_payment: int | None = None
    additional_info: str | None = None
    installment: Optional[int] = 0


class PaymentReceiptID(BaseModel):
    id: int


class FilesPaymentBase(BaseModel):
    payment_receipt_id: int
    url_file: str


class FilesPaymentCreate(FilesPaymentBase):
    pass


class FilesPaymentUpdate(FilesPaymentBase):
    pass


class FilesPaymentID(BaseModel):
    id: int


class PaymentReceiptSchema(PaymentReceiptBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class FilesPaymentSchema(FilesPaymentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaymentSchema(PaymentReceiptBase):
    id: int
    interval_days: int | None
    files: list[FilesPaymentSchema] | None

    model_config = ConfigDict(from_attributes=True)

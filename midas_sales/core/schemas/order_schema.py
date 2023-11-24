from datetime import datetime

from pydantic import BaseModel, ConfigDict

from midas_sales.core.models.order_model import ShippingEnum, StatusEnum
from midas_sales.core.schemas.company_schema import CompanySchema
from midas_sales.core.schemas.file_schema import FileSchema, FileCreate
from midas_sales.core.schemas.form_payment_schema import FormPaymentSchema
from midas_sales.core.schemas.product_schema import ProductSchema
from midas_sales.core.schemas.seller_schema import SellerSchema
from midas_sales.core.schemas.service_schema import ServiceSchema


class OrderProduct(BaseModel):
    product_id: int | None
    quantity: int | None
    price: float | None
    discount: float | None
    total: float | None


class OrderProductCreate(OrderProduct):
    pass


class OrderProductSchema(OrderProduct):
    model_config = ConfigDict(from_attributes=True)

    details: ProductSchema | None


class OrderService(BaseModel):
    service_id: int | None
    quantity: int | None
    price: float | None
    discount: float | None
    total: float | None


class OrderServiceCreate(OrderService):
    pass


class OrderServiceSchema(OrderService):
    model_config = ConfigDict(from_attributes=True)

    details: ServiceSchema | None


class OrderBase(BaseModel):
    order_number: str | None
    observation: str | None
    url_pdf: str | None
    buyer: str | None
    shipping: ShippingEnum | None
    status: StatusEnum | None
    created_at: datetime | None
    updated_at: datetime | None
    expired_at: datetime | None
    contact_date: datetime | None
    delivery_date: datetime | None


class OrderCreate(OrderBase):
    customer_id: int | None
    portage_id: int | None
    seller_id: int | None
    form_payment_id: int | None
    files: list[FileCreate] | None
    services: list[OrderServiceCreate] | None
    products: list[OrderProductCreate] | None


class OrderUpdate(OrderBase):
    customer_id: int | None
    portage_id: int | None
    seller_id: int | None
    form_payment_id: int | None
    files: list[FileCreate] | None
    services: list[OrderServiceCreate] | None
    products: list[OrderProductCreate] | None


class OrderSchema(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    files: list[FileSchema] | None
    total_services: float | None
    total_products: float | None
    total: float | None
    is_active: bool | None
    seller: SellerSchema | None
    customer: CompanySchema | None
    portage: CompanySchema | None
    form_payment: FormPaymentSchema | None
    services: list[OrderServiceSchema] | None
    products: list[OrderProductSchema] | None

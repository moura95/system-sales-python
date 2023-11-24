from pydantic import BaseModel, ConfigDict

from midas_sales.core.schemas.company_schema import CompanySchema


class ProductBase(BaseModel):
    name: str
    code: str | None
    bar_code: str | None
    price: float
    cost_value: float | None
    reference: str | None = None
    unit: str | None
    description: str | None = None
    image_url: str | None = None
    minimum_stock: int | None = None
    maximum_stock: int | None = None
    current_stock: int | None


class ProductCreate(ProductBase):
    factory_id: int | None


class ProductUpdate(ProductBase):
    factory_id: int | None
    is_active: bool


class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    factory: CompanySchema | None

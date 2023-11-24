from pydantic import BaseModel


class DashBoardTopProducts(BaseModel):
    product_name: str
    product_factory: str
    total_product_sales: int


class DashBoardTotalSales(BaseModel):
    total: float


class DashBoardTopBuyer(BaseModel):
    customer_name: str
    quantity: int
    total: float


class DashBoardTopSalesFactory(BaseModel):
    factory_name: str
    quantity: int
    total: float

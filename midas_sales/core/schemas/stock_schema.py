from datetime import datetime

from pydantic import BaseModel


class StockHistoryBase(BaseModel):
    id: int
    tenant_id: int
    user_id: int
    product_id: int
    reason: str
    before_stock: int
    after_stock: int
    observation: str | None = None
    created_at: datetime
    updated_at: datetime


class StockProduct(BaseModel):
    before_stock: int
    after_stock: int
    reason: str
    observation: str | None


class StockHistorySchema(StockHistoryBase):
    pass

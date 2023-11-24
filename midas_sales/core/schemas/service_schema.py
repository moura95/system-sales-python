from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    name: str
    code: str | None
    price: float
    description: str | None
    reference: str | None = None
    file_url: str | None = None
    created_at: datetime | None
    updated_at: datetime | None


class ServiceCreate(ServiceBase):
    factory_id: int | None


class ServiceUpdate(ServiceBase):
    is_active: bool


class ServiceSchema(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

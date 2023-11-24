from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TenantBase(BaseModel):
    cnpj: str | None
    name: str | None
    fantasy_name: str | None
    ie: str | None
    website: str | None
    logo_url: str | None


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    is_active: bool | None


class TenantSchema(TenantUpdate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    stripe_id: str | None
    data_expire: datetime
    created_at: datetime
    updated_at: datetime

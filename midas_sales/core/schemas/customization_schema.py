from pydantic import BaseModel


class CustomizationBase(BaseModel):
    key: str
    value: str
    title: str
    type: str
    changeable: bool


class CustomizationSchema(CustomizationBase):
    id: int
    is_active: bool
    tenant_id: int

from pydantic import BaseModel, ConfigDict

from midas_sales.analytics.models.lead_model import OriginLeadsEnum


class LeadBase(BaseModel):
    name: str
    email: str
    phone: str
    origin: OriginLeadsEnum


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class LeadID(BaseModel):
    id: int


class LeadSchema(LeadBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

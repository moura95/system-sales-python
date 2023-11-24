from pydantic import BaseModel, ConfigDict

from midas_sales.core.models.company_model import CompanyTypeEnum
from midas_sales.core.schemas.address_schema import AddressCreate, \
    AddressSchema, AddressUpdate


class CompanyBase(BaseModel):
    company_type: CompanyTypeEnum
    is_individual: bool
    name: str
    cpf_cnpj: str | None
    last_fantasy_name: str | None
    rg_ie: str | None
    phone: str | None
    email: str


class CompanyCreate(CompanyBase):
    addresses: list[AddressCreate] | None


class CompanyUpdate(CompanyBase):
    addresses: list[AddressUpdate] | None


class CompanySchema(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    addresses: list[AddressSchema] | None

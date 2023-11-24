from pydantic import BaseModel, ConfigDict, EmailStr

from midas_sales.core.schemas.address_schema import AddressCreate


class SellerBase(BaseModel):
    name: str
    cpf: str
    email: EmailStr | None
    phone: str | None
    observation: str | None
    pix: str | None
    addresses: list[AddressCreate] | None


class SellerCreate(SellerBase):
    pass


class SellerUpdate(SellerBase):
    pass


class SellerSchema(SellerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

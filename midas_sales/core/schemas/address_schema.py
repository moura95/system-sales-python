from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    type: str
    zip_code: str
    street: str
    number: str | None
    district: str | None
    complement: str | None
    state: str
    city: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressSchema(AddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

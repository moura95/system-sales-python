from pydantic import BaseModel, ConfigDict


class FormPaymentBase(BaseModel):
    name: str


class FormPaymentCreate(FormPaymentBase):
    pass


class FormPaymentUpdate(FormPaymentBase):
    pass


class FormPaymentSchema(FormPaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    is_active: bool


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    last_login: datetime
    created_at: datetime
    updated_at: datetime

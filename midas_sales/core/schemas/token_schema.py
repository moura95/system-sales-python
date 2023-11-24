from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None
    tenant_id: int | None
    plan: str | None
    user_id: int | None

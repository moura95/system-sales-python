from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.config import get_settings
from midas_sales.core.controllers.user_controller import UserController
from midas_sales.core.schemas.token_schema import TokenData
from midas_sales.database import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db, email: str, password: str):
    controller = UserController(db)
    user = await controller.get(email=email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    settings = get_settings()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key,
                             algorithm=settings.algorithm)
    return encoded_jwt


async def get_user(db, email: str):
    """Retorna o usuário do banco de dados"""
    controller = UserController(db)
    user = await controller.get(email=email)
    if user:
        return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_async_session)):
    """Retorna o usuário atual"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        email: str = payload.get("email")

        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, tenant_id=payload.get(
            "tenant_id"),
                               plan=payload.get("plan"),
                               user_id=payload.get("user_id"))
    except JWTError:
        raise credentials_exception
    user = await get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

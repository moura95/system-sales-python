from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.config import get_settings
from midas_sales.core.controllers.tenant_controller import TenantController
from midas_sales.core.models.user_model import User
from midas_sales.core.schemas.token_schema import Token
from midas_sales.database import get_async_session
from midas_sales.security import authenticate_user, create_access_token, \
    get_current_user

router = APIRouter(prefix="/token", tags=["Token"])


@router.post("/", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(db, form_data.username,
                                   form_data.password)
    settings = get_settings()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)

    controller_tenant = TenantController(db)
    tenant = await controller_tenant.get(
        id=user.tenant_id)

    access_token = create_access_token(
        data={"email": user.email, "tenant_id": tenant.id,
              "user_id": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh_token", response_model=Token)
def refresh_access_token(
        user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={"sub": user.email})

    return {"access_token": new_access_token, "token_type": "bearer"}

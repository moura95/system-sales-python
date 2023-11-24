from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.user_controller import UserController
from midas_sales.core.schemas.address_schema import AddressSchema
from midas_sales.core.schemas.user_schema import UserCreate, UserSchema, \
    UserUpdate
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/user", tags=["User"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[UserSchema])
async def get_all_users(current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = UserController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201, response_model=UserSchema)
async def create_user(user: UserCreate,
                      current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = UserController(db)
        return await controller.create(**user.model_dump(),
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", status_code=200, response_model=UserSchema)
async def get_user(user_id: int, current_user=Depends(get_current_user),
                   db: AsyncSession = Depends(get_async_session)):
    try:
        controller = UserController(db)
        return await controller.get(id=user_id,
                                    tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{user_id}", status_code=200, response_model=UserSchema)
async def update_user(user_id: int, user: UserUpdate,
                      current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = UserController(db)
        return await controller.update(**user.model_dump(), id=user_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=200, response_model=UserSchema)
async def delete_user(user_id: int, current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = UserController(db)
        return await controller.delete(id=user_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}/address/{address_id}", status_code=200,
               response_model=AddressSchema)
async def delete_user_address(user_id: int, address_id: int,
                              current_user=Depends(get_current_user),
                              db: AsyncSession = Depends(
                                  get_async_session)):
    try:
        controller = UserController(db)
        return await controller.delete(address_id=address_id, id=user_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

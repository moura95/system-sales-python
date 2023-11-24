from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.tenant_controller import TenantController
from midas_sales.core.schemas.address_schema import AddressSchema
from midas_sales.core.schemas.tenant_schema import TenantSchema, \
    TenantUpdate
from midas_sales.core.schemas.user_schema import UserSchema, UserCreate
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/tenant", tags=["Tenant"])


@router.get("/", status_code=200, response_model=TenantSchema)
async def get_tenant(current_user=Depends(get_current_user),
                     db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        return await controller.get(id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201, response_model=UserSchema)
async def create_tenant(tenant: UserCreate,
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        return await controller.create(**tenant.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", status_code=200, response_model=TenantSchema)
async def delete_tenant(current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        return await controller.delete(id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/address/{address_id}", status_code=200,
               response_model=AddressSchema)
async def delete_tenant_address(address_id: int,
                                current_user=Depends(get_current_user),
                                db: AsyncSession = Depends(
                                    get_async_session)):
    try:
        controller = TenantController(db)
        return await controller.delete(address_id=address_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/", status_code=200, response_model=TenantSchema)
async def update_tenant(tenant: TenantUpdate,
                        current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        return await controller.update(**tenant.model_dump(),
                                       id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

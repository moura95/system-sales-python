from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.tenant_controller import TenantController
from midas_sales.core.schemas.tenant_schema import TenantCreate, TenantSchema, \
    TenantUpdate
from midas_sales.core.schemas.user_schema import UserSchema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/tenant", tags=["Tenant"])


@router.post("/", status_code=201, response_model=UserSchema)
async def create(schema: TenantCreate,
                 db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)

        tenant = await controller.create(**schema.model_dump())
        return tenant
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/", status_code=200, response_model=TenantSchema)
async def update(schema: TenantUpdate,
                 current_user=Depends(get_current_user),
                 db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        query = await controller.update(**schema.model_dump(),
                                        id=current_user.tenant_id, )
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=200, response_model=TenantSchema)
async def get(current_user=Depends(get_current_user),
              db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        query = await controller.get(id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", status_code=200, response_model=TenantSchema)
async def delete(current_user=Depends(get_current_user),
                 db: AsyncSession = Depends(get_async_session)):
    try:
        controller = TenantController(db)
        query = await controller.delete(id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

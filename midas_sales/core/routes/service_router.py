from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.service_controller import ServiceController
from midas_sales.core.schemas.service_schema import ServiceCreate, \
    ServiceUpdate, ServiceSchema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/service", tags=["Service"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[ServiceSchema])
async def get_all_service(current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ServiceController(db)
        query = await controller.get_all(
            tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201, response_model=ServiceSchema)
async def create_service(service: ServiceCreate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ServiceController(db)
        query = await controller.create(**service.model_dump(),
                                        tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{service_id}", status_code=200, response_model=ServiceSchema)
async def get_service(service_id: int, current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ServiceController(db)
        query = await controller.get(id=service_id,
                                     tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{service_id}", status_code=200, response_model=ServiceSchema)
async def update_service(service_id: int, service: ServiceUpdate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ServiceController(db)
        query = await controller.update(**service.model_dump(), id=service_id,
                                        tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{service_id}", status_code=200, response_model=ServiceSchema)
async def delete_service(service_id: int,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ServiceController(db)
        return await controller.delete(id=service_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.company_controller import CompanyController
from midas_sales.core.schemas.address_schema import AddressSchema
from midas_sales.core.schemas.company_schema import CompanyCreate, \
    CompanyUpdate, CompanyTypeEnum, CompanySchema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/company", tags=["Company"],
                   dependencies=[Depends(get_current_user)])


@router.post("/", status_code=201, response_model=CompanySchema)
async def create_company(company: CompanyCreate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CompanyController(db)
        return await controller.create(**company.model_dump(),
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=200, response_model=list[CompanySchema])
async def get_all_company(company_type: CompanyTypeEnum,
                          current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CompanyController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id, company_type=company_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{company_id}", status_code=200, response_model=CompanySchema)
async def get_company(company_id: int, current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CompanyController(db)
        return await controller.get(id=company_id,
                                    tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{company_id}", status_code=200, response_model=CompanySchema)
async def update_company(company_id: int, company: CompanyUpdate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CompanyController(db)
        return await controller.update(**company.model_dump(), id=company_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{company_id}", status_code=200, response_model=CompanySchema)
async def delete_company(company_id: int,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CompanyController(db)
        return await controller.delete(id=company_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{company_id}/address/{address_id}", status_code=200,
               response_model=AddressSchema)
async def delete_company_address(company_id: int, address_id: int,
                                 current_user=Depends(get_current_user),
                                 db: AsyncSession = Depends(
                                     get_async_session)):
    try:
        controller = CompanyController(db)
        return await controller.delete(address_id=address_id, id=company_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

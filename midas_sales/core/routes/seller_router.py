from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.seller_controller import SellerController
from midas_sales.core.schemas.address_schema import AddressSchema
from midas_sales.core.schemas.seller_schema import SellerCreate, SellerUpdate, \
    SellerSchema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/seller", tags=["Seller"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[SellerSchema])
async def get_all_seller(current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = SellerController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201, response_model=SellerSchema)
async def create_seller(seller: SellerCreate,
                        current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = SellerController(db)
        return await controller.create(**seller.model_dump(),
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{seller_id}", status_code=200, response_model=SellerSchema)
async def get_seller(seller_id: int, current_user=Depends(get_current_user),
                     db: AsyncSession = Depends(get_async_session)):
    try:
        controller = SellerController(db)
        return await controller.get(id=seller_id,
                                    tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{seller_id}", status_code=200, response_model=SellerSchema)
async def update_seller(seller_id: int, seller: SellerUpdate,
                        current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = SellerController(db)
        return await controller.update(**seller.model_dump(), id=seller_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{seller_id}", status_code=200, response_model=SellerSchema)
async def delete_seller(seller_id: int, current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        controller = SellerController(db)
        return await controller.delete(id=seller_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{seller_id}/address/{address_id}", status_code=200,
               response_model=AddressSchema)
async def delete_seller_address(seller_id: int, address_id: int,
                                current_user=Depends(get_current_user),
                                db: AsyncSession = Depends(
                                    get_async_session)):
    try:
        controller = SellerController(db)
        return await controller.delete(address_id=address_id, id=seller_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

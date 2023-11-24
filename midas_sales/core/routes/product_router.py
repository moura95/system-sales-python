from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, \
    File
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.product_controller import ProductController
from midas_sales.core.controllers.stock_history_controller import \
    StockHistoryController
from midas_sales.core.schemas.product_schema import ProductCreate, \
    ProductUpdate, ProductSchema
from midas_sales.core.schemas.stock_schema import StockHistorySchema, \
    StockProduct
from midas_sales.core.utils.normalize_csv import normalize_product_to_schema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/product", tags=["Product"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[ProductSchema])
async def get_all_product(current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ProductController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/history", status_code=200,
            response_model=list[StockHistorySchema])
async def get_all_stock_historu(current_user=Depends(get_current_user),
                                db: AsyncSession = Depends(get_async_session)):
    try:
        controller = StockHistoryController(db)
        query = await controller.get_all(
            tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201)
async def create_product(product: ProductCreate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ProductController(db)
        return await controller.create(**product.model_dump(),
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", status_code=200, response_model=ProductSchema)
async def get_product(product_id: int, current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ProductController(db)
        return await controller.get(id=product_id,
                                    tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{product_id}", status_code=200, response_model=ProductSchema)
async def update_product(product_id: int, product: ProductUpdate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ProductController(db)
        return await controller.update(**product.model_dump(), id=product_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{product_id}/stock", status_code=200,
              response_model=ProductSchema)
async def update_product_stock(product_id: int, product: StockProduct,
                               current_user=Depends(get_current_user),
                               db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ProductController(db)
        query = await controller.update(current_stock=product.after_stock,
                                        id=product_id,
                                        tenant_id=current_user.tenant_id)
        controller_stock_history = StockHistoryController(db)
        await controller_stock_history.create(
            product_id=product_id,
            before_stock=product.before_stock,
            after_stock=product.after_stock,
            reason=product.reason,
            observation=product.observation,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
        )

        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}", status_code=200, response_model=ProductSchema)
async def delete_product(product_id: int,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = ProductController(db)
        return await controller.delete(id=product_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{product_id}/import", status_code=201,
             response_model=ProductSchema)
async def upload_product_csv(product_id: int,
                             current_user=Depends(get_current_user),
                             db: AsyncSession = Depends(get_async_session),
                             file: UploadFile = File(...)):
    try:
        csv_content = await file.read()
        df = pd.read_csv(BytesIO(csv_content))

        data_dict_list = df.to_dict(orient="records")
        controller = ProductController(db)

        for dt in data_dict_list:
            dtSchema = normalize_product_to_schema(dt)
            dtSchema["factory_id"] = product_id
            dtSchema["tenant_id"] = current_user.tenant_id
            schema = ProductCreate(**dtSchema)
            await controller.create(**schema.model_dump(),
                                    tenant_id=current_user.tenant_id)

        return {"Ok": "Produtos importados com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

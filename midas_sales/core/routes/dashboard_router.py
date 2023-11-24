from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.schemas.dashboard_schema import DashBoardTopProducts, \
    DashBoardTopSalesFactory, \
    DashBoardTotalSales, \
    DashBoardTopBuyer
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["DashBoard"])


@router.get("/products/top", status_code=200)
async def get_rank_products(current_user=Depends(get_current_user),
                           db: AsyncSession = Depends(get_async_session)):
    try:
        topProduct = {
            "product_factory": "Cleber",
            "product_name": "Lapiz",
            "total_product_sales": 100
        }

        topProducts = DashBoardTopProducts(**topProduct)
        return topProducts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sales/", status_code=200)
async def get_rank_sales(current_user=Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    try:
        total = {
            "total": 100
        }

        totalSales = DashBoardTotalSales(**total)
        return totalSales
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/buyers/top", status_code=200)
async def get_rank_buyers(current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        topBuyer = {
            "customer_name": "Cleber",
            "quantity": 100,
            "total": 1000
        }

        topBuyers = DashBoardTopBuyer(**topBuyer)
        return topBuyers
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/factory/top", status_code=200)
async def get_rank_factory(current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        topFactory = {
            "factory_name": "Cleber",
            "quantity": 100,
            "total": 10000
        }

        topFactories = DashBoardTopSalesFactory(**topFactory)
        return topFactories
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.customization_controller import \
    CustomizationController
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/customization", tags=["Customization"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200)
async def get_customization(current_user=Depends(get_current_user),
                            db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CustomizationController(db)
        return await controller.get_all(tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

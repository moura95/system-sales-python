from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.form_payment_controller import \
    FormPaymentController
from midas_sales.core.schemas.form_payment_schema import FormPaymentCreate, \
    FormPaymentSchema, FormPaymentUpdate
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/form_payment", tags=["FormPayment"],
                   dependencies=[Depends(get_current_user)])


@router.post("/", status_code=201, response_model=FormPaymentSchema)
async def create_form_payment(schema: FormPaymentCreate,
                              current_user=Depends(get_current_user),
                              db: AsyncSession = Depends(get_async_session)):
    try:
        controller = FormPaymentController(db)
        return await controller.create(**schema.model_dump(),
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", status_code=200, response_model=list[FormPaymentSchema])
async def get_all_form_payment(current_user=Depends(get_current_user),
                               db: AsyncSession = Depends(get_async_session)):
    try:
        controller = FormPaymentController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{form_payment_id}", status_code=200,
            response_model=FormPaymentSchema)
async def get_form_payment(form_payment_id: int,
                           current_user=Depends(get_current_user),
                           db: AsyncSession = Depends(get_async_session)):
    try:
        controller = FormPaymentController(db)
        return await controller.get(id=form_payment_id,
                                    tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{form_payment_id}", status_code=200,
              response_model=FormPaymentSchema)
async def update_form_payment(form_payment_id: int, schema: FormPaymentUpdate,
                              current_user=Depends(get_current_user),
                              db: AsyncSession = Depends(get_async_session)):
    try:
        controller = FormPaymentController(db)
        return await controller.update(**schema.model_dump(),
                                       id=form_payment_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{form_payment_id}", status_code=200,
               response_model=FormPaymentSchema)
async def delete_form_payment(form_payment_id: int,
                              current_user=Depends(get_current_user),
                              db: AsyncSession = Depends(get_async_session)):
    try:
        controller = FormPaymentController(db)
        return await controller.delete(id=form_payment_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

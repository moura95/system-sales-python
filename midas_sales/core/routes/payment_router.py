from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.payment_controller import PaymentController
from midas_sales.core.schemas.payment_schema import PaymentReceiptCreate, \
    PaymentReceiptUpdate
from midas_sales.core.schemas.payment_schema import PaymentSchema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/payment", tags=["Payment"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[PaymentSchema])
async def get_all_payment(current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = PaymentController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/balance/", status_code=200)
async def get_balance_cashier(current_user=Depends(get_current_user),
                              db: AsyncSession = Depends(get_async_session)):
    try:
        controller = PaymentController(db)
        payment_paid_total = 0
        received_paid_total = 0
        payment_unpaid_total = 0
        received_unpaid_total = 0
        data_payment = []
        data_received = []
        query = await controller.get_all(
            tenant_id=current_user.tenant_id)
        payment_list = query.all()
        for payment in payment_list:
            if payment.type_payment.value == 'Pagamento' and payment.status.value == 'Pago':
                payment_paid_total += payment.amount
                data_payment.append(payment)

            elif payment.type_payment.value == 'Recebimento' and payment.status.value == 'Pago':
                received_paid_total += payment.amount
                data_received.append(payment)

            elif payment.type_payment.value == 'Pagamento' and payment.status.value == 'Pendente':
                payment_unpaid_total += payment.amount
                data_payment.append(payment)

            elif payment.type_payment.value == 'Recebimento' and payment.status.value == 'Pendente':
                received_unpaid_total += payment.amount
                data_received.append(payment)
        balance = received_paid_total - payment_paid_total

        data = {
            "balance": balance,
            "payment_paid_total": payment_paid_total,
            "received_paid_total": received_paid_total,
            "payment_unpaid_total": payment_unpaid_total,
            "received_unpaid_total": received_unpaid_total,
            "data_payment": data_payment,
            "data_received": data_received
        }
        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201)
async def create_payment(payment: PaymentReceiptCreate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        numbers_of_receipts = payment.numbers_installments
        interval_days = payment.interval_days
        i = 1
        while i <= numbers_of_receipts:
            new_schema = payment.copy()
            payment.installment = i
            if payment.expiration_date:
                new_schema.expiration_date = payment.expiration_date + timedelta(
                    days=interval_days * i)
            else:
                new_schema.expiration_date = datetime.now() + timedelta(
                    days=interval_days * i)
            controller = PaymentController(db)
            await controller.create(**new_schema.model_dump(),
                                    tenant_id=current_user.tenant_id)
            i += 1
        return {"message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{payment_id}", status_code=200, response_model=PaymentSchema)
async def get_payment(payment_id: int, current_user=Depends(get_current_user),
                      db: AsyncSession = Depends(get_async_session)):
    try:
        controller = PaymentController(db)
        query = await controller.get(id=payment_id,
                                     tenant_id=current_user.tenant_id)

        if query is None:
            raise HTTPException(status_code=400, detail="Pagamento não encontrado")
        return query

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{payment_id}", status_code=200, response_model=PaymentSchema)
async def update_payment(payment_id: int, schema: PaymentReceiptUpdate,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = PaymentController(db)
        query = await controller.update(**schema.model_dump(), id=payment_id,
                                        tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{payment_id}", status_code=200, response_model=PaymentSchema)
async def delete_payment(payment_id: int,
                         current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = PaymentController(db)
        query = await controller.delete(id=payment_id,
                                        tenant_id=current_user.tenant_id)
        return query
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

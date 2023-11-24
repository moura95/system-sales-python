import stripe
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.config import get_settings
from midas_sales.core.controllers.tenant_controller import TenantController
from midas_sales.core.schemas.stripe_schema import InvoicePaidEvent, \
    StripeCheckout
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/stripe", tags=["Stripe"])

settings = get_settings()
stripe.api_key = settings.stripe_api_key


@router.post("/checkout", status_code=201)
async def create_stripe(schema: StripeCheckout, request: Request,
                        current_user=Depends(get_current_user)):
    try:
        # plan = "price_1NQzgAHtPYbCB7tj5LkWqb53"
        plan = schema.plan
        name = current_user.first_name + " " + current_user.last_name
        customer = stripe.Customer.create(
            api_key=stripe.api_key,
            customer=name,
            email=current_user.email,
        )
        meta_data = {
            "TenantId": current_user.tenant_id,
            "System": "MIDASSALES",
            "CustomerId": customer.id,
            "Email": current_user.email,
        }

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': plan,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url="https://midasgestor.com.br/checkout/success",
            cancel_url="https://midasgestor.com.br/checkout/failed",
            payment_method_types=['card'],
            metadata=meta_data
        )
        return RedirectResponse(checkout_session.url)

    except Exception as e:
        print(e)
    return "Server error", 500


@router.post("/webhook", status_code=201)
async def webhook_stripe(schema: InvoicePaidEvent,
                         db: AsyncSession = Depends(get_async_session)):
    try:
        metadata = schema.data.object["lines"]["data"][0]["metadata"]
        status = schema.data.object.get("status")

        if metadata.get("System") == "MIDASSALES" and status == "paid":
            tenant_id = int(metadata.get("TenantId"))
            interval = schema.data.object["lines"]["data"][0]["price"][
                "recurring"].get("interval_count")
            period_end = schema.data.object["lines"]["data"][0]["period"].get(
                "end")
            controller = TenantController(db)
            await controller.update_plan(tenant_id=tenant_id,
                                         period_end=period_end)
        return {"data": "success"}
    except Exception as e:
        print(e)
    return "Server error", 500

import json

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.order_controller import OrderController
from midas_sales.core.schemas.order_schema import OrderCreate, OrderUpdate, \
    OrderSchema
from midas_sales.core.schemas.pdf_schema import OrderPdf
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/order", tags=["Order"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[OrderSchema])
async def get_all_orders(current_user=Depends(get_current_user),
                         db: AsyncSession = Depends(get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.get_all(
            tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=OrderSchema, status_code=201)
async def create_order(order: OrderCreate,
                       current_user=Depends(get_current_user),
                       db: AsyncSession = Depends(get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.create(**order.model_dump(),
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=OrderSchema, status_code=200)
async def get_order(order_id: int, current_user=Depends(get_current_user),
                    db: AsyncSession = Depends(get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.get(id=order_id,
                                    tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}", response_model=OrderSchema, status_code=200)
async def update_order(order_id: int, order: OrderUpdate,
                       current_user=Depends(get_current_user),
                       db: AsyncSession = Depends(get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.update(**order.model_dump(), id=order_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}", status_code=200)
async def delete_order(order_id: int, current_user=Depends(get_current_user),
                       db: AsyncSession = Depends(get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.delete(id=order_id,
                                       tenant_id=current_user.tenant_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}/file/{file_id}", status_code=200,
               response_model=OrderSchema)
async def delete_order_file(order_id: int, file_id: int,
                            current_user=Depends(get_current_user),
                            db: AsyncSession = Depends(
                                get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.delete(id=order_id,
                                       tenant_id=current_user.tenant_id,
                                       file_id=file_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}/product/{product_id}", status_code=200,
               response_model=OrderSchema)
async def delete_order_product(order_id: int, product_id: int,
                               current_user=Depends(get_current_user),
                               db: AsyncSession = Depends(
                                   get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.delete(id=order_id,
                                       tenant_id=current_user.tenant_id,
                                       product_id=product_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}/service/{service_id}", status_code=200,
               response_model=OrderSchema)
async def delete_order_service(order_id: int, service_id: int,
                               current_user=Depends(get_current_user),
                               db: AsyncSession = Depends(
                                   get_async_session)):
    try:
        controller = OrderController(db)
        return await controller.delete(id=order_id,
                                       tenant_id=current_user.tenant_id,
                                       service_id=service_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/gerar_pdf/{order_id}", status_code=200,
            response_class=FileResponse)
async def gerar_pdf(order_id: int, current_user=Depends(get_current_user),
                    db: AsyncSession = Depends(get_async_session)):
    try:
        controller = OrderController(db)
        order = await controller.get(id=order_id,
                                     tenant_id=current_user.tenant_id)

        with open("midas_sales/templates/pdf/footer.html", "r") as arquivo:
            footer_html = arquivo.read()

        with open("midas_sales/templates/pdf/order.html", "r") as arquivo:
            order_template = arquivo.read()

        with open("midas_sales/templates/pdf/options.json", "r") as arquivo:
            options = json.load(arquivo)

        header_html = ""
        if order.created_at:
            order.created_at = order.created_at.strftime("%d/%m/%Y")
        if order.expired_at:
            order.expired_at = order.expired_at.strftime("%d/%m/%Y")
        if order.delivery_date:
            order.delivery_date = order.delivery_date.strftime("%d/%m/%Y")
        if order.contact_date:
            order.contact_date = order.contact_date.strftime("%d/%m/%Y")



        if order.customer.addresses:
            address = order.customer.addresses[0]
            customer_address = {
                "street": address.street,
                "number": address.number,
                "district": address.district,
                "city": address.city,
                "state": address.state,
                "zip_code": address.zip_code,
            }
        else:
            customer_address = {
            }

        products = []
        for product in order.products:
            products.append({
                "name": product.details.name,
                "code": product.details.code,
                "price": product.price,
                "quantity": product.quantity,
                "discount": product.discount,
                "total": product.total,
                "description": product.details.description
            })
        services = []
        for service in order.services:
            services.append({
                "name": service.details.name,
                "code": service.details.code,
                "price": service.price,
                "quantity": service.quantity,
                "discount": service.discount,
                "total": service.total,
                "description": service.details.description
            })

        context = {
            "tenant": {
                "name": order.tenant.name,
                "cnpj": order.tenant.cnpj,
                "logo_url": order.tenant.logo_url,
            },
            "seller": {
                "name": order.seller.name,
                "email": order.seller.email,
                "phone": order.seller.phone,
            },
            "customer": {
                "name": order.customer.name,
                "fantasy_name": order.customer.last_fantasy_name,
                "cnpj": order.customer.cpf_cnpj,
                "street": customer_address.get("street", ""),
                "number": customer_address.get("number", ""),
                "district": customer_address.get("district", ""),
                "city": customer_address.get("city", ""),
                "state": customer_address.get("state", ""),
                "zip_code": customer_address.get("zip_code", ""),
                "ie": order.customer.rg_ie,
                "email": order.customer.email,
                "phone": order.customer.phone,
            },
            "order": {
                "buyer": order.buyer,
                "observation": order.observation,
                "number": order.order_number,
                "status": order.status.value,
                "payment_form": order.form_payment.name,
                "created_at": order.created_at,
                "contact_date": order.contact_date,
                "expired_at": order.expired_at,
                "delivery_date": order.delivery_date,
                "total_products": order.total_products,
                "total_services": order.total_services,
                "total": order.total,
            },
            "products": products,
            "services": services
        }

        order_pdf = OrderPdf(
            footerHtmlTemplate=footer_html,
            headerHtmlTemplate=header_html,
            htmlTemplate=order_template,
            model=context,
            options=options,
            templateEngine="golang",
        )

        pdf_bytes = httpx.post(
            "https://pdf.midasgestor.com.br/api/pdf/from/html-template/render",
            json=order_pdf.model_dump())

        headers = {"Content-Disposition": "attachment; filename=sample.pdf"}

        # Create a Response object with the file bytes, media type and headers
        response = Response(pdf_bytes.content, media_type="application/pdf",
                            headers=headers)

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

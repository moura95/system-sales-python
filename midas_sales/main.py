from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from starlette.background import BackgroundTasks

from midas_sales.config import settings
from midas_sales.core.routes import calendar_router, company_router, \
    customization_router, dashboard_router, order_router, payment_router, \
    product_router, seller_router, service_router, stripe_router, \
    tenant_router, token_router, user_router, form_payment_router
from midas_sales.tasks import process_task, process_send_email


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(generate_unique_id_function=custom_generate_unique_id,
              title="Midas Sales API", version="0.1.0",
              description="Vendas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=204)
async def health():
    return


@app.post("/send_task/")
async def send_task(param: str, to: str, background_tasks: BackgroundTasks):
    # Envie a tarefa para o Celery para processamento em segundo plano
    # result = process_task.delay(param)
    result = process_task.delay(param)
    print(settings.smtp_password)
    results = process_send_email.delay(to=to, subject="Pagamento Sucesso",
                                       template="payment-success")
    return {
        "message": f"Task ID: {result.id} sent for processing. and {results.id}"}


app.include_router(calendar_router.router)
app.include_router(company_router.router)
app.include_router(customization_router.router)
app.include_router(form_payment_router.router)
app.include_router(dashboard_router.router)
app.include_router(order_router.router)
app.include_router(payment_router.router)
app.include_router(product_router.router)
app.include_router(seller_router.router)
app.include_router(service_router.router)
app.include_router(stripe_router.router)
app.include_router(tenant_router.router)
app.include_router(token_router.router)
app.include_router(user_router.router)

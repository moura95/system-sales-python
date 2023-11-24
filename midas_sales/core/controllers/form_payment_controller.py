from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.form_payment_model import FormPayment


class FormPaymentController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(FormPayment, db)

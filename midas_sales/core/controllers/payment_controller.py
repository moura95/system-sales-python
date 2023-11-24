from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.payment_model import Payment


class PaymentController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Payment, db)


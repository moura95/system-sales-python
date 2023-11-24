from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.customization_model import Customization


class CustomizationController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Customization, db)

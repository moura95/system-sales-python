from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.service_model import Service


class ServiceController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Service, db)

from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.analytics.models.activity_model import Activity
from midas_sales.base.controllers.base_controller import BaseController


class ActivityController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

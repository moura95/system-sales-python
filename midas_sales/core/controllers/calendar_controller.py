from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.calendar_model import Calendar


class CalendarController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Calendar, db)

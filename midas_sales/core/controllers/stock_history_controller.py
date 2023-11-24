from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.stock_history_model import StockHistory


class StockHistoryController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(StockHistory, db)

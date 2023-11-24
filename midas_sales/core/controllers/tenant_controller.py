from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.controllers.form_payment_controller import \
    FormPaymentController
from midas_sales.core.controllers.user_controller import UserController
from midas_sales.core.models.tenant_model import Tenant


class TenantController(BaseController):
    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(Tenant, db)

    async def create(self, **kwargs):
        tenant = self.model()
        self.session.add(tenant)
        await self.session.flush()
        _ = await FormPaymentController(self.db).create(tenant_id=tenant.id,
                                                        name="30/45/60")
        return await UserController(self.db).create(tenant_id=tenant.id,
                                                    **kwargs)

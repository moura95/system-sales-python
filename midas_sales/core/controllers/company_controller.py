from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.address_model import Address
from midas_sales.core.models.company_model import Company


class CompanyController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Company, db)

    async def create(self, **kwargs):
        new_dict = kwargs.copy()
        del new_dict["addresses"]
        new_addresses = kwargs.get("addresses")
        db_addresses = []
        if new_addresses:
            for a in new_addresses:
                db_addresses.append(
                    Address(**a, tenant_id=kwargs["tenant_id"]))
        new_company = Company(**new_dict, addresses=db_addresses)
        self.session.add(new_company)
        await self.session.flush()
        return new_company

    async def update(self, **kwargs):
        db_company = await self.get(id=kwargs["id"],
                                    tenant_id=kwargs["tenant_id"])
        for field_name, value in kwargs.items():
            if field_name == "addresses":
                db_addresses = []
                for a in value:
                    db_addresses.append(
                        Address(**a, tenant_id=kwargs["tenant_id"]))
                setattr(db_company, field_name, db_addresses)
            else:
                setattr(db_company, field_name, value)
        await self.session.flush()
        return db_company

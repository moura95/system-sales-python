from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.address_model import Address
from midas_sales.core.models.seller_model import Seller


class SellerController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Seller, db)

    async def create(self, **kwargs):
        new_dict = kwargs.copy()
        del new_dict["addresses"]
        new_addresses = kwargs.get("addresses")
        db_addresses = []
        if new_addresses:
            for a in new_addresses:
                db_addresses.append(
                    Address(**a, tenant_id=kwargs["tenant_id"]))
        new_seller = Seller(**new_dict, addresses=db_addresses)
        self.session.add(new_seller)
        await self.session.flush()
        return new_seller

    async def update(self, **kwargs):
        db_seller = await self.get(id=kwargs["id"],
                                    tenant_id=kwargs["tenant_id"])
        for key, value in kwargs.items():
            if key == "addresses":
                db_addresses = []
                for a in value:
                    db_addresses.append(
                        Address(**a, tenant_id=kwargs["tenant_id"]))
                setattr(db_seller, key, db_addresses)
            else:
                setattr(db_seller, key, value)
        await self.session.flush()
        return db_seller

from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.base.controllers.base_controller import BaseController
from midas_sales.core.models.file_model import File
from midas_sales.core.models.order_model import Order, OrderProduct, \
    OrderService


class OrderController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def create(self, **kwargs):
        new_dict = kwargs.copy()

        new_files = kwargs.get("files")
        del new_dict["files"]

        new_products = kwargs["products"]
        del new_dict["products"]

        new_services = kwargs["services"]
        del new_dict["services"]

        new_order = Order(**new_dict)

        if new_files:
            for f in new_files:
                new_order.files.append(
                    File(**f, tenant_id=kwargs["tenant_id"]))

        if new_products:
            for p in new_products:
                new_order.products.append(OrderProduct(**p))

        if new_services:
            for p in new_services:
                new_order.services.append(OrderService(**p))

        self.session.add(new_order)
        await self.session.flush()
        await self.session.refresh(new_order)
        return new_order

    async def update(self, **kwargs):
        db_order = await self.get(id=kwargs["id"],
                                  tenant_id=kwargs["tenant_id"])
        if db_order:
            for field_name, value in kwargs.items():
                if field_name == "files" and value:
                    for a in value:
                        db_order.files.append(
                            File(**a, tenant_id=kwargs["tenant_id"]))
                elif field_name == "products" and value:
                    for p in value:
                        for o in db_order.products:
                            if o.product_id == p["product_id"]:
                                o.price = p["price"]
                                o.quantity = p["quantity"]
                                o.discount = p["discount"]
                                o.total = p["total"]
                            else:
                                db_order.products.append(
                                    OrderProduct(**p, order_id=db_order.id))
                elif field_name == "services" and value:
                    for s in value:
                        for o in db_order.services:
                            if o.service_id == s["service_id"]:
                                o.price = s["price"]
                                o.quantity = s["quantity"]
                                o.discount = s["discount"]
                                o.total = s["total"]
                            else:
                                db_order.services.append(
                                    OrderService(**s, order_id=db_order.id))
                else:
                    setattr(db_order, field_name, value)
            await self.session.flush()
            return db_order
        return None

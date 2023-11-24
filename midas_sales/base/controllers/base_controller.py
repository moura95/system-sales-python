from sqlalchemy import select, and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.models.address_model import Address


class BaseController:
    def __init__(self, model, db: AsyncSession):
        self.model = model
        self.session = db

    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj

    # TODO: Add order_by, filter_by, limit, offset
    async def get_all(self, **kwargs):
        where_clauses = []
        for field_name, value in kwargs.items():
            where_clauses.append(getattr(self.model, field_name) == value)
        stmt = select(self.model).where(and_(*where_clauses))
        return await self.session.scalars(stmt)

    async def get(self, **kwargs):
        where_clauses = []
        for field_name, value in kwargs.items():
            where_clauses.append(getattr(self.model, field_name) == value)

        stmt = select(self.model).where(and_(*where_clauses))
        a = await self.session.scalar(stmt)
        return a

    async def update(self, **kwargs):
        where_clauses, update_dict = [], {}
        for field_name, value in kwargs.items():
            if field_name in ["id", "tenant_id"]:
                where_clauses.append(getattr(self.model, field_name) == value)
            else:
                update_dict[field_name] = value

        stmt = update(self.model).where(and_(*where_clauses)).values(
            **update_dict)
        return await self.session.scalar(stmt.returning(self.model))

    async def delete(self, **kwargs):
        if "address_id" in kwargs:
            address_controller = BaseController(Address, self.session)
            return await address_controller.delete(id=kwargs["address_id"],
                                                   tenant_id=kwargs[
                                                       "tenant_id"])
        elif "file_id" in kwargs:
            file_controller = BaseController(Address, self.session)
            return await file_controller.delete(id=kwargs["file_id"],
                                                tenant_id=kwargs["tenant_id"])
        elif "product_id" in kwargs:
            order_db = await self.get(id=kwargs["id"],
                                      tenant_id=kwargs["tenant_id"])
            for o in order_db.products:
                if o.product_id == kwargs["product_id"]:
                    order_db.products.remove(o)
                    await self.session.delete(o)
            return order_db
        elif "service_id" in kwargs:
            order_db = await self.get(id=kwargs["id"],
                                      tenant_id=kwargs["tenant_id"])
            for o in order_db.services:
                if o.service_id == kwargs["service_id"]:
                    order_db.services.remove(o)
                    await self.session.delete(o)
            return order_db
        else:
            where_clauses = []
            for field_name, value in kwargs.items():
                where_clauses.append(getattr(self.model, field_name) == value)
            stmt = delete(self.model).where(and_(*where_clauses))
            return await self.session.scalar(stmt.returning(self.model))

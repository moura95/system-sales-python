from sqlalchemy.orm import mapped_column, Mapped

from midas_sales.base.models.base_model import Base


class Plan(Base):
    __tablename__ = "admin_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]

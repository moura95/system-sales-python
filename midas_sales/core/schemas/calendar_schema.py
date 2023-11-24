from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CalendarBase(BaseModel):
    title: str
    visit_start: datetime | None
    visit_end: datetime | None
    all_day: bool


class CalendarCreate(CalendarBase):
    pass


class CalendarUpdate(CalendarBase):
    pass


class CalendarSchema(CalendarBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

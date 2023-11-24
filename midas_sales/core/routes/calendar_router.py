from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from midas_sales.core.controllers.calendar_controller import CalendarController
from midas_sales.core.schemas.calendar_schema import CalendarCreate, \
    CalendarUpdate, CalendarSchema
from midas_sales.database import get_async_session
from midas_sales.security import get_current_user

router = APIRouter(prefix="/calendar", tags=["Calendar"],
                   dependencies=[Depends(get_current_user)])


@router.get("/", status_code=200, response_model=list[CalendarSchema])
async def get_all_calendar(current_user=Depends(get_current_user),
                           db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CalendarController(db)
        return await controller.get_all(id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=201, response_model=CalendarSchema)
async def create_calendar(calendar: CalendarCreate,
                          current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CalendarController(db)

        return await controller.create(**calendar.model_dump(),
                                       user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{calendar_id}", status_code=200, response_model=CalendarSchema)
async def get_calendar(calendar_id: int,
                       current_user=Depends(get_current_user),
                       db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CalendarController(db)
        return await controller.get(id=calendar_id, user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{calendar_id}", status_code=200, response_model=CalendarSchema)
async def update_calendar(calendar_id: int, calendar: CalendarUpdate,
                          current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CalendarController(db)
        return await controller.update(**calendar.model_dump(), id=calendar_id,
                                       user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{calendar_id}", status_code=200,
               response_model=CalendarSchema)
async def delete_calendar(calendar_id: int,
                          current_user=Depends(get_current_user),
                          db: AsyncSession = Depends(get_async_session)):
    try:
        controller = CalendarController(db)
        return await controller.delete(id=calendar_id,
                                       user_id=current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

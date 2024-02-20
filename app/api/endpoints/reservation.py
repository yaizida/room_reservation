from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.reservation import ReservationCreate, ReservationDB
from app.api.endpoints.validators import (check_reservation_intersections,
                                          check_meeting_room_exists)
from app.crud.reservation import reservation_crud

router = APIRouter()


@router.post('/', response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(
        reservation.meeting_room_id, session
    )

    await check_reservation_intersections(
        # Так как валидатор принимает **kwargs,
        # аргументы должны быть переданы с указанием ключей
        **reservation.dict(), session=session
    )

    new_reservation = await reservation_crud.create(
        reservation, session
    )
    return new_reservation

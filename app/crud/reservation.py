from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select


from app.crud.base import CRUDBase
from app.models.reservation import Reservation

reservation_crud = CRUDBase(Reservation)


class CRUDReservation(CRUDBase):
    """Выбрать такие объекты Reservation, где выполняются следующие условия:
        номер переговорки равен заданному
        и верны следующие условия:
            начало бронирования меньше конца
            существующего объекта бронирования,
            окончание бронирования больше начала
            существующего объекта бронирования."""
    async def get_reservations_at_the_same_time(
        self,
        # Добавляем звёздочку, чтобы обозначить, что все дальнейшие параметры
        # должны передаваться по ключу. Это позволит располагать
        # параметры со значением по умолчанию
        # перед параметрами без таких значений.
        *, from_reserve: datetime,
        to_reserve: datetime,
        meeting_room_id: int,
        # Добовляем новый опциональный параметр - id объекта бронирования.
        reservation_id: Optional[int] = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        # Выносим уже существующий запрос в отдельное выражение.
        select_stmt = select(Reservation).where(
            Reservation.meeting_room_id == meeting_room_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # Если передан id бронирования ...
        if reservation_id is not None:
            # то к вырожению нужно добавить новое условие.
            select_stmt = select_stmt.where(
                # id искомых объектов не равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        Reservations = await session.execute(select_stmt)
        Reservations = Reservations.scalars().all()

    async def get_future_reservations_for_room(
        self,
        room_id: int,
        session: AsyncSession,
    ):
        reservation = select(Reservation).where(
            Reservation.meeting_room_id == room_id,
            and_(
                Reservation.to_reserve >= datetime.now()
            )
        )

        reservations = await session.execute(reservation)
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(Reservation)

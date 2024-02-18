from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем sessionmaker из файла с найстройками БД.
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


# Функция работает с асинхронной сессией,
# поэтому ставим ключивое слово async.
# В функции передаём схему MeetingRoom
async def create_meeting_room(
    new_room: MeetingRoomCreate,
    session: AsyncSession,
) -> MeetingRoom:
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)
    return db_room


# добовляем новую всинхронную функцию.
async def get_room_id_name(
    room_name: str,
    session: AsyncSession,
) -> Optional[int]:

    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id

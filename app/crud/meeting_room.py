from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder

# Импортируем sessionmaker из файла с найстройками БД.
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


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


async def read_all_rooms_from_db(
    session: AsyncSession,
) -> list[MeetingRoom]:
    list_of_rooms = await session.execute(select(MeetingRoom))
    return list_of_rooms.scalars().all()


async def get_meeting_room_by_id(
    room_id: int,
    session: AsyncSession,
) -> Optional[MeetingRoom]:
    db_room_id = await session.execute(
        select(MeetingRoom).where(
            MeetingRoom.id == room_id
        )
    )
    return db_room_id.scalars().first()


async def update_meeting_room(
    # объект из БД для обновления.
    db_room: MeetingRoom,
    # объект из запроса.
    room_in: MeetingRoomUpdate,
    session: AsyncSession
) -> MeetingRoom:
    # Представялем объект из БД в виде словаря.
    obj_data = jsonable_encoder(db_room)
    # Конвертируем объект с данными из запросв в словарь,
    # исключаем неустановленные пользователем поля.
    update_data = room_in.dict(exclude_unset=True)
    # Перебераем все ключи словаря, сформированного из БД-объекта.
    for field in obj_data:
        # Если конкртеное поле есть в словаре с данными запроста, то...
        if field in update_data:
            # Устананвливаем объекту БД новое значение атрибута.
            setattr(db_room, field, update_data[field])
        # Добовляем обновленный объект в сессию.
        session.add(db_room)
        # Фиксируем изменения.
        await session.commit()
        # обновляем объект из БД.
        await session.refresh(db_room)
        return db_room

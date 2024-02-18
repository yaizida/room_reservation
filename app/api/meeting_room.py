from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import create_meeting_room, get_room_id_name  # noqa
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB

router = APIRouter()


@router.post(
    '/meeting_rooms/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    )
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    # Указываем зависимость,
    # предствавляющую объект сессии, как параметр функции.
    session: AsyncSession = Depends(get_async_session)
):
    # Вызываем функцию проверки уникальности поля name:
    # Вторым параметром передаём сессию в CRUD-функцию
    room_id = await get_room_id_name(meeting_room.name, session)
    # Если такой объект уже есть в базе - вызываем ошибку:
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже сущетсвует!',
        )
    # Вторым параметром предаём сессию в CRUD-функцию
    new_room = await create_meeting_room(meeting_room, session)
    return new_room

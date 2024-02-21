from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import meeting_room_crud
from app.schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB,
                                      MeetingRoomUpdate)
from app.api.endpoints.validators import (check_meeting_room_exists,
                                          check_name_duplicate)
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    )
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    # Указываем зависимость,
    # предствавляющую объект сессии, как параметр функции.
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.patch(
    # ID обновленного объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзера."""
    # Получаем объект из БД по ID.
    # В ответ ожидеается либо None, либо объект класса MeetingRoom.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    if obj_in.name is not None:
        # Если в запросе получено поле name - проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # Передаем в корутину все необходимые для обновления данные.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )

    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(
        meeting_room, session
    )
    return meeting_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,

    )
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session)
):
    list_of_rooms = await meeting_room_crud.get_multi(session)
    return list_of_rooms

from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import (create_meeting_room, get_meeting_room_by_id,
                                   get_room_id_name, read_all_rooms_from_db,
                                   update_meeting_room)
from app.schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB,
                                      MeetingRoomUpdate)

router = APIRouter(
    prefix='/meeting_rooms',
    tags=['Meeting Rooms']
)


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    )
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    # Указываем зависимость,
    # предствавляющую объект сессии, как параметр функции.
    session: AsyncSession = Depends(get_async_session)
):
    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.patch(
    # ID обновленного объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        # ID обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    # Получаем объект из БД по ID.
    # В ответ ожидеается либо None, либо объект класса MeetingRoom.
    meeting_room = await get_meeting_room_by_id(
        meeting_room_id, session
    )
    print(meeting_room, obj_in)
    if meeting_room is None:
        raise HTTPException(
            # Для отсутсвующего объекта вернем статус 404
            status_code=404,
            detail='Переговорка не найдена!'
        )
    if obj_in.name is not None:
        # Если в запросе получено поле name - проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # Передаем в корутину все необходимые для обновления данные.
    meeting_room = await update_meeting_room(
        meeting_room, obj_in, session
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
    list_of_rooms = await read_all_rooms_from_db(session)
    return list_of_rooms


async def check_name_duplicate(
    room_name: str,
    session: AsyncSession
) -> None:
    room_id = await get_room_id_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )

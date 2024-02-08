from fastapi import APIRouter, HTTPException

from app.crud.meeting_room import create_meeting_room, get_room_id_name  # noqa
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB

router = APIRouter()


@router.post(
    '/meeting_rooms/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    )
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate
):
    # Вызываем функцию проверки уникальности поля name:
    room_id = await get_room_id_name(meeting_room.name)
    # Если такой объект уже есть в базе - вызываем ошибку:
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже сущетсвует!',
        )
    new_room = await create_meeting_room(meeting_room)
    return new_room

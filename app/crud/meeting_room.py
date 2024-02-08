# Импортируем sessionmaker из файла с найстройками БД.
from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


# Функция работает с асинхронной сессией,
# поэтому ставим ключивое слово async.
# В функции передаём схему MeetingRoom
async def create_meeting_room(
    new_room: MeetingRoomCreate
) -> MeetingRoom:
    # Коневертируем объект MeetingRommCreate в словарь.
    new_room_data = new_room.dict()

    # Создаем объект модели MeetingRoom.
    # В параметры передаём пары "ключ-значение",
    # для этого распоковываем словарь
    db_room = MeetingRoom(**new_room_data)

    # Создаём создаем ассинхронную ссесию черех контекстный менеджер
    async with AsyncSessionLocal() as session:
        # Добовляем созданный объект в ссесию.
        # Никакие действия с базой пока еще не выполняются.
        session.add(db_room)

        # Записываем изменения непосредственно в БД.
        # Так как сессия асинхронная, используем ключевое слово await.
        await session.commit()

        # Обновляем объект db_room: считываес данные из БД,
        # что бы получить его айдишник
        await session.refresh(db_room)
    # Возвращаем только что созданный объект класса MeetingRoom.
    return db_room

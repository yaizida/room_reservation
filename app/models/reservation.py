from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    # Столбцы с внешним ключом: ссылка на таблицу meetingroom.
    meeting_room_id = Column(Integer, ForeignKey('meetingroom.id'))

from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class Reservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    # Столбцы с внешним ключом: ссылка на таблицу meetingroom.
    meeting_room_id = Column(Integer, ForeignKey('meetingroom.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'
        )
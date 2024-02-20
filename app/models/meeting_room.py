from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.core.db import Base
# Здесь нужно было бы дописать импорт нужной модели.
from app.models.reservation import Reservation


class MeetingRoom(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    # А здесь заменить строку 'Reservation' на класс.
    reservations = relationship(Reservation, cascade='delete')
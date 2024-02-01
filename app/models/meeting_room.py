# Импортирукете из Алхимии нужные классы.
from sqlalchemy import Column, String

# Импортируете базовый класс для моделей.
from app.core.db import Base


class MeetingRoom(Base):
    # Имя переговорок должно быть не больше 100 символов,
    # уникальным и не пустым
    name = Column(String(100), unique=True, nullable=False)

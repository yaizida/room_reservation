# Импортирукете из Алхимии нужные классы.
from sqlalchemy import Column, String, Text

# Импортируете базовый класс для моделей.
from app.core.db import Base


class MeetingRoom(Base):
    # Имя переговорок должно быть не больше 100 символов,
    # уникальным и не пустым
    name = Column(String(100), unique=True, nullable=False)
    # Новый атрибут модели. Значение nullable по умлочанию равно True
    # поэтому его можно не указывать.
    description = Column(Text)

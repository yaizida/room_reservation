from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr


from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добвалено поле ID.
    id = Column(Integer, primary_key=True)


# В качестве основы для базового классса укаем класс PreBase.
Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


# Асинхроный генератор сессий.
async def get_async_session():
    # Через асинхронный котекстный менеджер и sessionmaker
    # открыывается сессия.
    async with AsyncSessionLocal() as async_session:
        yield async_session
        # Когда HTTP-запрос отработает - выолнение кода вернется сюдя,
        # и при выходн из контекстоного менеджера сессия будет закрта.

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Этот серивис позволит забронировать переговорку'

    class Config:
        env_file = '.env'


settings = Settings()

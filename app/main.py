from fastapi import FastAPI

from app.core.config import settings

# Установили заголовок приложения при помощи аргумента
# в качестве значения указываем атрибут app_title объекта settings
app = FastAPI(title=settings.app_title,
              description=settings.app_description)

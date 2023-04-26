import logging
from . app import dp
from . import utils, random_ten, add_word, initial_mes, translate_mode #выполнит инициализацию всех хендлеров
from aiogram.contrib.middlewares.logging import LoggingMiddleware

#Включаем логирование на уровне INFO
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
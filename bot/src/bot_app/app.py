from . local_settings import API_KEY #TODO: Добавить в git ignore
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types

#Создаем объект бота из класса, в который подкидываем наш токен
bot = Bot(token=API_KEY, parse_mode=types.ParseMode.MARKDOWN_V2)

#Создаем объект диспетчера, в который передаем объект бота
dp = Dispatcher(bot, storage=MemoryStorage())


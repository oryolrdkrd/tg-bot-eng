from aiogram import executor
from bot_app import dp

#Для того, чтобы наш бот запустился как сервис и начал слушать сообщения
#телеграма, нужно сделать модуль экзекьютор

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
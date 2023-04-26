#так как бот у нас асинхронный, то и клиент выбираем асинхронный
#он будет работать с dgango по rest
#если бы был синхронный, то использовал бы requests
import aiohttp
import ujson
from . local_settings import WORDS_API_URL_RANDOM, WORDS_API_URL_ADDWORD, WORDS_API_URL_DEL_WORD
import json

#эта функция из модуля random_ten.py
async def get_random():
    #Стартуем асинхронную сессию
    async with aiohttp.ClientSession() as session:
        #делаем rest-запрос к бекэнду
        #обращаемся к эндпоинту через асинхронного клиента
        async with session.get(WORDS_API_URL_RANDOM) as response:
            #возвращаем полученный результат в виде JSON, как корутина отработает
            return await response.json()

async def add_word(word, translation, user_id):
    #Стартуем асинхронную сессию
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        #делаем rest-запрос к бекэнду
        #обращаемся к эндпоинту через асинхронного клиента
        async with session.post(WORDS_API_URL_ADDWORD, json={'word':word,'translation_base': translation, 'user_id':user_id}) as response:
            #возвращаем полученный результат в виде JSON, как корутина отработает
            return await response.text()

async def del_word(word, user_id):
    # Стартуем асинхронную сессию
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        # делаем rest-запрос к бекэнду
        # обращаемся к эндпоинту через асинхронного клиента
        async with session.post(WORDS_API_URL_DEL_WORD,
                                json={'word': word, 'user_id': user_id}) as response:
            # возвращаем полученный результат в виде JSON, как корутина отработает
            return await response.text()


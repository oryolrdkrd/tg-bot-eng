from aiogram import types
from . app import dp, bot
from . keyboards import inline_kb
from . states import GameStates
from . data_fetcher import get_random
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands='train_ten', state="*")
async def train_ten(message:types.Message, state:FSMContext):
    #Установим машину в состояние
    await GameStates.random_ten.set()
    res = await get_random()
    #Передаем состояние в машину, чтобы он ее запомнил
    async with state.proxy() as data:
        data['step'] = 1 #первый шаг, первое слово
        data['answer'] = res.get('gender') #то что получили от бэка, будем сравнивать, что ответил пользователь
        data['word'] = res.get('word') #то что получили от бэка, будем сравнивать, что ответил пользователь
        data['translation_base'] = res.get('translation_base')  # то что получили от бэка, будем сравнивать, что ответил пользователь
        await message.reply(f"{data['step']} of 10. Какой род слова {data['word']} + {data['translation_base']}", reply_markup=inline_kb)

#реализуем обработчик колбэков, который будет реагировать на действия пользователя
@dp.callback_query_handler(lambda c: c.data in ['male', 'neuter', 'female', 'exit'], state=GameStates.random_ten)
async def button_click_call_back(callback_query: types.CallbackQuery, state:FSMContext):
    #ответ телеге
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    #получаем данные запомненного состояния
    async with state.proxy() as data:
        #сравниваем что ответили и что запрашивали
        #сначала получаем ответ
        if answer == data['answer']:
            res = await get_random()
            data['step'] +=1
            data['answer'] = res.get('gender')
            data['word'] = res.get('word')
            if data['step'] > 10:
                await bot.send_message(callback_query.from_user.id, "The game is over!!!")
                await GameStates.start.set()
            else:
                await bot.send_message(callback_query.from_user.id, "Yes\n" + f"{data['step']} of 10. Какой род слова {data['word']}", reply_markup=inline_kb)
        else:
            if answer == 'exit':
                data['step'] = 100
                await bot.send_message(callback_query.from_user.id, f"Вы завершили игру :(\n Напоминаем вам про /help")
                await state.reset_state()
            else:
                await bot.send_message(callback_query.from_user.id, f"No {answer} {data['answer']}\n",
                                       reply_markup=inline_kb)


import json
from aiogram import types
from . app import dp, bot
from aiogram.dispatcher import FSMContext
from . states import TestStates, DeskriptionStates, TranslateModeStates
from . data_fetcher import add_word, del_word, update_word
from . keyboards import inline_kb_YN, inline_kb_chancel, inline_kb_exit, in_kb_main_menu, in_kb_change_word
import aiogram.utils.markdown as fmt
from emoji import emojize
from . messages import MESSAGES
from . data_fetcher import get_random
from . keyboards import inline_kb

@dp.message_handler(state='*', commands=['random'])
#
#   Входим в режим переводчика. Предлагаем ввести слово
#
async def process_random_word_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    data = await state.get_data()
    state = dp.current_state(user=message.from_user.id)
    #await state.update_data(word=message.text.lower(), user_id=message.from_user.id)
    await state.set_state(TranslateModeStates.input_word)
    msg_text = fmt.text(fmt.hitalic(MESSAGES['random_word']), sep="\n")
    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    res = await get_random()
    async with state.proxy() as data_res:
        data_res['step'] = 1 #первый шаг, первое слово
        data_res['answer'] = res.get('gender') #то что получили от бэка, будем сравнивать, что ответил пользователь
        data_res['word'] = res.get('word') #то что получили от бэка, будем сравнивать, что ответил пользователь
        data_res['translation_base'] = res.get('translation_base')  # то что получили от бэка, будем сравнивать, что ответил пользователь
        await bot.send_message(chat_id=message.from_user.id, text=f"{data_res['step']} of 10\. Какой род слова {data_res['word']} \+ {data_res['translation_base']}", reply_markup=inline_kb)
import json

from aiogram import types
from . app import dp, bot
from . keyboards import inline_kb
from . states import GameStates
from . data_fetcher import get_random
from aiogram.dispatcher import FSMContext
from . messages import MESSAGES
from . states import TestStates, DeskriptionStates
from . utils import GetCurrentState
from . data_fetcher import add_word
from . keyboards import inline_kb_YN
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
import aiogram.utils.markdown as fmt
from emoji import emojize


#Делаем модуль добавления слова в телеграмме
#Сначала мы предлагаем ввести слово
#Потом ждем слово
#Как дождались просим перевод
#Ждем перевод


#На команду просим ввести слово и устанавливаем FM в нужный стэйт
#'test_state_2': 'Добавление слова. Предлагаем ввести слово для добавления в словарь'
@dp.message_handler(state='*', commands=['add_word'])
async def process_add_word_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    #check_state(message, state)
    await state.set_state(TestStates.all()[2]) #'test_state_2': 'Добавление слова. Предложено ввести слово для добавления в словарь',
    await message.reply(MESSAGES['add_word'], reply=False) #TODO: пока заглушка, нужно будет писать куда-то

#Принимаем перевод слова и сбрасываем стейт в инит
#'test_state_0': 'Начальное состояние инициации',
@dp.message_handler(state=TestStates.TEST_STATE_2)
async def process_add_word_add_translate_command(message: types.Message, state:FSMContext):
    #await message.reply('Первый!', message.from_user.id, message.text, reply=False)

    async with state.proxy() as data:
        data['word'] = message.text

    await bot.send_message(message.from_user.id, text=emojize('➡ Введите перевод слова!'))

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[3]) #'test_state_3': 'Добавление слова. Предложено ввести перевод этого слова'

@dp.message_handler(state=TestStates.TEST_STATE_3)
async def process_add_word_add_translate_command(message: types.Message, state:FSMContext):
    #await message.reply('Первый!', message.from_user.id, message.text, reply=False)
    #await bot.send_message(message.from_user.id, text = "Вы ввели "+message.text)

    async with state.proxy() as data:
        data['translation_base'] = message.text

    res = await add_word(data['word'], data['translation_base'], message.from_user.id)
    decode_res = json.loads(res)

    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()


    msg_text = fmt.text(
        fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
        fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
        fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
        sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 1:
        await bot.send_message(chat_id=message.from_user.id, text=f"-> Вы можете сделать:", reply_markup=inline_kb_YN)


"""
    #--------------- Отладочная конструкция ------------------
    text = MESSAGES['current_state'].format(
        current_state=await state.get_state(),
        des_current_state=DeskriptionStates[await state.get_state()],
        states=TestStates.all())
    await message.reply(MESSAGES['state_change'] + " " + f"{text}", reply=False)
"""

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки", reply_markup=inline_kb_full)



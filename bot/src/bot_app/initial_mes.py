#это логика пустой реакции на текст
#TODO: установить нормальную логику
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType
from . app import dp, bot
from . messages import MESSAGES
from .states import TestStates, DeskriptionStates
import aiogram.utils.markdown as fmt
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.utils import executor

from . import messages
from . keyboards import inline_kb
from . states import GameStates
from . data_fetcher import get_random
from aiogram.dispatcher import FSMContext

@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES['start'])
@dp.message_handler(commands=['start'], state=TestStates.TEST_STATE_3 | TestStates.TEST_STATE_4 | TestStates.TEST_STATE_5)
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES['start'])

    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[0])
    msg_text = fmt.text(
        fmt.text(fmt.hunderline("State"), "=", await state.get_state(), "=",
                 DeskriptionStates[await state.get_state()]),
        fmt.text("\nСообщение: ", fmt.hitalic(
            "Вы вышли из режима перевода. Воспользуйтесь командами /end, /help или /start."),
                 sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])

@dp.message_handler(commands=['help'], state=TestStates.TEST_STATE_4)
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])


"""
@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    print("yep")
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Первый!', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_2[0])
async def second_test_state_case_met(message: types.Message):
    await message.reply('Второй!', reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_3 | TestStates.TEST_STATE_4)
async def third_or_fourth_test_state_case_met(message: types.Message):
    await message.reply('Третий или четвертый!', reply=False)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text('Я не знаю, что с этим делать :(',
                        italic('\nЯ просто напомню,'), 'что есть',
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)
"""

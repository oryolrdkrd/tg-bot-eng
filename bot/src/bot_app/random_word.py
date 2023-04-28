import json
from aiogram import types
from . app import dp, bot
from aiogram.dispatcher import FSMContext
from . states import TestStates, DeskriptionStates, TranslateModeStates
from . data_fetcher import add_word, del_word, update_word
from . keyboards import inline_kb_YN, inline_kb_chancel, inline_kb_exit, in_kb_main_menu, in_kb_change_word, genmarkup
import aiogram.utils.markdown as fmt
from emoji import emojize
from . messages import MESSAGES
from . data_fetcher import get_random
from . keyboards import inline_kb
from . states import TestStates, DeskriptionStates, RandomModeStates

@dp.message_handler(state='*', commands=['random'])
#
#   Входим в режим переводчика. Предлагаем ввести слово
#
async def process_random_word_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.update_data(user_id=message.from_user.id)

    data = await state.get_data()

    await state.set_state(RandomModeStates.input_word)
    msg_text = fmt.text(fmt.hitalic(MESSAGES['random_word']), sep="\n")
    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    res = await get_random()

    prep_res = json.dumps(res)
    decode_res = json.loads(prep_res)

    msg_text = fmt.text(
        fmt.text("\n",
                 fmt.hbold(decode_res['word']),
                 sep="\n"))
    kb = genmarkup(decode_res['random_trt'], decode_res['translation_base'])
    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML", reply_markup=kb)
    await state.update_data(translation_base=decode_res['translation_base'])



@dp.callback_query_handler(lambda c: c.data in ['exit'], state=[RandomModeStates.input_word])
async def button_exit_tm_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    #await state.reset_state()
    msg_text = fmt.text(fmt.text(fmt.hitalic("Вы вышли из режима тренировки слов. Воспользуйтесь командами /help или /start."),
                 sep="\n"))

    await bot.send_message(chat_id=data['user_id'], text=msg_text, parse_mode="HTML", reply_markup=in_kb_main_menu)

@dp.callback_query_handler(lambda c: True, state=[RandomModeStates.input_word])
async def button_solve_tm_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    #await state.reset_state()
    if callback_query.data.lower() == data['translation_base'].lower():
        await bot.send_message(chat_id=data['user_id'], text=f"Верно\!  {callback_query.data} {data['translation_base']}", reply_markup=inline_kb_exit)

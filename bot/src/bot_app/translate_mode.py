import json
from aiogram import types
from . app import dp, bot
from aiogram.dispatcher import FSMContext
from . states import TestStates, DeskriptionStates, TranslateModeStates
from . data_fetcher import add_word, del_word
from . keyboards import inline_kb_YN, inline_kb_chancel, inline_kb_exit
import aiogram.utils.markdown as fmt
from emoji import emojize

@dp.message_handler(state='*', commands=['t'])
async def process_add_word_setstate_command(message: types.Message):

    state = dp.current_state(user=message.from_user.id)
    await state.update_data(word=message.text.lower(), user_id=message.from_user.id)
    await state.set_state(TranslateModeStates.input_word)
    try:
        msg_text = fmt.text(
            fmt.text(fmt.hunderline("State"),
                     "=",
                     await state.get_state(),
                     "=",
                     DeskriptionStates[await state.get_state()]),
            fmt.text("\nСообщение: ",
                     fmt.hitalic(
                         "Вы вошли в режим переводчика. В нем вы будете находиться, пока не не выполните команду /end, /help или /start."),
                     sep="\n")
        )
    except:
        msg_text = fmt.text(
            fmt.text(
                     fmt.hitalic(
                         "Вы вошли в режим переводчика. В нем вы будете находиться, пока не не выполните команду /end, /help или /start."),
                     sep="\n")
        )
    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    await bot.send_message(message.from_user.id, text=emojize('➡ Введите слово!'), reply_markup=inline_kb_exit)





#Принимаем перевод слова и сбрасываем стейт в инит
#'test_state_0': 'Начальное состояние инициации',
@dp.message_handler(state=TranslateModeStates.input_word)
async def process_add_word_add_translate_command(message: types.Message, state:FSMContext):

    #async with state.proxy() as data:
    #    data['word'] = message.text

    await state.update_data(word=message.text.lower(), user_id=message.from_user.id)

    data = await state.get_data()
    res = await add_word(data['word'], '', data['user_id'])
    decode_res = json.loads(res)

    msg_text = fmt.text(
        fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
        fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
                 fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
                 sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 1:
        await bot.send_message(chat_id=message.from_user.id, text=f"-> Вы можете сделать:", reply_markup=inline_kb_YN)
        await state.set_state(TranslateModeStates.choosing_edit_mode)
    else:
        await bot.send_message(message.from_user.id, text=emojize('➡ Введите перевод слова!'), reply_markup=inline_kb_chancel)
        await state.set_state(TranslateModeStates.input_translation)





@dp.message_handler(state=TranslateModeStates.input_translation)
async def process_add_word_add_translate_command(message: types.Message, state:FSMContext):

    await state.update_data(translation_base=message.text.lower(), user_id=message.from_user.id)
    data = await state.get_data()
    res = await add_word(data['word'], data['translation_base'], data['user_id'])
    decode_res = json.loads(res)

    msg_text = fmt.text(
        fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
        fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
        fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
        sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 1:
        await bot.send_message(chat_id=message.from_user.id, text=f"-> Вы можете сделать:", reply_markup=inline_kb_YN)
        await state.set_state(TranslateModeStates.choosing_edit_mode)
    else:
        await bot.send_message(message.from_user.id, text=emojize('➡ Введите слово!'))
        await state.set_state(TranslateModeStates.input_word)




@dp.callback_query_handler(lambda c: c.data in ['delete'], state=TranslateModeStates.choosing_edit_mode)
async def button_delete_click_call_back(callback_query: types.CallbackQuery, state:FSMContext):

    await bot.answer_callback_query(callback_query.id)

    data = await state.get_data()
    await bot.send_message(chat_id=data['user_id'],text=f"{data['word']}")
    res = await del_word(data['word'], data['user_id'])
    decode_res = json.loads(res)


    msg_text = fmt.text(
            fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
            fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
                     fmt.text(fmt.hbold(decode_res['word']), "="),
                     sep="\n")
    )

    await bot.send_message(chat_id=data['user_id'], text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 0:
        await bot.send_message(chat_id=data['user_id'], text=f"-> Вы можете сделать:", reply_markup=inline_kb_YN)
        await state.set_state(TranslateModeStates.choosing_edit_mode)

    await bot.send_message(data['user_id'], text=emojize('➡ Введите слово!'))
    await state.set_state(TranslateModeStates.input_word)

@dp.callback_query_handler(lambda c: c.data in ['go'], state=TranslateModeStates.choosing_edit_mode)
async def button_go_click_call_back(callback_query: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], text=emojize('➡ Введите слово!'))
    await state.set_state(TranslateModeStates.input_word)

@dp.callback_query_handler(lambda c: c.data in ['exit'], state=[TranslateModeStates.choosing_edit_mode, TranslateModeStates.input_translation, TranslateModeStates.input_word])
async def button_exit_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.reset_state()
    msg_text = fmt.text(fmt.text("\nСообщение: ", fmt.hitalic("Вы вышли из режима перевода. Воспользуйтесь командами /end, /help или /start."),
                 sep="\n"))

    await bot.send_message(chat_id=data['user_id'], text=msg_text, parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data in ['chancel'], state=[TranslateModeStates.input_translation, TranslateModeStates.input_word])
async def button_exit_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], text=emojize('➡ Введите слово!'))
    await state.set_state(TranslateModeStates.input_word)









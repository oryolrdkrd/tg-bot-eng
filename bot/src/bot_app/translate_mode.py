import json
from aiogram import types
from . app import dp, bot
from aiogram.dispatcher import FSMContext
from . states import TestStates, DeskriptionStates, TranslateModeStates, RandomModeStates
from . data_fetcher import add_word, del_word, update_word
from . keyboards import inline_kb_YN, inline_kb_chancel, inline_kb_exit, in_kb_main_menu, in_kb_change_word
import aiogram.utils.markdown as fmt
from emoji import emojize
from . messages import MESSAGES




@dp.message_handler(state='*', commands=['t'])
#
#   Входим в режим переводчика. Предлагаем ввести слово
#
async def process_add_word_setstate_command(message: types.Message):

    state = dp.current_state(user=message.from_user.id)
    await state.update_data(word=message.text.lower(), user_id=message.from_user.id)
    await state.set_state(TranslateModeStates.input_word)
    try:
        msg_text = fmt.text(fmt.hitalic(MESSAGES['translater_mode']), sep="\n")
    except:
        msg_text = fmt.text(fmt.hitalic(MESSAGES['translater_mode']), sep="\n")
    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit,
                           parse_mode=types.ParseMode.MARKDOWN_V2)



@dp.message_handler(state=TranslateModeStates.input_word)
#
#   Получаем слово. Делаем запрос. Выводим перевод или предлагаем ввод перевода
#
async def process_add_word_add_translate_command(message: types.Message, state:FSMContext):

    #async with state.proxy() as data:
    #    data['word'] = message.text

    await state.update_data(word=message.text.lower(), user_id=message.from_user.id)

    data = await state.get_data()
    res = await add_word(data['word'], '', data['user_id'])
    decode_res = json.loads(res)

    msg_text = fmt.text(
        #fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
        #fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
        fmt.text("\n", fmt.hitalic(decode_res['msg']),
                 fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
                 sep="\n")
    )

    await state.update_data(translation_base=decode_res['translation_base'])

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 1:
        #
        #   Если такое слово уже существет мы предлагаем меню с действиями
        #
        await bot.send_message(chat_id=message.from_user.id, text="➡️ _Вы можете сделать_\:", reply_markup=inline_kb_YN)
        await state.set_state(TranslateModeStates.choosing_edit_mode)
    else:
        await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_t'], reply_markup=inline_kb_chancel)
        await state.set_state(TranslateModeStates.input_translation)





@dp.message_handler(state=TranslateModeStates.input_translation)
async def process_add_word_add_translate_command(message: types.Message, state:FSMContext):

    await state.update_data(translation_base=message.text.lower(), user_id=message.from_user.id)
    data = await state.get_data()
    res = await add_word(data['word'], data['translation_base'], data['user_id'])
    decode_res = json.loads(res)

    msg_text = fmt.text(
        # fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
        # fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
        fmt.text(fmt.hitalic(decode_res['msg']),
        fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
        sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 1:
        await bot.send_message(chat_id=message.from_user.id, text="➡️ _Вы можете сделать_\:", reply_markup=inline_kb_YN)
        await state.set_state(TranslateModeStates.choosing_edit_mode)
    else:
        await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit)
        await state.set_state(TranslateModeStates.input_word)




@dp.callback_query_handler(lambda c: c.data in ['delete'], state=TranslateModeStates.choosing_edit_mode)
async def button_delete_click_call_back(callback_query: types.CallbackQuery, state:FSMContext):

    await bot.answer_callback_query(callback_query.id)

    data = await state.get_data()
    await bot.send_message(chat_id=data['user_id'],text=f"{data['word']}")
    res = await del_word(data['word'], data['user_id'])
    decode_res = json.loads(res)


    msg_text = fmt.text(
            # fmt.text(fmt.hunderline("Статус"), "=", decode_res['status']),
            # fmt.text("\nСообщение: ", fmt.hitalic(decode_res['msg']),
            fmt.text(fmt.hitalic(decode_res['msg']),
                     fmt.text(fmt.hbold(decode_res['word']), "="),
                     sep="\n")
    )

    await bot.send_message(chat_id=data['user_id'], text=msg_text, parse_mode="HTML")
    if decode_res['status'] == 0:
        await bot.send_message(chat_id=data['user_id'], text="➡️ _Вы можете сделать_\:", reply_markup=inline_kb_YN)
        await state.set_state(TranslateModeStates.choosing_edit_mode)

    await bot.send_message(data['user_id'], text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit, parse_mode='MarkdownV2')
    await state.set_state(TranslateModeStates.input_word)

@dp.callback_query_handler(lambda c: c.data in ['go'], state=TranslateModeStates.choosing_edit_mode)
async def button_go_click_call_back(callback_query: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit)
    await state.set_state(TranslateModeStates.input_word)

@dp.callback_query_handler(lambda c: c.data in ['exit'], state=[TranslateModeStates.choosing_edit_mode, TranslateModeStates.input_translation, TranslateModeStates.input_word])
async def button_exit_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    #await state.reset_state()
    msg_text = fmt.text(fmt.text(fmt.hitalic("Вы вышли из режима перевода. Воспользуйтесь командами /help или /start."),
                 sep="\n"))

    await bot.send_message(chat_id=data['user_id'], text=msg_text, parse_mode="HTML", reply_markup=in_kb_main_menu)





@dp.callback_query_handler(lambda c: c.data in ['chancel'], state=[TranslateModeStates.input_translation, TranslateModeStates.input_word])
async def button_exit_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(data['user_id'], text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit)
    await state.set_state(TranslateModeStates.input_word)


@dp.callback_query_handler(lambda c: c.data in ['translater'], state="*")
async def button_translater_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    state = dp.current_state(user=data['user_id'])
    await state.set_state(TranslateModeStates.input_word)
    try:
        msg_text = fmt.text(fmt.hitalic(MESSAGES['translater_mode']), sep="\n")
    except:
        msg_text = fmt.text(fmt.hitalic(MESSAGES['translater_mode']), sep="\n")

    await bot.send_message(chat_id=data['user_id'], text=msg_text, parse_mode="HTML")
    await bot.send_message(chat_id=data['user_id'], text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit)


@dp.callback_query_handler(lambda c: c.data in ['change'], state="*")
#
#   Режим изменения слова или перевода
#
async def button_translater_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    state = dp.current_state(user=data['user_id'])
    await state.set_state(TranslateModeStates.choosing_edit_mode)

    msg_text = "_Что конкретно вы хотите изменить_\? \u2694\ufe0f \n" \
            "`\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- `\n" \
            f"*Слово*\: `{data['word']}` \n" \
            "_или_\ \n" \
            f"*Перевод*\: `{data['translation_base']}`  \n"

    await bot.send_message(chat_id=data['user_id'], text=msg_text, reply_markup=in_kb_change_word)




@dp.callback_query_handler(lambda c: c.data in ['change_word'], state=TranslateModeStates.choosing_edit_mode)
#
#   Нажата кнопка изменения слова
#
async def cmd_change_word(message: types.Message, state:FSMContext):

    data = await state.get_data()
    await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_w'], reply_markup=inline_kb_chancel,
                           parse_mode=types.ParseMode.MARKDOWN_V2)
    await state.set_state(TranslateModeStates.edit_word)


@dp.callback_query_handler(lambda c: c.data in ['change_translation'], state=TranslateModeStates.choosing_edit_mode)
#
#   Нажата кнопка изменения перевода
#
async def cmd_change_translate(message: types.Message, state:FSMContext):

    data = await state.get_data()
    await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_t'], reply_markup=inline_kb_chancel,
                           parse_mode=types.ParseMode.MARKDOWN_V2)
    await state.set_state(TranslateModeStates.edit_translate)

@dp.message_handler(state=TranslateModeStates.edit_word)
#
#   Получено новое слово
#
async def process_update_word(message: types.Message, state:FSMContext):

    await state.update_data(word_edit=message.text.lower(), translation_edit='')
    data = await state.get_data()
    #await bot.send_message(chat_id=message.from_user.id, text=f"{data['word']}, {data['word_edit']}, {data['translation_edit']}, {data['user_id']}", parse_mode="HTML")

    res = await update_word(data['word'], data['word_edit'], data['translation_edit'], data['user_id'])
    decode_res = json.loads(res)


    msg_text = fmt.text(
        fmt.text(fmt.hitalic(decode_res['msg']),
        fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
        sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")

    await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit)
    await state.set_state(TranslateModeStates.input_word)


@dp.message_handler(state=TranslateModeStates.edit_translate)
#
#   Получено новый перевод
#
async def process_update_translate(message: types.Message, state:FSMContext):

    await state.update_data(word_edit='', translation_edit=message.text.lower())
    data = await state.get_data()
    #await bot.send_message(chat_id=message.from_user.id, text=f"{data['word']}, {data['word_edit']}, {data['translation_edit']}, {data['user_id']}", parse_mode="HTML")

    res = await update_word(data['word'], data['word_edit'], data['translation_edit'], data['user_id'])
    decode_res = json.loads(res)


    msg_text = fmt.text(
        fmt.text(fmt.hitalic(decode_res['msg']),
        fmt.text(fmt.hbold(decode_res['word']), "=", fmt.hbold(decode_res['translation_base'])),
        sep="\n")
    )

    await bot.send_message(chat_id=message.from_user.id, text=msg_text, parse_mode="HTML")

    await bot.send_message(message.from_user.id, text=MESSAGES['tm_in_w'], reply_markup=inline_kb_exit)
    await state.set_state(TranslateModeStates.input_word)









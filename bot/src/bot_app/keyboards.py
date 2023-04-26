from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from keyboa import Keyboa

#Создаем 3 объекта-кнопки

inline_button_male = InlineKeyboardButton('Мужской', callback_data='male')
inline_button_neuter = InlineKeyboardButton('Средний', callback_data='neuter')
inline_button_femail= InlineKeyboardButton('Женский', callback_data='female')
inline_button_exit= InlineKeyboardButton('Завершить игру', callback_data='exit')
inline_button_add= InlineKeyboardButton('Добавить слово', callback_data='add_word_command')



kb_test = [
    [
        InlineKeyboardButton("Option 1", callback_data="1"),
        InlineKeyboardButton("Option 2", callback_data="2"),
    ],
    [InlineKeyboardButton("Option 3", callback_data="3")],
]

kbt = InlineKeyboardMarkup(kb_test)


#Связываем кнопки в клавиатуру
inline_kb = InlineKeyboardMarkup()
inline_kb.add(inline_button_male)
inline_kb.add(inline_button_neuter)
inline_kb.add(inline_button_femail)
inline_kb.add(inline_button_exit)

inline_kb_1 = InlineKeyboardMarkup()
inline_kb_1.add(inline_button_add)



menu_YN = ["Да", "Нет"]
keyboard_YN = Keyboa(items=menu_YN)

button_hi = KeyboardButton('Привет! 👋')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)


button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')

# Меню из 3х вертикальных кнопок
markup3 = ReplyKeyboardMarkup().add(button1).add(button2).add(button3)
# Меню из 3х горизонатльныых кнопок
markup4 = ReplyKeyboardMarkup().row(button1, button2, button3)

markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Средний ряд'))

button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.insert(button6)

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)


markup_big = ReplyKeyboardMarkup()

markup_big.add(
    button1, button2, button3, button4, button5, button6
)
markup_big.row(
    button1, button2, button3, button4, button5, button6
)

markup_big.row(button4, button2)
markup_big.add(button3, button2)
markup_big.insert(button1)
markup_big.insert(button6)
markup_big.insert(KeyboardButton('9️⃣'))



#==================== InLine
inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))


#Клавиатура Да/Нет
inline_button_change = InlineKeyboardButton('⚛ Изменить', callback_data='change')
inline_button_delete = InlineKeyboardButton('☠ Удалить', callback_data='delete')
inline_button_go = InlineKeyboardButton('➡ Дальше', callback_data='go')
inline_button_exit = InlineKeyboardButton('🌂 Закончить', callback_data='exit')
inline_kb_YN = InlineKeyboardMarkup()
inline_kb_YN.add(inline_button_change, inline_button_delete, inline_button_go, inline_button_exit)

#Клавиатура Да/Нет
inline_button_chancel = InlineKeyboardButton('✖ Отменить', callback_data='chancel')
inline_kb_chancel = InlineKeyboardMarkup()
inline_kb_chancel.add(inline_button_chancel, inline_button_exit)

#Клавиатура с кнопкой "Закончить"
inline_kb_exit = InlineKeyboardMarkup()
inline_kb_exit.add(inline_button_exit)

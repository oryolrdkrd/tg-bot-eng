from . import states
from emoji import emojize

#приветствие бота
WELCOME_MESSAGE = '''
Hello! I can hep you to memorize English noun gender!
For more info go to <a href="http://www.example.com/">TG-Bot</a>\n
Comands are:
/train_ten
/train_all
/add_word
'''


help_message_old = 'Для того, чтобы изменить текущее состояние пользователя, ' \
               f'отправь команду "/setstate x", где x - число от 0 до {len(states.TestStates.all()) - 1}.\n' \
               'Чтобы сбросить текущее состояние, отправь "/setstate" без аргументов.'

help_message = "Итак, мне приятно рассказать тебе, что я умею: \n" \
               "/add_word \n" \
               "Добавление нового слова в твою базу данных \n" \
               "/train_ten \n" \
               "Это игра, в которой ты получаешь 10 случайных слов со случайными вариантами перевода. \n" \
               "/t\n" \
               "Это запрос перевода слова. При этом будет фиксироваться частота обращения к этому слову\n" \
               "/train_freq\n" \
               "Это тренировка твоих самых частотных запросов. После 3-х правильных ответов частота снижается. "

start_message = "Привет\! Я бот, который помогает быстро изучать английские слова\. " \
                "Для понимания что я умею можешь выполнить команду /help \n" \
                "А чтобы выйти из всех режимов, введи /start"
invalid_key_message = 'Ключ "{key}" не подходит.\n' + help_message
state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}":"{des_current_state}", что удовлетворяет условию "один из {states}"'
add_word_message = emojize(':right_arrow: Введите английское слово:')
translater_mode_message = 'Вы вошли в режим Переводчика. Работает он так: вы вводите слово и получаете его перевод, если такого ' \
                          'слова нет, то вам будет предложено его добавить.'
translater_mode_input_word = "➡ Переводчик: *Введите слово*\!"

MESSAGES = {
    'start': start_message,
    'help': help_message,
    'invalid_key': invalid_key_message,
    'state_change': state_change_success_message,
    'state_reset': state_reset_message,
    'current_state': current_state_message,
    'add_word': add_word_message,
    'translater_mode': translater_mode_message,
    'tm_in_w': translater_mode_input_word
}

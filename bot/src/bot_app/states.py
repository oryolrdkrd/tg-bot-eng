from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.helper import Helper, HelperMode, ListItem

#Описываем 3 наших состояния с помощью класса
class GameStates(StatesGroup):
    start = State()
    random_ten = State()
    all_words = State()
    add_word = State()

class TestStates(Helper):
    mode = HelperMode.snake_case
    TEST_STATE_0 = ListItem() #Нулевое состояние, используем для сброса в исходное состояние
    TEST_STATE_1 = ListItem() #Сейчас будет происходить добавление нового слова
    TEST_STATE_2 = ListItem() #Сейчас будет добавление перевода
    TEST_STATE_3 = ListItem() #
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()

#словарь расшифровки состояний
DeskriptionStates = {
    'test_state_0': 'Начальное состояние инициации',
    'test_state_1': 'Справка. Инициация',
    'test_state_2': 'Добавление слова. Предложено ввести слово для добавления в словарь',
    'test_state_3': 'Добавление слова. Предложено ввести перевод этого слова',
    'test_state_4': 'Режим перевода: ждем ввода слова для перевода'
}

class TranslateModeStates(StatesGroup):
    input_word = State()
    input_translation = State()
    delete = State()
    choosing_edit_mode = State()
    edit_word = State()
    edit_translate = State()

class RandomModeStates(StatesGroup):
    input_word = State()


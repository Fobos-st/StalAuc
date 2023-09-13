from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

main_button = [
    [types.KeyboardButton(text="Проверка цены"),
     types.KeyboardButton(text="Ожидание предмета")],
    [types.KeyboardButton(text="Текущий запрос"),
     types.KeyboardButton(text="Удалить запрос")]

]
main_kb = types.ReplyKeyboardMarkup(keyboard=main_button, resize_keyboard=True, one_time_keyboard=False)


quality_inline_button = [
    [types.InlineKeyboardButton(text='Обычный', callback_data='0')],
    [types.InlineKeyboardButton(text='Необычный', callback_data='1')],
    [types.InlineKeyboardButton(text='Особый', callback_data='2')],
    [types.InlineKeyboardButton(text='Редкий', callback_data='3')],
    [types.InlineKeyboardButton(text='Исключительный', callback_data='4')],
    [types.InlineKeyboardButton(text='Легендарный', callback_data='5')],
]

quality_inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=quality_inline_button)

additional_inline_keyboard = types.InlineKeyboardMarkup()
for i in range(1, 16):
    additional_inline_keyboard.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}'))
additional_inline_keyboard.add(types.InlineKeyboardButton(text='Без разницы', callback_data='All'))


cancel_button = [
    [types.InlineKeyboardButton(text='Отмена❌', callback_data='Отмена')]
]

cancel_inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=cancel_button)


async def get_keyboard_item(choices):
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    for choice in choices.keys():
        kb.add(
            InlineKeyboardButton(choice, callback_data=f'{choices.get(choice)}'),
        )
    kb.add(types.InlineKeyboardButton(text='Отмена❌', callback_data='Отмена'))
    return kb

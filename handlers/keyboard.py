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


async def get_control_menu(callback: str) -> types.inline_keyboard.InlineKeyboardMarkup:
    """
    В завистимости от callback.data определяет изменения клавиатуры
    :param callback: callback_data
    :return: InlineKeyboard
    """
    callback = callback.split()
    page = int(callback[1])
    id_item = callback[2]
    if callback[0] == "add_page":
        page += 1
        if callback[3] == 'asc':
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} asc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} asc")],
                [types.InlineKeyboardButton(text="Выкуп 🔼", callback_data=f"none {page} {id_item} desc")]
            ]
        else:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} desc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
            ]
        ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
        return ikb
    elif callback[0] == "remove_page":
        page -= 1
        if page == 1:
            if callback[3] == 'asc':
                auc_table_inline_button = [
                    [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                     types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                    [types.InlineKeyboardButton(text="Выкуп 🔼", callback_data=f"none {page} {id_item} desc")]
                ]
            else:
                auc_table_inline_button = [
                    [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                     types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                    [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
                ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
            return ikb
        else:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} desc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
            return ikb
    elif callback[3] == 'asc':
        if page == 1:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} asc")],
                [types.InlineKeyboardButton(text="Выкуп 🔼", callback_data=f"none {page} {id_item} desc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
            return ikb
        else:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} asc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} asc")],
                [types.InlineKeyboardButton(text="Выкуп 🔼", callback_data=f"none {page} {id_item} desc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
            return ikb
    elif callback[3] == 'desc':
        if page == 1:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
            return ikb
        else:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} desc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
            return ikb

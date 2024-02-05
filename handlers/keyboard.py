from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_button = [
    [types.KeyboardButton(text="Проверка цены"),
     types.KeyboardButton(text="Ожидание предмета")],
    [types.KeyboardButton(text="Текущий запрос"),
     types.KeyboardButton(text="Удалить запрос")],
    [types.KeyboardButton(text="Средняя цена"),
     types.KeyboardButton(text="История цен")],
    [types.KeyboardButton(text="Перекуп таблица"),
     types.KeyboardButton(text="Финанс.помощь проекту")]
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


auction_choice_button = [
    [types.InlineKeyboardButton(text='Проверка цены', callback_data='auction_check_price'),
     types.InlineKeyboardButton(text='Графики цены', callback_data='auction_chart_price')],
    [types.InlineKeyboardButton(text='Средняя цена', callback_data='auction_average_price')],
]
auction_choice_keyboard = types.InlineKeyboardMarkup(inline_keyboard=auction_choice_button)


background_process_choice_button_0 = [
    [types.InlineKeyboardButton(text='Добавить предмет', callback_data='auction_check_price')],
]
background_process_choice_keyboard_0 = types.InlineKeyboardMarkup(inline_keyboard=background_process_choice_button_0)

background_process_choice_button_1 = [
    [types.InlineKeyboardButton(text='Изменить предмет', callback_data='auction_check_price')],
    [types.InlineKeyboardButton(text='Удалить предмет', callback_data='auction_check_price')]
]
background_process_choice_keyboard_1 = types.InlineKeyboardMarkup(inline_keyboard=background_process_choice_button_1)


additional_inline_button = [
    [types.InlineKeyboardButton(text=f'{1}', callback_data=f'{1}'),
     types.InlineKeyboardButton(text=f'{2}', callback_data=f'{2}'),
     types.InlineKeyboardButton(text=f'{3}', callback_data=f'{3}')],
    [types.InlineKeyboardButton(text=f'{4}', callback_data=f'{4}'),
     types.InlineKeyboardButton(text=f'{5}', callback_data=f'{5}'),
     types.InlineKeyboardButton(text=f'{6}', callback_data=f'{6}')],
    [types.InlineKeyboardButton(text=f'{7}', callback_data=f'{7}'),
     types.InlineKeyboardButton(text=f'{8}', callback_data=f'{8}'),
     types.InlineKeyboardButton(text=f'{9}', callback_data=f'{9}')],
    [types.InlineKeyboardButton(text=f'{10}', callback_data=f'{10}'),
     types.InlineKeyboardButton(text=f'{11}', callback_data=f'{11}'),
     types.InlineKeyboardButton(text=f'{12}', callback_data=f'{12}')],
    [types.InlineKeyboardButton(text=f'{13}', callback_data=f'{13}'),
     types.InlineKeyboardButton(text=f'{14}', callback_data=f'{14}'),
     types.InlineKeyboardButton(text=f'{15}', callback_data=f'{15}')]
]
additional_inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=additional_inline_button)
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
                     types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} asc")],
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
    elif callback[3] == 'asc':
        if page == 1:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} asc")],
                [types.InlineKeyboardButton(text="Выкуп 🔼", callback_data=f"none {page} {id_item} desc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
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
        else:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} desc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
                 types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
                [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
            ]
            ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
        return ikb

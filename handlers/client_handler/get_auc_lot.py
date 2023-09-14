from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import API_request
import database.dbitem
import handlers.keyboard
import text
from create_bot import bot
from ..keyboard import cancel_inline_keyboard, get_control_menu


class WaitItemName(StatesGroup):
    text = State()


# @dp.message_handler()
async def cmd_item_check_check_item(message: types.Message):
    if message.text == "Проверка цены":
        await WaitItemName.text.set()
        await message.answer(text.input_item_name_messeage,
                             reply_markup=cancel_inline_keyboard)
    else:
        pass


# @dp.message_handler(content_types=["text"], state=WaitItemName.text)
async def get_item_name(message: types.Message, state: FSMContext):
    id_item = database.dbitem.search_item_id_by_name(message.text, "RU")
    print(message.from_user.first_name)
    if len(id_item) > 1:
        kb = await handlers.keyboard.get_keyboard_item(id_item)
        return await message.reply('Нашёл несколько вариантов, выберете ниже', reply_markup=kb)
    elif len(id_item) == 1:
        id_item = list(id_item.values())[0]
        page = 1
        auc_table_inline_button = [
            [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
             types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
            [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
        ]
        ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)

        await bot.send_message(message.from_user.id, await API_request.get_auc_item_first(id_item),
                               reply_markup=ikb)
        await state.finish()
    else:
        await message.answer('Такого предмета нету в нашем списке(')
        await state.finish()


# @dp.callback_query_handler(state=WaitItemName.text)
async def cmd_request(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Отмена":
        await state.finish()
        await bot.send_message(callback_query.from_user.id, ":-(")
    else:
        await state.finish()
        await callback_query.message.delete()
        callback_data = callback_query.data
        page = 1
        id_item = callback_data
        auc_table_inline_button = [
            [types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip"),
             types.InlineKeyboardButton(text="▶️", callback_data=f"add_page {page} {id_item} desc")],
            [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
        ]
        ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
        await state.finish()
        text = await API_request.get_auc_item_first(callback_data)
        if text == 'Даного предмета нету на аукционе(':
            await bot.send_message(callback_query.from_user.id, text)
        else:
            await bot.send_message(callback_query.from_user.id, text,
                                   reply_markup=ikb)


# @dp.callback_query_handler()
async def changing_the_list_of_lots(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Отмена":
        await state.finish()
        await bot.send_message(callback_query.from_user.id, ":-(")
    if callback_query.data.split()[1] == 'skip':  #изменить проверку этого условия для скипа(сделать так что другие callback_data пропускает мимо)
        return
    last_page, text_msg = await API_request.get_auc_item(callback_query.data.split())
    if last_page:
        page = int(callback_query.data.split()[1]) + 1
        id_item = callback_query.data.split()[2]
        if callback_query.data.split()[3] == 'asc':
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} asc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip")],
                [types.InlineKeyboardButton(text="Выкуп 🔼", callback_data=f"none {page} {id_item} desc")]
            ]
        else:
            auc_table_inline_button = [
                [types.InlineKeyboardButton(text="◀️", callback_data=f"remove_page {page} {id_item} desc"),
                 types.InlineKeyboardButton(text=f"Страница: {page}", callback_data="numer_page skip")],
                [types.InlineKeyboardButton(text="Выкуп 🔽", callback_data=f"none {page} {id_item} asc")]
            ]
        ikb = types.InlineKeyboardMarkup(inline_keyboard=auc_table_inline_button)
    else:
        ikb = await get_control_menu(callback_query.data)
    await callback_query.message.edit_text(text_msg,
                                           reply_markup=ikb)


def register_client_handlers_get_auc_lot(dp: Dispatcher):
    dp.register_message_handler(cmd_item_check_check_item, content_types=['text'], text="Проверка цены")
    dp.register_message_handler(get_item_name, content_types=['text'], state=WaitItemName.text)
    dp.register_callback_query_handler(cmd_request, state=WaitItemName.text)

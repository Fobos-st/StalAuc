from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import text
from create_bot import bot
from database.dbitem import search_item_id_by_name, search_item_name_by_id, is_it_artifact
from database.dbsql import delete_request
from database.dbsql import update_sqlite_table
from text import current_request
from ..keyboard import cancel_inline_keyboard, get_keyboard_item
from ..keyboard import (main_kb, quality_inline_keyboard,
                        additional_inline_keyboard,
                        background_process_choice_keyboard_0,
                        background_process_choice_keyboard_1)


class MakeRequestUser(StatesGroup):
    item_name = State()
    item_id = State()
    price = State()
    quality = State()
    additional = State()


async def delete_current_user_request(callback_query: types.CallbackQuery):
    delete_request(callback_query.from_user.id)
    await callback_query.message.edit_text(text="Вы ещё не выбирали предметы",
                                           reply_markup=background_process_choice_keyboard_0)


async def cmd_item_check_check_item(callback_query: types.CallbackQuery):
    await MakeRequestUser.item_name.set()
    await bot.send_message(callback_query.from_user.id, text.input_item_name_messeage,
                           reply_markup=cancel_inline_keyboard)


# @dp.message_handler(content_types=["text"], state=MakeRequestUser.item_name)
async def get_item_name(message: types.Message, state: FSMContext):
    id_item = search_item_id_by_name(message.text, "RU")
    if len(id_item) > 1:
        kb = await get_keyboard_item(id_item)
        return await message.reply('Нашёл несколько вариантов, выберете ниже', reply_markup=kb)
    elif len(id_item) == 1:
        callback_data = list(id_item.values())[0]
        await state.update_data(item_name=message.text)
        await message.answer('Напишите цену выкупа предмета')
        await MakeRequestUser.next()
        await state.update_data(item_id=callback_data)
        await MakeRequestUser.next()
    else:
        await message.answer('Такого предмета нету в нашем списке, а может быть Зив его куда-то унёс во время зимней вечеринки с пивом!🍻',
                             reply_markup=main_kb)
        await state.finish()


# @dp.callback_query_handler(state=MakeRequestUser.item_name)
async def reg_request_in_db_one(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Отмена":
        await state.finish()
        await bot.send_message(callback_query.from_user.id, "(", reply_markup=main_kb)
        await callback_query.message.delete()
    else:
        await callback_query.message.delete()
        callback_data = callback_query.data
        await state.update_data(item_name=search_item_name_by_id(callback_data))
        await bot.send_message(chat_id=callback_query.from_user.id, text='Замечательно')
        await MakeRequestUser.next()
        await state.update_data(item_id=callback_data)
        await MakeRequestUser.next()
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Напишите цену выкупа предмета, Введите сумму без пробелов и запятых')


# @dp.message_handler(content_types=["text"], state=MakeRequestUser.price)
async def reg_request_in_db_two(message: types.Message, state: FSMContext):
    try:
        text_user_msg = int(message.text)
        await state.update_data(price=text_user_msg)
        data = await state.get_data()
        if is_it_artifact(data["item_id"]):
            await MakeRequestUser.next()
            await message.answer(
                'Выберете редкость \nПри появления артфеакта подходящего для вас по цене будут отмечаться как артефакты и более '
                'высокой редкости так и выбранной изначально', reply_markup=quality_inline_keyboard)
        else:
            update_sqlite_table(message.from_user.id, data['item_id'], data['price'])
            await state.finish()
            await message.answer(text=f"Ваш текущий лот: \n {current_request(message.from_user.id)}",
                                 reply_markup=background_process_choice_keyboard_1)
    except ValueError:
        await message.answer('Неправильная форма записи', reply_markup=main_kb)


# @dp.callback_query_handler(state=MakeRequestUser.quality)
async def reg_request_in_db_three(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(quality=callback_query.data)
    await MakeRequestUser.next()
    await callback_query.message.delete()
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выберите от 0-15 качество артефакта',
                           reply_markup=additional_inline_keyboard)


# @dp.callback_query_handler(state=MakeRequestUser.additional)
async def reg_request_in_db_four(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.update_data(additional=callback_query.data)
    data = await state.get_data()
    additional = 'Любая' if data['additional'] == 'All' else f"от {data['additional']} и более"
    update_sqlite_table(user_id=callback_query.from_user.id,
                        item=data['item_id'],
                        price=data['price'],
                        quality=data['quality'],
                        additional=data['additional'])

    await bot.send_message(callback_query.from_user.id,
                           text=f"Ваш текущий лот: \n {current_request(callback_query.from_user.id)}",
                           reply_markup=background_process_choice_keyboard_1)
    await state.finish()


def register_client_handlers_user_request(dp: Dispatcher):
    dp.register_callback_query_handler(cmd_item_check_check_item, text="reg_user_request")
    dp.register_callback_query_handler(delete_current_user_request, text="del_user_request")
    dp.register_message_handler(get_item_name, content_types=['text'], state=MakeRequestUser.item_name)
    dp.register_callback_query_handler(reg_request_in_db_one, state=MakeRequestUser.item_name)
    dp.register_message_handler(reg_request_in_db_two, content_types=["text"], state=MakeRequestUser.price)
    dp.register_callback_query_handler(reg_request_in_db_three, state=MakeRequestUser.quality)
    dp.register_callback_query_handler(reg_request_in_db_four, state=MakeRequestUser.additional)

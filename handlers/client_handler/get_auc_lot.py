from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMedia
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime
import API_request
import database.dbitem
import handlers.keyboard
import text
from create_bot import bot, dp
from ..keyboard import cancel_inline_keyboard, get_control_menu
from PIL import Image, ImageDraw, ImageFont
import os


class WaitItemName(StatesGroup):
    text = State()


def remaining_time(time_str):
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    current_time = datetime.utcnow()
    target_time = datetime.strptime(time_str, time_format)
    remaining_time = target_time - current_time

    if remaining_time.days < 0:
        return "Время уже прошло"
    elif remaining_time.days > 0:
        if remaining_time.days == 1:
            return f"Остался {remaining_time.days} день"
        else:
            return f"Осталось {remaining_time.days} дня"
    elif remaining_time.seconds >= 3600:
        hours = remaining_time.seconds // 3600
        if 1 < hours < 5 or 22 <= hours <= 23:
            return f"Осталось {hours} часа"
        if 21 == hours or 1 == hours:
            return f"Остался {hours} час"
        else:
            return f"Осталось {hours} часов"
    elif remaining_time.seconds >= 60:
        minutes = remaining_time.seconds // 60
        return f"Осталось {minutes} минут"
    else:
        return f"Осталось {remaining_time.seconds} секунд"


async def create_get_auc_lot_img(lots: dict, id_item: str, username: str) -> str:
    #  Сделать перевод словарь с лотами сразу вне данной функции чтобы проверять
    #  длинну и в случае отсуствия лота не выводить пустой ПДА
    im2 = Image.open(database.dbitem.get_item_image(id_item)).convert("RGBA").resize((95, 95))
    im1 = Image.open('database/PDA.png')
    font = ImageFont.truetype("database/Roboto-Medium.ttf", size=22)
    font1 = ImageFont.truetype("database/Roboto-Medium.ttf", size=21)
    iteration = 0
    item_name = database.dbitem.search_item_name_by_id(id_item)
    for lot in lots:
        im1.paste(im2, (45, 95 + 99 * iteration))

        quality_color = {
            0: "EEEEEE",
            1: "70CF22",
            2: "2239CF",
            3: "d968c4",
            4: "FF0000",
            5: "FFF44D",
        }

        draw_text = ImageDraw.Draw(im1)
        try:
            if 'ptn' in lot['additional']:
                draw_text.text(
                    (150, 105 + 99 * iteration),
                    f'{item_name} +{lot["additional"]["ptn"]}',
                    # Добавляем шрифт к изображению
                    font=font,
                    fill=f'#{quality_color[lot["additional"]["qlt"]]}')
            else:
                draw_text.text(
                    (150, 105 + 99 * iteration),
                    f'{item_name}',
                    # Добавляем шрифт к изображению
                    font=font,
                    fill=f'#{quality_color[lot["additional"]["qlt"]]}')
        except Exception:
            if 'ptn' in lot['additional']:
                draw_text.text(
                    (150, 105 + 99 * iteration),
                    f'{item_name} +{lot["additional"]["ptn"]}',
                    # Добавляем шрифт к изображению
                    font=font,
                    fill=f'#{quality_color[0]}')
            else:
                draw_text.text(
                    (150, 105 + 99 * iteration),
                    f'{item_name}',
                    # Добавляем шрифт к изображению
                    font=font,
                    fill=f'#{quality_color[0]}')
        draw_text.text(
            (150, 150 + 99 * iteration),
            remaining_time(lot['endTime']),
            # Добавляем шрифт к изображению
            font=font1,
            fill='#cbaf2a')
        draw_text.text(
            (420, 128 + 99 * iteration),
            '{0:,}'.format(int(lot["startPrice"])).replace(',', '.'),
            # Добавляем шрифт к изображению
            font=font,
            fill='#DBDBDB')
        draw_text.text(
            (570, 128 + 99 * iteration),
            '{0:,}'.format(int(lot["buyoutPrice"])).replace(',', '.'),
            # Добавляем шрифт к изображению
            font=font,
            fill='#DBDBDB')
        draw_text.text(
            (750, 100 + 99 * iteration),
            ' ',
            # Добавляем шрифт к изображению
            font=font1,
            fill='#DBDBDB')
        draw_text.text(
            (750, 125 + 99 * iteration),
            'В разработке',
            # Добавляем шрифт к изображению
            font=font1,
            fill='#DBDBDB')
        draw_text.text(
            (750, 150 + 99 * iteration),
            ' ',
            # Добавляем шрифт к изображению
            font=font1,
            fill='#DBDBDB')

        iteration += 1

    filename = username + id_item + ".png"
    im1.save(filename, quality=5, font=font)
    im1.close()
    im2.close()
    return filename


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

        lots = await API_request.get_auc_item_first(id_item)
        if len(lots) != 0:
            filename = await create_get_auc_lot_img(lots, id_item, message.from_user.first_name)
            with open(filename, 'rb') as file:
                await bot.send_photo(message.from_user.id, file,
                                     reply_markup=ikb)
            os.remove(filename)
        else:
            await message.answer('Предмета нету на аукционе в данный момент')
        await state.finish()
    else:
        await message.answer('Такого предмета нету в нашем списке(')
        await state.finish()


# @dp.callback_query_handler(state=WaitItemName.text)
async def cmd_req(callback_query: types.CallbackQuery, state: FSMContext):
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
        lots = await API_request.get_auc_item_first(id_item)
        if len(lots) != 0:
            filename = await create_get_auc_lot_img(lots, id_item, callback_query.from_user.first_name)
            with open(filename, 'rb') as file:
                await bot.send_photo(callback_query.from_user.id, file,
                                     reply_markup=ikb)
            os.remove(filename)
        else:
            print(len(lots))
            await bot.send_message(callback_query.from_user.id, 'Предмета нету на аукционе в данный момент')


# @dp.callback_query_handler()
async def changing_the_list_of_lots(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "Отмена":
        await state.finish()
        await bot.send_message(callback_query.from_user.id, ":-(")
    if callback_query.data.split()[1] == 'skip':  #изменить проверку этого условия для скипа(сделать так что другие callback_data пропускает мимо)
        return
    last_page, lots = await API_request.get_auc_item(callback_query.data.split())
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

    if len(lots) != 0:
        filename = await create_get_auc_lot_img(lots, callback_query.data.split()[2], callback_query.from_user.first_name)
        with open(filename, 'rb') as file:
            photo = InputMedia(type="photo", media=file)
            await callback_query.message.edit_media(media=photo,
                             reply_markup=ikb)
        os.remove(filename)
    else:
        print(len(lots))


def register_client_handlers_get_auc_lot(dp: Dispatcher):
    dp.register_message_handler(cmd_item_check_check_item, content_types=['text'], text="Проверка цены")
    dp.register_message_handler(get_item_name, content_types=['text'], state=WaitItemName.text)
    dp.register_callback_query_handler(cmd_req, state=WaitItemName.text)
    dp.register_callback_query_handler(changing_the_list_of_lots)

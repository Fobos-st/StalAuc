from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import bot
from database.dbsql import reg
from ..keyboard import main_kb


# @dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           r"CAACAgIAAxkBAAEKk1FlNKx8auj72PEN0OqPy1pH7uGKCAACQAEAAladvQps6VtALEnWJTAE")
    await message.answer("""Бот находится в разработке и на данный момент он в MVP состояние
Проще говоря в бета-тесте""")
    ikb = InlineKeyboardMarkup(row_width=1)
    ikb.add(InlineKeyboardButton('Русский', callback_data='Russian'))
    await message.answer("Привет! Выбери язык, чтобы окунуться в Хэллоуинский дух торговли!", reply_markup=ikb)


# @dp.callback_query_handler(text=['Russian'])
async def cmd_server_selection(callback_query: types.CallbackQuery):
    # language depending on the choice
    reg(callback_query.from_user.id)
    ikb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    ikb.add(InlineKeyboardButton('RU', callback_data='RU'))
    await bot.send_message(callback_query.from_user.id, "Выберите ваш игровой сервер на этот страшный Хэллоуин💀:", reply_markup=ikb)


# @dp.callback_query_handler(text=['RU'])
async def cmd_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, """
🎃Добро пожаловать в мир Хэллоуина из темных просторов Чернобыльской Зоны!🧟‍♂️

В этом магическом боте скрыты 3 загадочные функции, которые помогут вам в вашем путешествии:

🕵️‍♂️1)Проверка цены - доверьтесь своим судьбоносным инстинктам,
и этот волшебный бот выведет перед вами информацию о текущих лотах на искомый предмет.
Остерегайтесь, информация может быть крайне "сырая", но не откажите себе в этом очаровании.

🔮2)Ожидание предмета — это уже настоящий магический ритуал! 
Позвольте этому боту ощутить ваши мечты и добавить желаемый предмет в ожидание.
Ведь только в таинственный Хэллоуинский вечер🕛, когда звезды выстраиваются в особенный порядок,
бот уведомит вас о появлении этого предмета на аукционе. 

🕯️3)История цен - волшебная функция, создающая для вас особенный гримуар. Этот бот составит свечевой график с вашими
особыми таймингами и создаст возможность потыкать каждую свечу и её тень. Excel файл станет страницей из забытой сказки,
где вы сами будите формировать и делать свои таинственные решения.

В этом странном волшебстве Хэллоуина, оставайтесь бдительными и готовьте свои нервы,
ведь Чернобыльская Зона скрывает множество опасностей и загадочных существ. 
Желаем вам незабываемых приключений и сталкерской удачи в этом мистическом путешествии!
""", reply_markup=main_kb)


def register_client_handlers_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_callback_query_handler(cmd_server_selection, text=['Russian'])
    dp.register_callback_query_handler(cmd_main, text=['RU'])

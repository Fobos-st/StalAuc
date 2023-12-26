from aiogram import Dispatcher, types
from create_bot import bot
from handlers.keyboard import main_kb
import database.dbsql
import random


async def ruffle_winner() -> str:
    all_members = await database.dbsql.print_all_raffle_users()
    num = random.randint(0, len(all_members) - 1)
    await bot.send_message(all_members[num][0], winner_text)
    await bot.send_message(1254191582, f'ID:{all_members[num][0]} \nTelegram name:{all_members[num][1]} \nGame nickname:{all_members[num][2]}')
    return all_members[num][1]


async def ruffle_winner_test() -> str:
    all_members = await database.dbsql.print_all_raffle_users()
    num = random.randint(0, len(all_members) - 1)
    await bot.send_message(1254191582, f'ID:{all_members[num][0]} \nTelegram name:{all_members[num][1]} \nGame nickname:{all_members[num][2]}')
    return all_members[num][1]


winner_text = """
Привет! Поздравляю тебя с выйграшем БП!
В ближайшие время постараюсь кинуть его тебе на куру, надеюсь ник введёный тобой был верным.
Если есть вопросы то пиши мне через -> /ticket
"""


result_raffle_text = ("""
❄️Уважаемые путешественники Зоны!❄️

Давайте подведём итоги розыгрыша.
В участие приняло {} и среди них лишь 1 победитель.
И им стал "{}"
Подарок уже отправляется победителю 

Всем большое спасибо за участие,
С Уважением разработчик StalAcution!
""")


# @dp.message_handler(commands=['update'])
async def send_result_ruffle_all_users(message: types.Message):
    if message.from_user.id == 1254191582:
        data = database.dbsql.get_all_id_users()
        blocked_user = 0
        winner = await ruffle_winner()
        for user in data:
            try:
                await bot.send_message(user[0], result_raffle_text.format(await database.dbsql.get_count_user_raffle(),
                                                                          winner), reply_markup=main_kb)
            except Exception as lox:
                print(lox)
                blocked_user += 1
        await message.answer(f"Пользователи получили сообщение, из них не получили {blocked_user}")


async def send_result_ruffle_for_me(message: types.Message):
    if message.from_user.id == 1254191582:
        await bot.send_message(1254191582, result_raffle_text.format(await database.dbsql.get_count_user_raffle(),
                                                                     await ruffle_winner_test()), reply_markup=main_kb)


def register_admin_handler_result_raffle(dp: Dispatcher):
    dp.register_message_handler(send_result_ruffle_all_users, commands=['result_raffle'])
    dp.register_message_handler(send_result_ruffle_for_me, commands=['for_me'])

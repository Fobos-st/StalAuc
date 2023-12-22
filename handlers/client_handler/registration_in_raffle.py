from aiogram import Dispatcher, types
from database.dbsql import reg_in_sweepstakes, check_user_in_db_raffle
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class RegRaffle(StatesGroup):
    user_game_nickname = State()


async def send_reg_message(message: types.Message):
    result = await check_user_in_db_raffle(message.from_user.id)
    if result:
        await RegRaffle.user_game_nickname.set()
        await message.answer('Введите ваш игровой ник без ошибок(Ru сервера):')
    else:
        await message.answer(await reg_in_sweepstakes(message.from_user.id, message.from_user.full_name))


async def create_reg_raffle(message: types.Message, state: FSMContext):
    await message.answer(await reg_in_sweepstakes(message.from_user.id, message.from_user.full_name, message.text))
    await state.finish()


def register_client_handlers_registration_in_raffle(dp: Dispatcher):
    dp.register_message_handler(send_reg_message, content_types=['text'], text="Участвовать в розыгрыше")
    dp.register_message_handler(create_reg_raffle, content_types=['text'], state=RegRaffle.user_game_nickname)


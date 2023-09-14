from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot


class CreateTicket(StatesGroup):
    text = State()


@dp.message_handler(commands=['ticket'])
async def cmd_ticket(message: types.Message):
    await CreateTicket.text.set()
    await message.answer("Напиши отзыв об боте либо-же свою жалобу")


@dp.message_handler(state=CreateTicket.text)
async def send_ticket_admin(message: types.Message, state: FSMContext):
    await message.answer("Отлично, разработчик обязательно получит ваше столь важное сообщение")
    await state.finish()
    await bot.send_message(1254191582, f"""Собщение от {message.from_user.first_name},
{message.text}
""")

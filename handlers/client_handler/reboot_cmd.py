from aiogram import types, Dispatcher
from ..keyboard import main_kb


# @dp.message_handler(commands=['reboot'])
async def cmd_reboot_main_kb(message: types.Message):
    await message.answer("Клавиатура добавлена. \nДанная команда возвращает клавиатуру в случае её исчезновения так как иногда WEB версия ТГ работает некорректно и клавиатура пропадает", reply_markup=main_kb)


def register_client_handler_update(dp: Dispatcher):
    dp.register_message_handler(cmd_reboot_main_kb, commands=['reboot'])

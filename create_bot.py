from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot('YOUR TOKEN')
dp = Dispatcher(bot, storage=storage)

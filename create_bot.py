import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from background_proces import check_item
from config import BOT_TOKEN


async def on_bot_start_up(dispatcher: Dispatcher) -> None:
    """List of actions which should be done before bot start"""
    asyncio.create_task(check_item())  # creates background task


def create_bot_factory() -> None:
    """Создание и запуск бота"""
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)


storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

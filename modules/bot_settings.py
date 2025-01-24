import aiogram as aio
from aiogram.fsm.storage.memory import *

bot = aio.Bot()  # Telegram bot API token
dp = aio.Dispatcher(storage=MemoryStorage())

warning_message_chat_id = []
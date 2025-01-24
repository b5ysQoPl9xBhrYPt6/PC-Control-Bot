import aiogram as aio
from aiogram.fsm.storage.memory import *

bot = aio.Bot('7735775616:AAGfu3M0m4hznc6lvlHgWteYO_lDmSqj1hI')  # Telegram bot API token
dp = aio.Dispatcher(storage=MemoryStorage())

warning_message_chat_id = [5534294941]

temp_dir_name = 'temp_direction'
processes_object_name = 'Locked'
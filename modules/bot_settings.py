import aiogram as aio
from aiogram.fsm.storage.memory import *

bot = aio.Bot()  # Telegram bot API token
dp = aio.Dispatcher(storage=MemoryStorage())

warning_message_chat_id = []

temp_dir_name = 'temp_direction'
processes_object_name = 'Locked'

save_tasks = [
    'svchost.exe', 'winlogon.exe', 'wininit.exe', 'smss.exe', 
    'services.exe', 'csrss.exe', 'System Idle Process', 'System',
    'Registry', 'sihost.exe', 'Lsalso.exe', 'lsass.exe'
    ]

file_system_menu_memory = {}

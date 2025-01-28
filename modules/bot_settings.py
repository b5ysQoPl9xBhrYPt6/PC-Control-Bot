import aiogram as aio
from aiogram.fsm.storage.memory import *
from . import json
import os, sys

json_file_name = 'info.json'  # Create a json file next to main.py with the following data: {"Token": "Your Telegram bot API token", "WarningMessageChatIdList": [000000000, 000000000, ...]}
json_data = json.read(os.path.abspath(os.path.join(sys.argv[0], os.pardir, json_file_name)))

bot = aio.Bot(json_data['Token'])
dp = aio.Dispatcher(storage=MemoryStorage())

warning_message_chat_id = json_data['WarningMessageChatIdList']

temp_dir_name = 'temp_directory'
processes_object_name = 'Locked'

save_tasks = [
    'svchost.exe', 'winlogon.exe', 'wininit.exe', 'smss.exe', 
    'services.exe', 'csrss.exe', 'System Idle Process', 'System',
    'Registry', 'sihost.exe', 'Lsalso.exe', 'lsass.exe'
    ]

file_system_menu_memory = {}

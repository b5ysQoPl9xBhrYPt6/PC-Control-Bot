from .bot_settings import bot, dp, processes_object_name, save_tasks
from aiogram.types import *
from aiogram.fsm.context import *
from aiogram.fsm.state import *
from aiogram import exceptions
from . import actions
import os

class Memory(StatesGroup):  # Memory for waiting
    WAITING_FOR_ACTION = State()
    WAITING_FOR_MESSAGE = State()
    WAITING_FOR_PROCESS = State()
    WAITING_FOR_ADD_PROCESS_NAME = State()
    WAITING_FOR_REMOVE_PROCESS_NAME = State()
    WAITING_FOR_COPY_FILE = State()

async def explorer(message: Message, state: FSMContext, path: str):
    button_list = []
    dir_list = []
    file_list = []

    try:
        for item in actions.dir_list(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                button = KeyboardButton(text=f'Перейти в {str(item)} <{item_path}>')
                dir_list.append([button])
            elif os.path.isfile(item_path):
                button_get = KeyboardButton(text=f'Скачать {str(item)} <{item_path}>')
                file_list.append([button_get])

        button_exit = KeyboardButton(text='Выйти')
        button_back = KeyboardButton(text=f'Назад <{os.path.abspath(os.path.join(path, os.pardir))}>')

        button_list.append([button_back, button_exit])

        for dir in dir_list:
            button_list.append(dir)
        for file in file_list:
            button_list.append(file)
        
        kb = ReplyKeyboardMarkup(keyboard=button_list)
        await message.answer(f'Текущий путь:\n{path}', reply_markup=kb)
    except exceptions.TelegramBadRequest as bad_request:
        try:
            button_list.clear()
            dir_list.clear()
            file_list.clear()
            for item in actions.dir_list(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    button = KeyboardButton(text=f'Перейти в {str(item)} <{item_path}>')
                    dir_list.append([button])

            button_exit = KeyboardButton(text='Выйти')
            button_back = KeyboardButton(text=f'Назад <{os.path.abspath(os.path.join(path, os.pardir))}>')

            button_list.append([button_back, button_exit])

            for dir in dir_list:
                button_list.append(dir)
            
            kb = ReplyKeyboardMarkup(keyboard=button_list)
            await message.answer(f'В папке слишком много файлов. В ней будут отображаться только другие папки, но вы все ещё можете скачать файлы из неё, если знаете точное название файла, написав "Скачать file_name.txt".\nПодробности: {bad_request}', reply_markup=kb)
            await message.answer(f'Текущий путь:\n{path}')
        except exceptions.TelegramBadRequest as bad_request:
            await message.answer(f'Невозможно перейти в папку, так-как в ней слишком много содержимого. Возможно в будущем, это будет исправлено.\nПодробности: {bad_request}')
    await state.set_state(Memory.WAITING_FOR_COPY_FILE)

async def main_message(message: Message, state: FSMContext):
    action_send_message = KeyboardButton(text='Отправить сообщение')
    action_send_screenshot = KeyboardButton(text='Снимок экрана')
    action_lock_cursor = KeyboardButton(text='Заблокировать или разблокировать курсор')
    action_lock_application = KeyboardButton(text='Заблокировать или разблокировать открытие процессов')
    action_get_file = KeyboardButton(text='Получить файл')
    kb = ReplyKeyboardMarkup(keyboard=[
        [action_send_message, action_send_screenshot],
        [action_lock_cursor],
        [action_lock_application],
        [action_get_file]
        ])

    await message.answer('Выберите доступное действие для взаимодействия с ПК.', reply_markup=kb)
    await state.set_state(Memory.WAITING_FOR_ACTION)

async def locked_processes_message(message: Message, state: FSMContext):
    button_add_task_data = KeyboardButton(text='Добавить задачу в список заблокированных')
    button_remove_task_data = KeyboardButton(text='Убрать задачу из списка заблокированных')
    button_set_task_data = KeyboardButton(text='Пересоздать список заблокированных задач')
    button_lock_task = KeyboardButton(text='Заблокировать или разблокировать открытие процессов')
    button_exit = KeyboardButton(text='Выйти')
    button_tasks = KeyboardButton(text='Список')
    lock_processes_menu = ReplyKeyboardMarkup(keyboard=[
        [button_add_task_data],
        [button_remove_task_data],
        [button_set_task_data],
        [button_lock_task],
        [button_exit, button_tasks]
        ])
    
    await message.answer('Выберите доступное действие для блокировки открытия процессов.\nПри запуске бота, блокировка процессов автоматически включается, но вы можете её отключить или изменить список заблокированных процессов.', reply_markup=lock_processes_menu)
    await state.set_state(Memory.WAITING_FOR_PROCESS)

@dp.message(Memory.WAITING_FOR_MESSAGE)
async def send_message(message: Message, state: FSMContext):
    if not message.text == None:
        actions.thread_message(message.text)
        await message.answer('Ваше сообщение было отправлено.')
        await main_message(message, state)
    else:
        await message.answer('В сообщении можно отправлять только текст. Повторите попытку:')

@dp.message(Memory.WAITING_FOR_ADD_PROCESS_NAME)
async def add_task(message: Message, state: FSMContext):
    if not message.text in save_tasks:
        if '.exe' in message.text:
            if actions.add_locked_tasks_data(message.text):
                await message.answer('Процесс добавлен в список.')
                await message.answer(f'Новый список заблокированных процессов:\n{actions.return_locked_processes()[str(processes_object_name)]}')
            else:
                await message.answer('Не удалось внести изменения в список.')
        else:
            await message.answer('Похоже, вы указали название процесса неправильно, попробуйте ещё. Название обязательно должно быть исполняемым файлом с припиской ".exe" в конце. Например Notepad.exe')
    else:
        await message.answer(f'Невозможно добавить процесс "{message.text}" в список заблокированных процессов, так-как этот процесс важен для работы системы.')
    await locked_processes_message(message, state)

@dp.message(Memory.WAITING_FOR_REMOVE_PROCESS_NAME)
async def remove_task(message: Message, state: FSMContext):
    if not message.text == 'Отмена':
        if message.text in actions.return_locked_processes()[str(processes_object_name)]:
            if actions.remove_locked_tasks_data(str(message.text)):
                await message.answer(f'Процесс "{message.text}" удален из списка заблокированных.')
            else:
                await message.answer(f'Не удалось удалить "{message.text}" из списка.')
        else:
            await message.answer(f'Не удалось найти "{message.text}" в списке.')
    else:
        await message.answer('Действие отменено.')
    await message.answer(f'Список заблокированных процессов:\n{actions.return_locked_processes()[str(processes_object_name)]}')
    await locked_processes_message(message, state)

from .bot_settings import bot, dp, processes_object_name, save_tasks, file_system_menu_memory
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
    WAITING_FOR_RUN_FILE = State()
    WAITING_FOR_RUN_FILE_MENU = State()

async def main_message(message: Message, state: FSMContext):
    action_send_message = KeyboardButton(text='Отправить сообщение')
    action_send_screenshot = KeyboardButton(text='Снимок экрана')
    action_lock_cursor = KeyboardButton(text='Заблокировать или разблокировать курсор')
    action_lock_application = KeyboardButton(text='Заблокировать или разблокировать открытие процессов')
    action_get_file = KeyboardButton(text='Получить файл')
    action_run_file = KeyboardButton(text='Запустить файл')
    kb = ReplyKeyboardMarkup(keyboard=[
        [action_send_message, action_send_screenshot],
        [action_lock_cursor],
        [action_lock_application],
        [action_get_file, action_run_file]
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

async def choose(message: Message, state: FSMContext, set_state: Memory, buttons: list[list[KeyboardButton]], answer: str):
    kb = ReplyKeyboardMarkup(keyboard=buttons)
    await message.answer(answer, reply_markup=kb)
    await state.set_state(set_state)

async def explorer(message: Message, state: FSMContext, path: str, set_state: Memory, page_index: int, mode: int = 0):
    await message.answer('Загрузка директории...')
    item_list = []
    button_list = []
    dir_list = []
    file_list = []
    file_system_menu_memory[str(message.from_user.id)] = {"Path": path, "Page": page_index}

    if mode == 0:
        text = 'Скачать'
    else:
        text = 'Запустить'

    dir_info = actions.dir_list(path)
    if dir_info[0]:
        for item in actions.dir_list(path)[-1]:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                button_dir = KeyboardButton(text=f'Перейти в {item}')
                dir_list.append([button_dir])
            elif os.path.isfile(item_path):
                button_file = KeyboardButton(text=f'{text} {item}')
                file_list.append([button_file])
    else:
        await message.answer(f'Произошла ошибка. Подробности:\n{dir_info[-1]}')

    button_exit = KeyboardButton(text='Выйти')
    button_back = KeyboardButton(text='Назад')
    button_previous_page = KeyboardButton(text='Предыдущая страница')
    button_next_page = KeyboardButton(text='Следующая страница')

    item_count = 20
    for dir in dir_list:
        item_list.append(dir)
    for file in file_list:
        item_list.append(file)
    pages = [[x for x in item_list[i:i+item_count]] for i in range(0, len(item_list), item_count)]

    button_list.insert(0, [button_back, button_exit])

    try:
        for button in pages[page_index]:
            button_list.append(button)
        button_list.append([button_previous_page, button_next_page])
    except IndexError:
        file_system_menu_memory[str(message.from_user.id)]["Page"] = 0
        try:
            for button in pages[0]:
                button_list.append(button)
            button_list.append([button_previous_page, button_next_page])
        except IndexError:
            await message.answer(f'Не удалось отобразить директорию "{path}"')

    if file_system_menu_memory[str(message.from_user.id)]["Page"] < 0:
        file_system_menu_memory[str(message.from_user.id)]["Page"] = len(pages) - 1

    try:
        kb = ReplyKeyboardMarkup(keyboard=button_list)
        await message.answer(f'Страница: {file_system_menu_memory[str(message.from_user.id)]["Page"]}\nТекущий путь:\n{path}', reply_markup=kb)
    except exceptions.TelegramBadRequest:
        for file in file_list:
            item_list.remove(file)

        try:
            kb = ReplyKeyboardMarkup(keyboard=button_list)
            await message.answer(f'Не удалось отобразить файлы, так как в текущей директории слишком много содержимого, будут отображаться только папки. Вы все еще можете скачать файлы из этой директории, написав "Скачать file_name.txt", если знаете точное имя файла.', reply_markup=kb)
            await message.answer(f'Страница: {file_system_menu_memory[str(message.from_user.id)]["Page"]}\nТекущий путь:\n{path}')
        except exceptions.TelegramBadRequest:
            for dir in dir_list:
                item_list.remove(dir)
            
            kb = ReplyKeyboardMarkup(keyboard=button_list)
            await message.answer(f'Не удалось отобразить содержимое директории, так как в ней слишком много файлов и папок. Вы все еще можете скачать файлы из этой директории или перейти в другую, если знаете точное имя файла или папки, написав "Скачать file_name.txt" или "Перейти в directory_name".')
            await message.answer(f'Страница: {file_system_menu_memory[str(message.from_user.id)]["Page"]}\nТекущий путь:\n{path}', reply_markup=kb)
    print(file_system_menu_memory)

    await state.set_state(set_state)

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

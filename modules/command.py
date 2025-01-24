from .bot_settings import bot, dp, processes_object_name
from aiogram.types import *
from aiogram.fsm.context import *
from aiogram.fsm.state import *
from . import actions

class Memory(StatesGroup):  # Memory for waiting
    WAITING_FOR_ACTION = State()
    WAITING_FOR_MESSAGE = State()
    WAITING_FOR_PROCESS = State()

async def main_message(message: Message, state: FSMContext):
    action_send_message = KeyboardButton(text='Отправить сообщение')
    action_send_screenshot = KeyboardButton(text='Снимок экрана')
    action_lock_cursor = KeyboardButton(text='Заблокировать или разблокировать курсор')
    action_lock_application = KeyboardButton(text='Заблокировать или разблокировать открытие процессов')
    kb = ReplyKeyboardMarkup(keyboard=[
        [action_send_message, action_send_screenshot],
        [action_lock_cursor],
        [action_lock_application]
        ])

    await message.answer('Выберите доступное действие для взаимодействия с ПК.', reply_markup=kb)
    await state.set_state(Memory.WAITING_FOR_ACTION)

async def locked_processes_message(message: Message, state: FSMContext):
    button_add_task_data = KeyboardButton(text='Добавить задачу в список заблокированных')
    button_remove_task_data = KeyboardButton(text='Убрать задачу из списка заблокированных')
    button_set_task_data = KeyboardButton(text='Переписать список заблокированных задач')
    button_lock_task = KeyboardButton(text='Заблокировать или разблокировать открытие процессов')
    button_exit = KeyboardButton(text='Выйти')
    lock_processes_menu = ReplyKeyboardMarkup(keyboard=[
        [button_add_task_data],
        [button_remove_task_data],
        [button_set_task_data],
        [button_lock_task],
        [button_exit]
        ])
    
    await message.answer('Выберите доступное действие для блокировки открытия процессов.\nПри запуске бота, блокировка процессов автоматически включается, но вы можете её отключить или изменить список заблокированных процессов.', reply_markup=lock_processes_menu)
    await state.set_state(Memory.WAITING_FOR_PROCESS)


@dp.message(Memory.WAITING_FOR_PROCESS)
async def lock_processes(message: Message, state: FSMContext):
    if message.text == 'Выйти':
        await main_message(message, state)
    elif message.text == 'Заблокировать или разблокировать открытие процессов':
        await message.answer(f'Список заблокированных процессов:\n{actions.return_locked_processes()[str(processes_object_name)]}')
        if actions.thread_lock_tasks():
            await message.answer('Открытие процессов из списка заблокировано. Нажмите "Заблокировать или разблокировать открытие процессов" еще раз, чтобы его разблокировать.')
        else:
            await message.answer('Открытие процессов из списка разблокировано.')
    else:
        await message.answer('Неизвестная команда. Повторите попытку.')

@dp.message(Memory.WAITING_FOR_MESSAGE)
async def send_message(message: Message, state: FSMContext):
    if not message.text == None:
        actions.thread_message(message.text)
        await message.answer('Ваше сообщение было отправлено.')
        await main_message(message, state)
    else:
        await message.answer('В сообщении можно отправлять только текст. Повторите попытку:')

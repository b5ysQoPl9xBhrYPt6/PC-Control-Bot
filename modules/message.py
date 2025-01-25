from .command import *
from aiogram import exceptions
from .bot_settings import processes_object_name

@dp.message(Memory.WAITING_FOR_ACTION)
async def select_action(message: Message, state: FSMContext):
    if message.text == 'Отправить сообщение':
        await message.answer('Введите сообщение для отправки:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Memory.WAITING_FOR_MESSAGE)
    elif message.text == 'Снимок экрана':
        await message.answer('Снимок экрана загружается...')
        try:
            await message.answer_photo(photo=FSInputFile(actions.get_screenshot()), caption='Получен снимок экрана.')
        except exceptions.TelegramBadRequest:
            await message.answer('Не удалось получить снимок экрана.')
    elif message.text == 'Заблокировать или разблокировать курсор':
        if actions.thread_lock_cursor():
            await message.answer('Передвижение курсора заблокировано. Нажмите "Заблокировать или разблокировать курсор" еще раз, чтобы его разблокировать.')
        else:
            await message.answer('Передвижение курсора разблокировано.')
    elif message.text == 'Заблокировать или разблокировать открытие процессов':
        await locked_processes_message(message, state)
    else:
        await message.answer('Неизвестная команда. Повторите попытку.')

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
    elif message.text == 'Пересоздать список заблокированных задач':
        if actions.clear_locked_tasks_data():
            await message.answer(f'Список очищен. Новый список заблокированных процессов:\n{actions.return_locked_processes()[str(processes_object_name)]}')
        else:
            await message.answer('Не удалось очистить список.')
    elif message.text == 'Список':
        await message.answer(f'Список заблокированных процессов:\n{actions.return_locked_processes()[str(processes_object_name)]}')
    elif message.text == 'Добавить задачу в список заблокированных':
        await message.answer('Введите название процесса (например: Taskmgr.exe) для внесения в список заблокированных:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Memory.WAITING_FOR_ADD_PROCESS_NAME)
    elif message.text == 'Убрать задачу из списка заблокированных':
        if not len(actions.return_locked_processes()[str(processes_object_name)]) == 0:
            button_list = []
            for item in actions.return_locked_processes()[str(processes_object_name)]:
                button = KeyboardButton(text=str(item))
                button_list.append([button])
            button_cancel = KeyboardButton(text='Отмена')
            button_list.append([button_cancel])
            kb = ReplyKeyboardMarkup(keyboard=button_list)
            await message.answer('Введите название процесса, который находится в списке:', reply_markup=kb)
            await state.set_state(Memory.WAITING_FOR_REMOVE_PROCESS_NAME)
        else:
            await message.answer('Список пустой.')
    else:
        await message.answer('Неизвестная команда. Повторите попытку.')

@dp.message()
async def message_handler(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text  # User message

    if msg == '/start':
        await main_message(message, state)

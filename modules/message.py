from .command import *
from aiogram import exceptions
from .bot_settings import processes_object_name, temp_dir_name

temp_path = os.path.join(os.getenv('TEMP'), temp_dir_name)
max_file_size = 32

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
    elif message.text == 'Получить файл':
        await message.answer(f'Данная возможность сильно ограничена, так как возможно скачать только файл с максимальным размером {max_file_size} МБ.')
        await explorer(message, state, 'C:\\', Memory.WAITING_FOR_COPY_FILE, 0)
    elif message.text == 'Запустить файл':
        button_temp = KeyboardButton(text='Загрузки')
        button_default = KeyboardButton(text='C:\\')
        await choose(message, state, Memory.WAITING_FOR_RUN_FILE_MENU, [[button_temp], [button_default]], 'Выберите директорию:')
    else:
        await message.answer('Неизвестная команда. Повторите попытку.')

@dp.message(Memory.WAITING_FOR_RUN_FILE_MENU)
async def copy_file_choose_menu(message: Message, state: FSMContext):
    if message.text == 'Загрузки':
        await explorer(message, state, os.path.abspath(os.path.join(os.getenv('TEMP'), temp_dir_name)), Memory.WAITING_FOR_RUN_FILE, 1)
    else:
        await explorer(message, state, message.text, Memory.WAITING_FOR_RUN_FILE, 1)

@dp.message(Memory.WAITING_FOR_RUN_FILE)
async def run_file(message: Message, state: FSMContext):
    if message.text == 'Выйти':
        del file_system_menu_memory[str(message.from_user.id)]
        await main_message(message, state)
    elif 'Перейти в ' in message.text:
        folder = message.text.split('Перейти в ')[-1]
        await explorer(message, state, os.path.join(file_system_menu_memory[str(message.from_user.id)], folder), Memory.WAITING_FOR_RUN_FILE, 1)
    elif message.text == 'Назад':
        await explorer(message, state, os.path.abspath(os.path.join(file_system_menu_memory[str(message.from_user.id)], os.pardir)), Memory.WAITING_FOR_RUN_FILE, 1)
    elif 'Запустить ' in message.text:
        file = message.text.split('Запустить ')[-1]
        await message.answer(f'Файл: {file}\nПопытка запуска...')
        result = actions.run_file(os.path.join(file_system_menu_memory[str(message.from_user.id)], file))
        if result[0]:
            await message.answer(f'Файл "{file}" успешно запущен.')
        else:
            await message.answer(f'Не удалось запустить файл "{file}".\nПодробности: {result[-1]}')

@dp.message(Memory.WAITING_FOR_COPY_FILE)
async def copy_file(message: Message, state: FSMContext):
    if message.text == 'Выйти':
        del file_system_menu_memory[str(message.from_user.id)]
        await main_message(message, state)
    elif 'Перейти в ' in message.text:
        folder = message.text.split('Перейти в ')[-1]
        await explorer(message, state, os.path.join(file_system_menu_memory[str(message.from_user.id)], folder), Memory.WAITING_FOR_COPY_FILE)
    elif message.text == 'Назад':
        await explorer(message, state, os.path.abspath(os.path.join(file_system_menu_memory[str(message.from_user.id)], os.pardir)), Memory.WAITING_FOR_COPY_FILE)
    elif 'Скачать ' in message.text:
        file = message.text.split('Скачать ')[-1]
        file_path = os.path.abspath(os.path.join(file_system_menu_memory[str(message.from_user.id)], file))
        file_info = actions.check_size(file_path, 1024 * 1024 * max_file_size)
        file_size = actions.get_size(file_path)
        if file_size[0]:
            if file_size[-1] > max_file_size - max_file_size // 2:
                await message.answer(f'Файл: {file}\nРазмер: {file_size[-1] if file_size[0] else None} МБ\nФайл имеет большой размер, скачивание может продлиться 1 минуту, иначе действие будет отменено.\nПопытка скачивания...')
            else:
                await message.answer(f'Файл: {file}\nРазмер: {file_size[-1] if file_size[0] else None} МБ\nПопытка скачивания...')
        else:
            await message.answer(f'Файл: {file}\nРазмер: {file_size[-1] if file_size[0] else None} МБ\nПопытка скачивания...')
        try:
            if file_info[0]:
                await message.answer_document(FSInputFile(file_path), caption=f'Получен файл "{file}" из "{file_system_menu_memory[str(message.from_user.id)]}".')
            else:
                if file_info[-1]:
                    await message.answer(f'Произошла ошибка. Подробности:\n{file_info[-1]}')
                else:
                    if file_size[0]:
                        await message.answer(f'Невозможно скачать файл, так как его размер превышает {max_file_size} МБ.\nРазмер файла: {file_size[-1]} МБ.')
                    else:
                        await message.answer(f'Невозможно скачать файл, так как его размер превышает {max_file_size} МБ.\nРазмер файла неизвестен.')
        except exceptions.TelegramNetworkError as network:
            await message.answer(f'Невозможно скачать файл {file}. Возможно у вас нету доступа к нему, файл занят другим процессом или время скачивания превышено.\nПодробности: {network}')
        except exceptions.TelegramBadRequest:
            await message.answer('Файл пуст.')
    else:
        await message.answer('Неизвестная команда, повторите попытку.\nПодсказка: если вы не используете клавиатуру с выбором, команды нужно писать обязательно с большой буквы.')

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

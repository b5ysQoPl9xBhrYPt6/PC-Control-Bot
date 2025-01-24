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

@dp.message()
async def message_handler(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text  # User message

    if msg == '/start':
        await main_message(message, state)

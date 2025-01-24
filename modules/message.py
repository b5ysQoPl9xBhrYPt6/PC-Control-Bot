from .command import *

@dp.message(Memory.WAITING_FOR_ACTION)
async def select_action(message: Message, state: FSMContext):
    if message.text == 'Отправить сообщение':
        await message.answer('Введите сообщение для отправки:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Memory.WAITING_FOR_MESSAGE)
    elif message.text == 'Снимок экрана':
        await message.answer('Снимок экрана загружается...')
        await message.answer_photo(photo=FSInputFile(actions.get_screenshot()), caption='Получен снимок экрана.')
    elif message.text == 'Заблокировать или разблокировать курсор':
        if actions.thread_lock_cursor():
            await message.answer('Курсор заблокирован. Нажмите "Заблокировать или разблокировать курсор" еще раз, чтобы его разблокировать.')
        else:
            await message.answer('Курсор разблокирован. Нажмите "Заблокировать или разблокировать курсор" еще раз, чтобы его заблокировать.')

@dp.message()
async def message_handler(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text  # User message

    if msg == '/start':
        await main_message(message, state)

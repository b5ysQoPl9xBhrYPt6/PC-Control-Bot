from .bot_settings import bot, dp
from aiogram.types import *
from aiogram.fsm.context import *
from aiogram.fsm.state import *
from . import actions

class Memory(StatesGroup):  # Memory for waiting
    WAITING_FOR_ACTION = State()

    WAITING_FOR_MESSAGE = State()

async def main_message(message: Message, state: FSMContext):
    action_send_message = KeyboardButton(text='Отправить сообщение')
    action_send_screenshot = KeyboardButton(text='Получить снимок экрана')
    kb = ReplyKeyboardMarkup(keyboard=[
        [action_send_message, action_send_screenshot]
        ])

    await message.answer('Выберите доступное действие для взаимодействия с ПК.', reply_markup=kb)
    await state.set_state(Memory.WAITING_FOR_ACTION)

@dp.message(Memory.WAITING_FOR_MESSAGE)
async def send_message(message: Message, state: FSMContext):
    if not message.text == None:
        actions.thread_message(message.text)
        await message.answer('Ваше сообщение было отправлено.')
        await main_message(message, state)
    else:
        await message.answer('В сообщение можно отправлять только текст. Повторите попытку:')

@dp.message(Memory.WAITING_FOR_ACTION)
async def select_action(message: Message, state: FSMContext):
    if message.text == 'Отправить сообщение':
        await message.answer('Введите сообщение для отправки:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Memory.WAITING_FOR_MESSAGE)
    elif message.text == 'Получить снимок экрана':
        await message.answer('Снимок экрана загружается...')
        await message.answer_photo(photo=FSInputFile(actions.get_screenshot()), caption='Получен снимок экрана.')

@dp.message()
async def message_handler(message: Message, state: FSMContext):
    await state.clear()
    msg = message.text  # User message
    # print(message)
    if msg == '/start':
        await main_message(message, state)
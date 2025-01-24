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
    action_send_screenshot = KeyboardButton(text='Снимок экрана')
    action_lock_cursor = KeyboardButton(text='Заблокировать или разблокировать курсор')
    kb = ReplyKeyboardMarkup(keyboard=[
        [action_send_message, action_send_screenshot],
        [action_lock_cursor]
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

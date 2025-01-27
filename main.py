# It is recommended to run as administrator.

from sys import exit
import aiogram.exceptions
import modules
import modules.actions as actions
from aiogram.types import FSInputFile, ReplyKeyboardRemove
import aiogram
import logging
import asyncio

logging.basicConfig(level=logging.INFO)  # Logging info

async def close():
    await modules.bot.session.close()
    exit()

async def main():
    actions.get_screenshot()
    for id in modules.warning_message_chat_id:
        try:
            await modules.bot.send_photo(chat_id=id, photo=FSInputFile(actions.get_screenshot_path()), caption='Компьютер активный. Напишите /start, чтобы начать управление.', reply_markup=ReplyKeyboardRemove())
        except aiogram.exceptions.TelegramBadRequest:
            print(f'Chat {id} not founded.')
        except aiogram.exceptions.TelegramServerError:
            await modules.bot.send_message(chat_id=id, text='Компьютер активный. Напишите /start, чтобы начать управление.')

    await modules.bot.delete_webhook(drop_pending_updates=True)
    await modules.dp.start_polling(modules.bot)

if __name__ == '__main__':
    actions.thread_lock_tasks()
    try:
        asyncio.run(main())  # Start bot
    except KeyboardInterrupt:
        asyncio.run(close())

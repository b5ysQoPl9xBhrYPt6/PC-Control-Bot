from sys import exit
import modules
import aiogram
import logging
import asyncio

logging.basicConfig(level=logging.INFO)  # Logging info

async def main():
    await modules.bot.delete_webhook(drop_pending_updates=True)
    await modules.dp.start_polling(modules.bot)
    # await modules.bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())  # Start bot
    except KeyboardInterrupt:
        exit()

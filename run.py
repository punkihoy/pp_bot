import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers import router
from bot.write_handler import router_write
from bot.watcher_handlers import router_watch

load_dotenv("config.env")
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_routers(router, router_write, router_watch)
    await bot.send_message(os.getenv("ADMIN_ID"), "bot is starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

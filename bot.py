import asyncio
from aiogram import Bot, Dispatcher
from router import router
from register import dp_1
from admin_router import rt

API_TOKEN = "7241043302:AAF2TjfX3JOqvH8hnTCbVN8_X4RFfXwKAUE"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.include_router(router)
dp.include_router(dp_1)
dp.include_router(rt)

async def main():
    print("👍 Bot ishladi")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
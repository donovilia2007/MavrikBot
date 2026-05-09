import asyncio
import logging

from santa import SantaGame
from start_aiogram import router, bot, dp

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await SantaGame.init_db()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='MavrikBot.log', filemode='a', encoding='utf-8')
    asyncio.run(main())
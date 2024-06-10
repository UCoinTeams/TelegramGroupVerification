import asyncio
import logging
import telebot

from tgbot import start_bot
from schedule import ban_detection
from utils.config_vars import LOG_LEVEL, sql, d_api

telebot.logger.setLevel(LOG_LEVEL.upper())
logging.getLogger().setLevel(LOG_LEVEL.upper())
logging.basicConfig(
    format="[%(levelname)s]%(asctime)s: %(message)s",
    handlers=[
        logging.FileHandler("data/run.log", encoding="UTF-8"),
        logging.StreamHandler(),
    ],
)


async def main():
    tasks = [
        asyncio.create_task(start_bot()),
        asyncio.create_task(ban_detection()),
    ]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("任务已取消")


if __name__ == "__main__":
    sql.create_user_db()
    sql.admin_log_db()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("收到退出信号，取消任务...")
        sql.close()
        d_api.close()
        for task in asyncio.all_tasks():
            task.cancel()
        asyncio.get_event_loop().stop()

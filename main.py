import asyncio
import logging
import telebot

from tgbot import start_bot
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

if __name__ == '__main__':
    sql.create_user_db()
    sql.admin_log_db()
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        loop.close()
        sql.close()
        d_api.close()
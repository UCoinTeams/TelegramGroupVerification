from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
)

from .start import send_start

from utils.config_vars import config

bot = AsyncTeleBot(config["TG"]["BOT_TOKEN"], parse_mode="MarkdownV2")


def bot_register():
    bot.register_message_handler(send_start, commands=["start"], pass_bot=True)


async def set_bot_command():
    """设置Bot命令"""
    await bot.delete_my_commands()
    try:
        await bot.set_my_commands(
            [
                BotCommand("start", "开始验证绑定"),
            ],
            scope=BotCommandScopeAllPrivateChats(),
            language_code="zh",
        )
        await bot.set_my_commands(
            [
                BotCommand("start", "認証を開始する"),
            ],
            scope=BotCommandScopeAllPrivateChats(),
            language_code="ja",
        )
        await bot.set_my_commands(
            [
                BotCommand("start", "Start verification"),
            ],
            scope=BotCommandScopeAllPrivateChats(),
            language_code="en",
        )
        return
    except Exception:
        pass


async def start_bot():
    bot_register()
    await set_bot_command()
    await bot.polling(non_stop=True)

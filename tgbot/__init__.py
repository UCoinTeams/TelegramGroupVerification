from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import (
    BotCommand,
    Message,
    BotCommandScopeAllPrivateChats,
)

from .start import send_start
from .callback_pages import get_u2_id

from utils.config_vars import config, redis

bot = AsyncTeleBot(config["TG"]["BOT_TOKEN"], parse_mode="MarkdownV2")


def bot_register():
    bot.add_custom_filter(IsRreply())
    # commands
    bot.register_message_handler(
        send_start, commands=["start"], chat_types=["private"], pass_bot=True
    )
    bot.register_message_handler(
        send_reply, chat_types=["private"], is_reply=True, pass_bot=True
    )
    # callback_pages
    bot.register_callback_query_handler(
        get_u2_id, func=lambda c: c.data.startswith("gu2id"), pass_bot=True
    )


async def send_reply(message: Message):
    """检测回复消息"""
    if redis_data := redis.get(f"msg_id:{message.reply_to_message.message_id}"):
        redis_data = redis_data.decode().split("|")
        if redis_data[0] == "to_verify":
            
            return
    else:
        return await bot.send_message(
            message.chat.id,
            "未检测到这条消息的数据，请重新开始。\n\nNo data detected for this message, please start again\\.\n\nこのメッセージのデータが検出されませんでした。\nもう一度やり直してください。",
            reply_to_message_id=message.message_id,
        )


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


class IsRreply(SimpleCustomFilter):
    """判断是否为回复"""

    key = "is_reply"

    @staticmethod
    async def check(message):
        if (
            message.reply_to_message
            and message.reply_to_message.from_user.username
            == config["TG"]["BOT_USERNAME"]
        ):
            return True
        else:
            return False


async def start_bot():
    bot_register()
    await set_bot_command()
    await bot.polling(non_stop=True)

from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)

from utils.message_text import MessageText


async def send_start(message: Message, bot: AsyncTeleBot):
    """发送开始欢迎消息"""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="中文", callback_data="gu2id|cn"),
        InlineKeyboardButton(text="English", callback_data="gu2id|en"),
        InlineKeyboardButton(text="日本語", callback_data="gu2id|ja"),
    )
    await bot.send_message(
        message.chat.id, MessageText().Welcome(), reply_markup=markup
    )

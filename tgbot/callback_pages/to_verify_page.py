from random import sample
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from utils.message_text import MessageText


async def verify_page(message: Message, bot: AsyncTeleBot, language: str):
    """验证页面"""
    vcode = "".join(
        sample("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 5)
    )
    msg = MessageText(language).Ver_code(message.text, message.from_user.id, vcode)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text=msg.markup, callback_data=f"ver|{language}|{message.text}|{vcode}"
        )
    )
    await bot.reply_to(message, msg.text, reply_markup=markup)

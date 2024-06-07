from random import sample
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from utils.message_text import MessageText
from utils.config_vars import d_api, redis, sql, config


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


async def verify(call: CallbackQuery, bot: AsyncTeleBot):
    """验证"""
    _, language, u2_id, vcode = call.data.split(
        "|"
    )  # [0'ver', 1'cn', 2'123456', 3'abcde']
    msg_text = MessageText(language)
    if degree := redis.get(f"ver:{call.from_user.id}"):
        if int(degree) >= 5:
            return await bot.edit_message_text(
                text=msg_text.Ver_error(),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
    redis.incr(f"ver:{call.from_user.id}", 1)
    redis.expire(f"ver:{call.from_user.id}", 60 * 60 * 24)
    if await d_api.verify_u2_captcha(u2_id, vcode):
        await bot.answer_callback_query(call.id, "ok!")
        if sql_data := sql.inqury_user(u2_id=u2_id):
            for i in sql_data:
                await bot.ban_chat_member(
                    chat_id=config["TG"]["GROUP_ID"], user_id=i[1]
                )
                await bot.kick_chat_member(
                    chat_id=config["TG"]["CHANNEL_ID"], user_id=i[1]
                )
        await d_api.bark_notify(
            "群组新人验证通过通知",
            f"➤%20TG_UserID:%20{call.from_user.id}%0a➤%20U2_UserID:%20{u2_id}%0a➤%20语言:%20{language}",
            call.from_user.id,
        )
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(
            text=msg_text.Ver_passed(
                config["TG"]["GROUP_LINK"], config["TG"]["CHANNEL_LINK"]
            ),
            chat_id=call.message.chat.id,
        )
    else:
        await bot.answer_callback_query(call.id, "error!")
        return await bot.send_message(
            text=msg_text.Not_detected(), chat_id=call.message.chat.id
        )

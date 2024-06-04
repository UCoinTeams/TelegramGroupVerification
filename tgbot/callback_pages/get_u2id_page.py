from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ForceReply,
)

from utils.config_vars import sql, redis
from utils.message_text import MessageText


async def get_u2_id(call: CallbackQuery, bot: AsyncTeleBot):
    """获取 U2 ID"""
    language = call.data.split("|")[1]
    text = MessageText(language)
    if sql_data := sql.inqury_user(call.from_user.id):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text=text.Repeat_error_markup(), callback_data="cancel"
            )
        )
        return await bot.edit_message_text(
            text=text.Repeat_error(sql_data[0][0]),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    _text = text.Inquiry_u2id()
    send_msg = await bot.send_message(
        call.message.chat.id,
        _text.text,
        reply_markup=ForceReply(selective=True, input_field_placeholder=_text.markup),
    )
    redis.set(
        f"msg_id:{send_msg.message_id}",
        f"to_verify|{language}",
        ex=60 * 5,
    )
    return


async def test_u2_id(
    message: Message, bot: AsyncTeleBot, data: str, language: str
) -> bool:
    """测试 U2 ID"""
    if not data.isdigit():
        msg = MessageText(language).Inquiry_u2id(error=True)
        markup = ForceReply(selective=True, input_field_placeholder=msg.markup)
        send_msg = await bot.reply_to(message, msg.text, reply_markup=markup)
        redis.set(
            f"msg_id:{send_msg.message_id}",
            f"to_verify|{language}",
            ex=60 * 5,
        )
        await bot.send_sticker(
            message.chat.id,
            "CAACAgUAAxkBAAFATDphqabbLMEQSVtvg0cvZNnoLBXciAACBQQAAphHUFWUjRgXeOSWEyIE",
        )
        return False
    return True

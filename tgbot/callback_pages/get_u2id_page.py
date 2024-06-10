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
    if bool(sql.inqury_user(call.from_user.id)):
        await bot.answer_callback_query(call.id, "error!")
        return await bot.edit_message_text(
            text=text.Repeat_error(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    _text = text.Inquiry_u2id()
    await bot.answer_callback_query(call.id, "ok!")
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
    msg_text = MessageText(language)
    if not data.isdigit() or len(data) > 5:
        msg = msg_text.Inquiry_u2id(error=True)
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
    if sql_data := sql.inqury_user(u2_id=data):
        msg = msg_text.Re_verify(sql_data[0][1])
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(text=msg.markup, callback_data=f"re_ver|{language}")
        )
        await bot.reply_to(
            message,
            text=msg.text,
            reply_markup=markup,
        )
        return False
    return True

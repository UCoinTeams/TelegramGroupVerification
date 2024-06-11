from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from utils.config_vars import sql


async def send_u2info_add(message: Message, bot: AsyncTeleBot):
    """添加用户信息"""
    message_data = message.text.split(" ")
    if len(message_data) == 2:
        if message.reply_to_message is None:
            return await bot.reply_to(message, "错误使用")
        tg_id = message.reply_to_message.from_user.id
        u2_id = int(message_data[1])
    elif len(message_data) == 3:
        tg_id = int(message_data[1])
        u2_id = int(message_data[2])
        if u2_id > 100000 or tg_id < 100000:
            return await bot.reply_to(message, text="非正常数据 tg\\_id 前 u2\\_id 后")
    else:
        return await bot.reply_to(message, "错误使用")
    data = sql.inqury_user(tg_id=tg_id, u2_id=u2_id)
    if bool(data):
        return await bot.reply_to(message, text="已存在记录 如要记录请先删除记录")
    else:
        sql.insert_admin_log(
            message.from_user.id,
            message.from_user.full_name,
            "命令: add -> 添加用户信息",
            tg_id,
            u2_id,
        )
        sql.insert_user(tg_id, u2_id, "cn")
        await bot.send_message(message.chat.id, text="已记录")
    return await bot.delete_message(message.chat.id, message_id=message.message_id)

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from utils.config_vars import sql


async def send_u2info(message: Message, bot: AsyncTeleBot):
    message_data = message.text.split(" ")
    if len(message_data) == 1 and message.reply_to_message is None:
        return await bot.reply_to(message, "错误使用")
    elif len(message_data) == 1:
        query_id = message.reply_to_message.from_user.id
    elif len(message_data) == 2:
        query_id = int(message_data[1])
        if query_id > 100000:  # 判断为tg_id
            data = sql.inqury_user(query_id)
        else:
            data = sql.inqury_user(u2_id=query_id)
    if bool(data):
        text = "*以下是查询到的信息:*\n"
        for i in data:
            sql.insert_admin_log(message.from_user.id, message.from_user.full_name, "命令: uinfo -> 查询用户信息", i[1], i[2])
            text += (
                f"➤ *TG UserID: *[{i[1]}](tg://user?id={i[1]})\n"
                f"➤ *U2 UserID: *[{i[2]}](https://u2.dmhy.org/userdetails.php?id={i[2]})\n"
                f"➤ *记录语言: *`{i[3]}`\n"
                f"➤ *记录时间: *`{i[4]}`\n\n"
            )
        await bot.send_message(
            message.from_user.id,
            text=text,
            parse_mode="Markdown",
        )
    else:
        await bot.send_message(
            message.from_user.id,
            text="未查询到此用户的有关信息"
        )
    await bot.delete_message(message.chat.id, message_id=message.message_id)
    return

import asyncio
import logging
import re

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardMarkup

from utils.config_vars import sql, redis, config
from utils.data_api import DataAPI


async def send_log_msg(log_info) -> list:
    """发送日志信息"""
    bot = AsyncTeleBot(config["TG"]["BOT_TOKEN"])
    user = re.findall(
        r"id=(\d+)]【(.+?)】", log_info["message"]
    )  # 0: u2_id, 1: username
    reason = re.findall(r".+原因：(.+)\[/color]", log_info["message"])
    data = sql.inqury_user(
        u2_id=int(user[0][0])
    )  # 0: id, 1: tg_id, 2: u2_id, 3: language, 4: record_time
    if not bool(data):
        text = (
            f"#禁用帳號 \n"
            f"[{user[0][1]}（{user[0][0]}）](https://u2.dmhy.org/userdetails.php?id={user[0][0]}) 被管理员 [{user[1][1]}（{user[1][0]}）](https://u2.dmhy.org/userdetails.php?id={user[1][0]}) 禁用了\n"
            f"*原因: {reason[0]}*\n"
        )
        try:
            await bot.send_message(
                chat_id=config["TG"]["GROUP_ID"], text=text, parse_mode="Markdown"
            )
            logging.info("Schedule: [I] 推送成功")
        except:
            logging.error("Schedule: [E] 推送失败")
    else:
        logging.info("Schedule: [I] 在数据表中查询到此人 向管理员推送")
        data = data[0]
        text = (
            "[@admin](tg://user?id=633746866) *检测到本群内有被 Ban 用户：*\n\n"
            f"➤ *TG UserID: *[{data[1]}](tg://user?id={data[1]})\n"
            f"➤ *U2 UserID: *[{data[2]}](https://u2.dmhy.org/userdetails.php?id={data[2]})\n"
            f"➤ *记录语言: *`{data[3]}`\n"
            f"➤ *记录时间: *`{data[4]}`\n\n"
            f"*被 Ban 原因：*`{reason[0]}`"
        )
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardMarkup(text="移除该成员", callback_data=f"ban|{data[1]}"),
        )
        try:
            await bot.send_message(
                chat_id=config["TG"]["GROUP_ID"],
                text=text,
                parse_mode="Markdown",
                reply_markup=markup,
            )
            logging.info("Schedule: [I] 推送成功")
        except:
            logging.error("Schedule: [E] 推送失败")
    return


async def ban_detection():
    """检测 U2 禁用帐号"""
    sleep_time = 60 * 5
    while True:
        d_api = DataAPI(
            u2_cookie=config["U2_COOKIE"],
            api_uesr_id=config["API_USER_ID"],
            api_token=config["API_TOKEN"],
            bark_uel=config["BARK_URL"],
        )
        log_list = await d_api.get_u2_log()
        if not log_list:
            await asyncio.sleep(sleep_time)
            continue
        old_id = redis.get("ban_data")
        for log in log_list[::-1]:
            if "禁用帳號" in log["message"]:
                if not old_id:
                    await send_log_msg(log)
                elif log["id"] > int(old_id):
                    await send_log_msg(log)
                elif log["id"] == int(old_id):
                    break
                else:
                    continue
        redis.set("ban_data", log_list[0]["id"], ex=3600000)
        await d_api.close()
        await asyncio.sleep(sleep_time)

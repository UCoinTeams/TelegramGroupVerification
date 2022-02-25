# -*- coding:utf-8 -*-
import json
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from lxml import etree
from requests import cookies, session

from bot import bot, telebot
from config import GROUP_ID, HEADERS, U2_COOKIE

session = session()
session.headers.clear()
session.headers.update(HEADERS)
cookie_jar = cookies.RequestsCookieJar()
cookie_jar.set("nexusphp_u2", U2_COOKIE, domain="u2.dmhy.org")
session.cookies = cookie_jar

_time = 0


def ban_checker():
    global _time
    print('\n[I] 本次运行：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    try:
        print('[I] get_last_time: 发起请求')
        url = 'https://u2.dmhy.org/log.php?query=%E7%A6%81%E7%94%A8%E5%B8%B3%E8%99%9F&search=all&action=dailylog'
        result = session.get(url)
        html_data = etree.HTML(result.text.encode('utf-8'))
        time_list = html_data.xpath(
            './/td[@class="rowfollow nowrap"]/time/@title')
    except:
        print('[E] 未能获取到合法的内容：U2娘可能宕机')
        return 1
    print(f'[I] 最近一次_time: {time_list[0]}')
    if _time == 0:
        _time = time_list[0]
        print(f'[I] 初始化：{_time}')
    elif _time == time_list[0]:
        print(f'[E] 错误的：当前：{_time}；获取：{time_list[0]}')
        return 0
    print(f'[I] 处理期间新log队列：{_time} ~ {time_list[0]}')
    _ban_id_list = html_data.xpath(
        './/td[@class="rowfollow"]/font/span/bdo[@dir="ltr"]/a[1]/@href')
    _ban_reason_list = html_data.xpath(
        './/td[@class="rowfollow"]/font/span/bdo[@dir="ltr"]/text()[3]')
    a = [i for i,v in enumerate(time_list) if v == _time][0]
    ban_id_list = []
    ban_reason_list = []
    if a != 0:
        for i in range(a):
            ban_id_list.append(
                _ban_id_list[i].strip('userdetails.php?id='))
            ban_reason_list.append(_ban_reason_list[i].split('原因：')[1])
    else:
        ban_id_list.append(
            _ban_id_list[0].strip('userdetails.php?id='))
        ban_reason_list.append(_ban_reason_list[0].split('原因：')[1])
    with open('test.json') as f:
        data = json.loads(f.read())
    for ban_id, ban_reason in zip(ban_id_list, ban_reason_list):
        try:
            ban_user_data = [i for i in data if i['U2_uid'] == int(ban_id)][0]
            print('[I] 在数据表中查询到此人 向管理员推送')
            text = "@Ukennn\n*检测到本群内有被 Ban 用户：*\n\n" \
                  f"➤ *TG UserID: *[{ban_user_data.get('TG_id')}](tg://user?id={ban_user_data.get('TG_id')})\n" \
                  f"➤ *U2 UserID: *[{ban_user_data.get('U2_uid')}](https://u2.dmhy.org/userdetails.php?id={ban_user_data.get('U2_uid')})\n" \
                  f"➤ *记录时间: *`{ban_user_data.get('time')}`\n" \
                  f"➤ *记录语言: *`{ban_user_data.get('language')}`\n\n" \
                  f"*被 Ban 原因：*`{ban_reason}`"
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='移除该成员', callback_data=f"ban|{ban_user_data.get('TG_id')}"),telebot.types.InlineKeyboardButton(text='不移除', callback_data=f"unban"))
            try:
                bot.send_message(chat_id=GROUP_ID, text=text, parse_mode='Markdown', reply_markup=markup, timeout=20)
                print('[I] 推送成功')
            except:
                print('[E] 推送失败')
        except IndexError:
            print('[I] 未在数据表中查询到此人')
    _time = time_list[0]
    print('[I] 本次任务处理完毕')


def main():
    print('[I] 已启动')
    ban_checker()
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    scheduler.add_job(
        func=ban_checker,
        trigger='interval',
        minutes=1
    )
    print('\n[I] 定时任务已设置')
    scheduler.start()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        exit()

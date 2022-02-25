#!/usr/bin/python
import json
import time

import requests
import telebot
from lxml import etree
from requests import cookies, session
from requests.packages import urllib3

from config import (ADMIN_ID, BAKA_API, BOT_TOKEN, CHANNEL_ID, GROUP_ID,
                    HEADERS, U2_COOKIE, VERIFY_STR)

# 请求u2头
session = session()
session.headers.clear()
session.headers.update(HEADERS)
cookie_jar = cookies.RequestsCookieJar()
cookie_jar.set("nexusphp_u2", U2_COOKIE, domain="u2.dmhy.org")
session.cookies = cookie_jar
# 请求botapi
bot = telebot.TeleBot(BOT_TOKEN)

# 判断验证uid输入是否是数字
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(str)
        return True
    except (ValueError, TypeError):
        pass

    return False

# 欢迎
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.chat.type == "private":
        text = ("\\[中文🇨🇳]\n"
                "欢迎使用UCoin入群验证机器人\n"
                "为了确认您是U2用户，\n"
                "请输入\"/code\"来获取验证码\n\n"

                "\\[English🇬🇧]\n"
                "Welcome to the UCoin Group Join Verification Robot\n"
                "To confirm you are a U2 user, \n"
                "please enter \"/code\" to get the verification code\n\n"

                "\\[日本語🇯🇵]\n"
                "UCoin グループに入ってロボットを検証\n"
                "U2ユーザであることを確認するために、\n"
                "｢/code｣を入力して認証コードを取得してください。")
        bot.send_message(message.chat.id, text=text , reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)

# 获取验证码
@bot.message_handler(commands=['code'])
def send_code(message):
    if message.chat.type == "private":
        text = (f"验证码/CAPTCHA/認証コード: “`[url={VERIFY_STR}][/url]`”\n\n"

                "\\[中文🇨🇳]\n"
                "请将这个验证码填写在您的[U2个人说明](https://u2.dmhy.org/usercp.php?action=personal) 的任何位置，\n"
                "完成后请输入\"`/cn 你的UID`\"\n\n"

                "\\[English🇬🇧]\n"
                "Please fill in this verification code anywhere in your [U2 personal](https://u2.dmhy.org/usercp.php?action=personal) instructions.\n"
                "When finished, please enter \n"
                "\"`/en YouUID`\"\n\n"

                "\\[日本語🇯🇵]\n"
                "この検証コードをあなたの[U2個人説明](https://u2.dmhy.org/usercp.php?action=personal) するどの位置に記入してください。\n"
                "完了後は「`/jp 君のUID`」を入力してください。")
        bot.send_message(message.chat.id, text=text , reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)

# 中文验证
@bot.message_handler(commands=['cn'])
def send_cn(message):
    if message.chat.type == "private":
        data = message.text.split(' ')
        if data[0] != "/cn":
            bot.send_message(message.chat.id, "输入错误 请输入：`/cn UID`", parse_mode='Markdown', timeout=20)
            bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAFATDphqabbLMEQSVtvg0cvZNnoLBXciAACBQQAAphHUFWUjRgXeOSWEyIE', timeout=20)
        else:
            if len(data) == 2:
                uid = data[1]
                check = is_number(uid)
                if check is False:
                    bot.send_message(message.chat.id, "输入错误 请输入：`/cn UID`", parse_mode='Markdown', timeout=20)
                    bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAFATDphqabbLMEQSVtvg0cvZNnoLBXciAACBQQAAphHUFWUjRgXeOSWEyIE', timeout=20)
                else:
                    if int(uid) > 100000:
                        bot.send_message(message.chat.id, "输入错误 请输入：`/cn UID`", parse_mode='Markdown', timeout=20)
                        bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAFATDphqabbLMEQSVtvg0cvZNnoLBXciAACBQQAAphHUFWUjRgXeOSWEyIE', timeout=20)
                    else:
                        bot.send_message(message.chat.id, "请稍等正在验证... UID:" + uid, timeout=20)
                        test_id = uid
                        if data_seek(test_id) == 'yes':
                            bot.send_message(message.chat.id, "你已验证过，如有疑问请联系 @Ukennnn", timeout=20)
                        else:
                            if get_user_info(test_id) == 'yes':                            
                                text = ("*UCoin群组&频道&工具&群规声明*\n"
                                        "*群组：*\n"
                                        "[UCoin金毛食品部羡慕本部]("+ groups_invite_links(test_id) +")\n"
                                        "[UCoin English Only Group](https://t.me/joinchat/)\n"
                                        "[UCoin金毛食品部游戏分部](https://t.me/joinchat/)\n"
                                        "[UCoin金毛食品部 Line 分部](http://line.me/ti/g/)\n"
                                        "[UCoin金毛食品部蒸汽分部](https://s.team/chat/)\n"
                                        "[UCoin金毛食品部掘金分部](https://t.me/joinchat/)\n"
                                        "[UCoin金毛食品部核弹分部](https://t.me/joinchat/)\n\n"

                                        "*频道：*\n"
                                        "[动漫花园U2 Rss订阅频道]("+ channel_invite_links(test_id) +")\n"
                                        "[动漫花园BDMV U2 Rss订阅频道](https://t.me/joinchat/)\n"
                                        "[动漫花园U2种子优惠通知频道](https://t.me/joinchat/)\n\n"

                                        "*U2相关脚本&工具*：\n"
                                        "[U2状态检测](https://stats.uptimerobot.com/216D5tkXBy/785888780)\n"
                                        "[U2自动2.33优惠脚本](https://gist.github.com/littleya/86cd895f97b614ebea376a1008291ccf#file-u2auto2-33x-py)\n"
                                        "[U2做种页显示地区猴油脚本](https://gist.github.com/c0re100/3dea464145bf6abc8b1332a463fed525)"
                                        "[U2一键调戏U2娘猴油脚本（请勿滥用](https://cdn.jsdelivr.net/gh/mwhds97/PT@master/scripts/U2%E5%A8%98+.user.js)\n"
                                        "[U2 Tool Box - 通过 Telegram Bot 实现的签到、查询、施放魔法等功能的机器人](https://u2.dmhy.org/forums.php?action=viewtopic&topicid=13474&page=last#pid149883)\n"
                                        "[U2批量发糖脚本](https://share.a0000778.name/userscript/U2/gift.user.js)\n"
                                        "[U2无法访问解决办法](https://t.me/c/1364462408/548530)\n"
                                        "[U2家族树查询](https://u2.ukenn.top/)\n\n"

                                        "[UCoin系列群组群规&免责声明](https://t.me/c/1364462408/459536)\n\n"

                                        "编辑于2021年12月")                       
                                bot.send_message(message.chat.id,  text=text , parse_mode='Markdown', disable_web_page_preview=True, timeout=20)
                                nowtime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                indata = {"time": nowtime,"U2_uid": int(test_id),"TG_id": message.from_user.id,"language": 'cn'}
                                write_json(indata)
                                bark("群组新人验证通过通知", f"➤%20TG_UserID:%20{message.from_user.id}%0a➤%20U2_UserID:%20{test_id}%0a➤%20通过时间:%20{nowtime}%0a➤%20语言:%20cn")
                            else:
                                bot.send_message(message.chat.id, "验证失败，请再试一遍", timeout=20)
            else:
                bot.send_message(message.chat.id, "输入错误 请输入：`/cn UID`", parse_mode='Markdown', timeout=20)
                bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAFATDphqabbLMEQSVtvg0cvZNnoLBXciAACBQQAAphHUFWUjRgXeOSWEyIE', timeout=20)
    
# 英文验证    
@bot.message_handler(commands=['en'])
def send_cn(message):
    if message.chat.type == "private":
        data = message.text.split(' ')
        if data[0] != "/en":
            bot.send_message(message.chat.id, "Input error Please enter.`/en UID`", parse_mode='Markdown', timeout=20)
        else:
            if len(data) == 2:
                uid = data[1]
                check = is_number(uid)
                if check is False:
                    bot.send_message(message.chat.id, "Input error Please enter.`/en UID`", parse_mode='Markdown', timeout=20)
                else:
                    if int(uid) > 100000:
                        bot.send_message(message.chat.id, "Input error Please enter.`/en UID`", parse_mode='Markdown', timeout=20)
                    else:
                        bot.send_message(message.chat.id, "Please wait is verifying... UID:" + uid, timeout=20)
                        test_id = uid
                        if data_seek(test_id) == 'yes':
                            bot.send_message(message.chat.id, "You have verified, if you have any questions please contact @Ukennnn", timeout=20)
                        else:
                            if get_user_info(test_id) == 'yes':
                                text = ("*UCoin Groups & Channels & Group Rules Statement*\n\n"

                                        "*Group.*\n"
                                        "[UCoin English Only Group](https://t.me/joinchat/)\n\n"

                                        "*Channel.*\n"
                                        "[U2 Rss Subscription Channel]("+ channel_invite_links(test_id) +")\n"
                                        "[U2 Rss BDMV Subscription Channel](https://t.me/joinchat/)\n"
                                        "[U2 Seeds Discount Notification Channel](https://t.me/joinchat/)\n\n"

                                        "[UCoin Group Rules & Disclaimer](https://t.me/c/1364462408/459536)\n\n"

                                        "Edited in December 2021")
                                bot.send_message(message.chat.id, text=text , parse_mode='Markdown', disable_web_page_preview=True, timeout=20)
                                nowtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                indata = {"time": nowtime,"U2_uid": int(test_id),"TG_id": message.from_user.id,"language": 'en'}
                                write_json(indata)
                                bark("群组新人验证通过通知", f"➤%20TG_UserID:%20{message.from_user.id}%0a➤%20U2_UserID:%20{test_id}%0a➤%20通过时间:%20{nowtime}%0a➤%20语言:%20en")
                            else:
                                bot.send_message(message.chat.id, "Verification failed, please try again", timeout=20)

            else:
                bot.send_message(message.chat.id, "Input error Please enter.`/en UID`", parse_mode='Markdown', timeout=20)

# 日文验证
@bot.message_handler(commands=['jp'])
def send_cn(message):
    if message.chat.type == "private":
        data = message.text.split(' ')
        if data[0] != "/jp":
            bot.send_message(message.chat.id, "入力エラー 入力：`/jp UID`", parse_mode='Markdown', timeout=20)
        else:
            if len(data) == 2:
                uid = data[1]
                check = is_number(uid)
                if check is False:
                    bot.send_message(message.chat.id, "入力エラー 入力：`/jp UID`", parse_mode='Markdown', timeout=20)
                else:
                    if int(uid) > 100000:
                        bot.send_message(message.chat.id, "入力エラー 入力：`/jp UID`", parse_mode='Markdown', timeout=20)
                    else:
                        bot.send_message(message.chat.id, "検証中 少々お待ちください... UID:" + uid, timeout=20)
                        test_id = uid
                        if data_seek(test_id) == 'yes':
                            bot.send_message(message.chat.id, "検証済みですので、ご質問があれば @Ukennn にお問い合わせください", timeout=20)
                        else:
                            if get_user_info(test_id) == 'yes':
                                text = ("*UCoin Groups & Channels & Group Rules Statement*\n\n"

                                        "*Group.*\n"
                                        "[UCoin English Only Group](https://t.me/joinchat/)\n\n"

                                        "*Channel.*\n"
                                        "[U2 Rss Subscription Channel]("+ channel_invite_links(test_id) +")\n"
                                        "[U2 Rss BDMV Subscription Channel](https://t.me/joinchat/)\n"
                                        "[U2 Seeds Discount Notification Channel](https://t.me/joinchat/)\n\n"

                                        "[UCoin Group Rules & Disclaimer](https://t.me/c/1364462408/459536)\n\n"

                                        "Edited in December 2021")
                                bot.send_message(message.chat.id, text=text , parse_mode='Markdown', disable_web_page_preview=True, timeout=20)
                                nowtime=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                                indata = {"time": nowtime,"U2_uid": int(test_id),"TG_id": message.from_user.id,"language": 'jp'}
                                write_json(indata)
                                bark("群组新人验证通过通知", f"➤%20TG_UserID:%20{message.from_user.id}%0a➤%20U2_UserID:%20{test_id}%0a➤%20通过时间:%20{nowtime}%0a➤%20语言:%20jp")
                            else:
                                bot.send_message(message.chat.id, "検証に失敗しました、もう一度試してください。", timeout=20)

            else:
                bot.send_message(message.chat.id, "入力エラー 入力：`/jp UID`", parse_mode='Markdown', timeout=20)

# 查询目标u2 uid
@bot.message_handler(commands=['uinfo'])
def send_u2info(message):
    message_data = message.text.split(' ')
    getuser_id = message.from_user.id
    if getuser_id == ADMIN_ID:
        if len(message_data) == 1:
            from_user = message.reply_to_message.from_user.id
        if len(message_data) == 2:
            from_user = int(message_data[1])
        with open('test.json') as f:
            data = json.loads(f.read())
        try:
            if from_user > 100000:
                user_data = [i for i in data if i['TG_id'] == from_user][0]
            else:
                user_data = [i for i in data if i['U2_uid'] == from_user][0]
                from_user = user_data.get('TG_id')
            login_time = str(user_data.get('time'))
            u2_uid = str(user_data.get('U2_uid'))
            language = user_data.get('language')
            text = ('*以下是查询到的信息:*\n'
                    '➤ *TG UserID: *['+str(from_user)+'](tg://user?id='+str(from_user)+')\n'
                    '➤ *U2 UserID: *['+u2_uid+'](https://u2.dmhy.org/userdetails.php?id='+u2_uid+')\n'
                    '➤ *记录时间: *`'+login_time+'`\n'
                    '➤ *记录语言: *`'+language+'`')
            bot.send_message(message.chat.id, text=text, reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
            bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)
        except IndexError:
            bot.send_message(message.chat.id, text='未查询到此用户的有关信息' , reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
            bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)
    else:
        bot.send_message(message.chat.id, text='该功能只限超级管理员使用', reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
        bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)

# 记录u2 uid
@bot.message_handler(commands=['add'])
def send_u2info(message):
    message_data = message.text.split(' ')
    getuser_id = message.from_user.id
    if getuser_id == ADMIN_ID:
        if len(message_data) == 2:
            from_user = message.reply_to_message.from_user.id
            u2_uid = int(message_data[1])
        if len(message_data) == 3:
            from_user = int(message_data[1])
            u2_uid = int(message_data[2])
        if u2_uid >100000 or from_user<100000:
            bot.send_message(message.chat.id, text='非正常数据' , reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
            bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)
        else:
            with open('test.json') as f:
                data = json.loads(f.read())
            tg_data = [i for i in data if i['TG_id'] == from_user]
            u2_data = [i for i in data if i['U2_uid'] == u2_uid]
            if tg_data == [] and u2_data == []:
                nowtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) # 当前时间
                indata = {"time": nowtime,"U2_uid": u2_uid,"TG_id": from_user,"language": 'cn'}
                write_json(indata)
                bot.send_message(message.chat.id, text='已记录' , reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
                bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)
            else:
                bot.send_message(message.chat.id, text='重复记录' , reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
                bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)
    else:
        bot.send_message(message.chat.id, text='该功能只限超级管理员使用', reply_to_message_id=message.message_id , parse_mode='Markdown', timeout=20)
        bot.delete_message(message.chat.id, message_id=message.message_id, timeout=20)

# 处理 ban 按钮
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'ban')
def back_week_callback(call):
    ban_id = call.data.split('|')[1]
    if call.from_user.id == ADMIN_ID:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id, timeout=20)
        bot.ban_chat_member(chat_id=call.message.chat.id, user_id=ban_id)
        bot.send_message(chat_id=call.message.chat.id, text=f'已将 {ban_id} 从该群组移除', parse_mode='Markdown', timeout=20)
    else:
        bot.answer_callback_query(call.id, text='此操作只允许超级管理员使用', show_alert=True)

# 处理 unban 按钮
@bot.callback_query_handler(func=lambda call: call.data.split('|')[0] == 'unban')
def back_week_callback(call):
    if call.from_user.id == ADMIN_ID:
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id, timeout=20)
    else:
        bot.answer_callback_query(call.id, text='此操作只允许超级管理员使用', show_alert=True)

# 创建群组链接
def groups_invite_links(test_id):
    name = test_id                                                     # 备注UID
    link = bot.create_chat_invite_link(GROUP_ID, name, member_limit=1) # 创建群组链接
    return link.invite_link                                            # 返回群组链接

# 创建频道链接
def channel_invite_links(test_id):
    name = test_id                                                       # 备注UID
    link = bot.create_chat_invite_link(CHANNEL_ID, name, member_limit=1) # 创建频道链接
    return link.invite_link                                              # 返回频道链接
    
# 记录验证信息
def write_json(indata):
    with open("test.json", 'r+', encoding='utf-8') as f:    # 打开文件
        try:
            data = json.load(f)                             # 读取
        except:
            data = []                                       # 空文件
        data.append(indata)                                 # 添加
        f.seek(0, 0)                                        # 重新定位回开头
        json.dump(data, f, ensure_ascii=False, indent=4)    # 写入

# 判断是否重复验证
def data_seek(test_id):
    with open('test.json') as f:                            # 打开文件
        data_seek = json.loads(f.read())                    # 读取
    data_li = [i['U2_uid'] for i in data_seek]              # 写入列表
    if int(test_id) in data_li:                             # 判断列表内是否有被验证的UID
        data_back = 'yes'
    else:
        data_back = 'no'
    return data_back                                        # 返回是否重复验证

# 判断U2个人简介是否有验证信息
def get_user_info(test_id):
    promotion_url = 'https://u2.dmhy.org/userdetails.php?id='+str(test_id)  # 请求U2地址
    urllib3.disable_warnings()
    result = session.get(promotion_url)
    html = etree.HTML(result.text.encode('utf-8'))
    codes_list = []                                                         # 生成一个空列表
    for li in html.xpath('//a[@class="faqlink"]'):                          # 定位
        codes_list.append(li.xpath('./@href')[0])                           # 将网页爬取的数据写入列表
    if VERIFY_STR in codes_list:                                            # 判断列表内是否有验证码
        test_back = 'yes'
    else:
        test_back = 'no'
    return test_back                                                        # 返回是否有验证信息

# baka推送
def bark(title: str, content: str):
    url = f'{BAKA_API}/{title}/{content}?icon=https://s2.loli.net/2022/02/14/tmAqHOKT1VWp8CR.jpg?group=GroupLogin'
    return requests.get(url)

# 开始启动
if __name__ == '__main__':
    bot.polling()

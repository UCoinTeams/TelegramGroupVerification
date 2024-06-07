class MessageText:
    def __init__(self, language: str = "cn"):
        self.language = language

    def Ver_passed(self, group_link, channel_link):
        if self.language == "cn":
            return (
                "*UCoin群组&频道&工具&群规声明*\n"
                "*群组：*\n"
                f"[UCoin金毛食品部 羡充上流本部 (主群)]({group_link})\n"
                "[UCoin English Only Group](https://t.me/joinchat/P1RbQxeaDbgtQCTvgyE4Gg)\n"
                "[UCoin金毛食品部 游戏分部](https://t.me/joinchat/dr_HTf1VNjo5OTg1)\n"
                "[UCoin金毛食品部 掘金分部](https://t.me/joinchat/zPSga0GOZRtjMzZl)\n"
                "[UCoin金毛食品部 核弹分部](https://t.me/+3S_p-zHN7RoxOTNl)\n"
                "[UCoin金毛食品部 Line 分部](http://line.me/ti/g/gU7yYyZz_v)\n"
                "[UCoin金毛食品部 Steam(蒸汽) 分部](https://s.team/chat/fbTxLWZ6)\n"
                "[UCoin金毛食品部 Twitter 分部](https://twitter.com/i/communities/1501161490467864582)\n"
                "[UCoin金毛食品部 Github 分部](https://github.com/UCoinTeams)\n\n"
                "*频道：*\n"
                f"[动漫花园 U2 Rss订阅频道]({channel_link})\n"
                "[动漫花园 BDMV U2 Rss订阅频道](https://t.me/joinchat/UOaDykBRORQSIlYQ)\n"
                "[动漫花园 U2 种子优惠通知频道](https://t.me/joinchat/RuCiWjkv34hMv7PM)\n"
                "[动漫花园 U2 种子候选通知频道](https://t.me/+7WfqFTF-MqcyMGFl)\n\n"
                "*U2相关脚本&工具*：\n"
                "[U2状态检测](https://stats.uptimerobot.com/216D5tkXBy/785888780)\n"
                "[U2自动2.33优惠脚本](https://gist.github.com/littleya/86cd895f97b614ebea376a1008291ccf#file-u2auto2-33x-py)\n"
                "[U2做种页显示地区猴油脚本](https://gist.github.com/c0re100/3dea464145bf6abc8b1332a463fed525)"
                "[U2一键调戏U2娘猴油脚本（请勿滥用](https://cdn.jsdelivr.net/gh/mwhds97/PT@master/scripts/U2%E5%A8%98+.user.js)\n"
                "[U2 Tool Box - 通过 Telegram Bot 实现的签到、查询、施放魔法等功能的机器人](https://u2.dmhy.org/forums.php?action=viewtopic&topicid=13474&page=last#pid149883)\n"
                "[U2批量发糖脚本](https://share.a0000778.name/userscript/U2/gift.user.js)\n"
                "[U2无法访问解决办法](https://t.me/c/1364462408/548530)\n"
                "[U2家族树查询](https://u2.ukenn.top/)\n"
                "[U2怎么看种子的发种者](https://t.me/c/1364462408/1064844)\n\n"
                "[UCoin系列群组群规&免责声明](https://t.me/c/1364462408/459536)\n\n"
                "编辑于2024年5月"
            )
        elif self.language == "en":
            return (
                "*UCoin Groups & Channels & Group Rules Statement*\n\n"
                "*Group.*\n"
                "[UCoin English Only Group](https://t.me/joinchat/P1RbQxeaDbgtQCTvgyE4Gg)\n\n"
                "*Channel.*\n"
                f"[U2 Rss Subscription Channel]({channel_link})\n"
                "[U2 Rss BDMV Subscription Channel](https://t.me/joinchat/UOaDykBRORQSIlYQ)\n"
                "[U2 Seeds Discount Notification Channel](https://t.me/joinchat/RuCiWjkv34hMv7PM)\n"
                "[U2 Seeds Candidate Notification Channel](https://t.me/+7WfqFTF-MqcyMGFl)\n\n"
                "[UCoin Group Rules & Disclaimer](https://t.me/c/1364462408/459536)\n\n"
                "Edited in September 2022"
            )
        elif self.language == "ja":
            return (
                "*UCoin Groups & Channels & Group Rules Statement*\n\n"
                "*Group.*\n"
                "[UCoin English Only Group](https://t.me/joinchat/P1RbQxeaDbgtQCTvgyE4Gg)\n\n"
                "*Channel.*\n"
                f"[U2 Rss Subscription Channel]({channel_link})\n"
                "[U2 Rss BDMV Subscription Channel](https://t.me/joinchat/UOaDykBRORQSIlYQ)\n"
                "[U2 Seeds Discount Notification Channel](https://t.me/joinchat/RuCiWjkv34hMv7PM)\n"
                "[U2 Seeds Candidate Notification Channel](https://t.me/+7WfqFTF-MqcyMGFl)\n\n"
                "[UCoin Group Rules & Disclaimer](https://t.me/c/1364462408/459536)\n\n"
                "Edited in September 2022"
            )

    def Welcome(self):
        return (
            "*欢迎使用 UCoin 入群验证机器人\n\n"
            "Welcome to use the UCoin group verification bot\\.\n\n"
            "UCoin入群認証ボットへようこそ*"
        )
    
    def Repeat_error(self):
        if self.language == "cn":
            return "*此用户已绑定过 U2 账号*"
        elif self.language == "en":
            return "*This user has already bound a U2 account*"
        elif self.language == "ja":
            return "*このユーザーはすでに U2 アカウント にバインドされています*"

    def Re_verify(self, tg_id: int = None):
        if self.language == "cn":
            self.text = f"*此账号已绑定 TelegramID: \\*\\*\\*\\*\\*{tg_id % 10000}\n\n是否解除该账号绑定，重新进行验证？*"
            self.markup = "解除绑定并重新验证"
        elif self.language == "en":
            self.text = f"*This account has been bound to TelegramID: \\*\\*\\*\\*\\*{tg_id % 10000}\\.\n\nDo you want to unbind this account and re\\-verify it?*"
            self.markup = "Unbind and re-verify"
        elif self.language == "ja":
            self.text = f"*このアカウントは TelegramID: \\*\\*\\*\\*\\*{tg_id % 10000} にバインドされています\n\nこのアカウントのバインドを解除し、再度検証しますか？*"
            self.markup = "バインドを解除して再検証する"
        return self

    def Ver_error(self):
        if self.language == "cn":
            return "今日验证次数已达上限，请明天再试"
        elif self.language == "en":
            return "The number of verifications today has reached the limit, please try again tomorrow"
        elif self.language == "ja":
            return "今日の検証回数が上限に達しました。明日もう一度お試しください"

    def Not_detected(self):
        if self.language == "cn":
            return "未检测到验证信息"
        elif self.language == "en":
            return "No verification information detected"
        elif self.language == "ja":
            return "検証情報が検出されませんでした"

    def Inquiry_u2id(self, error: bool = False):
        if error:
            if self.language == "cn":
                self.text = "*输入错误, 请重新输入您的 U2 UID*"
                self.markup = "请重新输入 U2 UID"
                return self
            elif self.language == "en":
                self.text = "*Input error, please re-enter your U2 ID*"
                self.markup = "Re-enter your U2 UID"
                return self
            elif self.language == "ja":
                self.text = "*入力エラー、U2 UID を再入力してください*"
                self.markup = "U2 UID を再入力してください"
                return self
        elif self.language == "cn":
            self.text = (
                "*为了确认您是 U2 用户, 现在需要进行必要验证步骤\n\n"
                "请发送您的 U2 UID*"
            )
            self.markup = "请输入 U2 UID"
            return self
        elif self.language == "en":
            self.text = (
                "*To confirm that you are a U2 user, we now need to proceed with the necessary verification steps\\.\n\n"
                "Please send your U2 UID*"
            )
            self.markup = "Enter your U2 UID"
            return self
        elif self.language == "ja":
            self.text = (
                "*U2のユーザーであることを確認するために、必要な検証手順が必要です。\n\n"
                "U2 UID を送信してください*"
            )
            self.markup = "U2 UID を入力してください"
            return self

    def Ver_code(self, u2_id, tg_id, v_code: str):
        if self.language == "cn":
            self.text = (
                f"UID: `{u2_id}` \\(`{tg_id}`\\) 开始验证\n\n"
                f"*您的验证标识符为:* \n\n`[url={v_code}][/url]`\n\n"
                "可将此标识符填写在您的 [U2 个人说明](https://u2.dmhy.org/usercp.php?action=personal) 的__任意位置__并保存，"
                "完成后点击下方验证开始按钮\n\n"
                "__注: 本标识符实际不会在个人说明页显示出来, 验证完成后可删除此标识符__"
            )
            self.markup = "验证开始"
            return self
        elif self.language == "en":
            self.text = (
                f"*UID: {u2_id} \\(TG ID: {tg_id}\\) starts verification\n\n"
                f"Your verification identifier is: `[url={v_code}][/url]`\n\n"
                "Please fill in this verification code in any position of your [U2 personal description](https://u2.dmhy.org/usercp.php?action=personal),\n"
                "After completion, click the button below to start verification*"
            )
            self.markup = "Start verification"
            return self
        elif self.language == "ja":
            self.text = (
                f"*UID: {u2_id} \\(TG ID: {tg_id}\\) 検証を開始します\n\n"
                f"あなたの検証コードは: `[url={v_code}][/url]`\n\n"
                "この検証コードを [U2個人説明](https://u2.dmhy.org/usercp.php?action=personal) の任意の位置に入力してください。\n"
                "完了後、下のボタンをクリックして検証を開始します*"
            )
            self.markup = "検証を開始します"
            return self

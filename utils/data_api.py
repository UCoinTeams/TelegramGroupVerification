import aiohttp
from lxml.etree import HTML


class DataAPI:
    def __init__(self, u2_cookie: str, bark_uel: str):
        self.u2_cookie = u2_cookie
        self.bark_url = bark_uel
        self.s = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10),
            headers={
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.8",
            },
        )

    async def close(self):
        await self.s.close()

    async def verify_u2_captcha(self, u2_id: int, captcha: str) -> bool:
        """验证 U2 验证码"""
        async with self.s.get(
            f"https://u2.dmhy.org/userdetails.php?id={u2_id}",
            headers={"Cookie": self.u2_cookie},
        ) as resp:
            html = HTML(await resp.text(encoding="utf-8"))
            info_data_list = []
            for info_data in html.xpath('//a[@class="faqlink"]'):
                info_data_list.append(info_data.xpath("./@href")[0])
            if captcha in info_data_list:
                return True
            return False

    async def bark_notify(self, title, content, tg_user_id) -> None:
        """Bark 推送"""
        return await self.s.get(
            f"{self.bark_url}/{title}/{content}",
            params={
                "icon": "https://s2.loli.net/2022/02/14/tmAqHOKT1VWp8CR.jpg",
                "group": "GroupLogin",
                "url": f"tg://user?id={tg_user_id}",
            },
        )

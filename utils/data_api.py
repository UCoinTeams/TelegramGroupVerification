import aiohttp
import logging
from lxml.etree import HTML


class DataAPI:
    def __init__(self, u2_cookie: str, api_user_id: int, api_token: str, bark_url: str):
        self.u2_cookie = u2_cookie
        self.api_user_id = api_user_id
        self.api_token = api_token
        self.bark_url = bark_url
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10),
            headers={
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.8",
            },
        )

    async def close(self):
        """关闭会话"""
        if not self.session.closed:
            await self.session.close()

    async def verify_u2_captcha(self, u2_id: int, captcha: str) -> bool:
        """验证 U2 验证码"""
        try:
            async with self.session.get(
                f"https://u2.dmhy.org/userdetails.php?id={u2_id}",
                headers={"Cookie": self.u2_cookie},
            ) as resp:
                if resp.status != 200:
                    return False
                html = HTML(await resp.text(encoding="utf-8"))
                info_data_list = [
                    link.get("href") for link in html.xpath('//a[@class="faqlink"]')
                ]
                return captcha in info_data_list
        except aiohttp.ClientError as e:
            logging.error(f"Error during captcha verification: {e}")
            return False

    async def bark_notify(self, title: str, content: str, tg_user_id: int) -> None:
        """Bark 推送"""
        try:
            async with self.session.get(
                f"{self.bark_url}/{title}/{content}",
                params={
                    "icon": "https://s2.loli.net/2022/02/14/tmAqHOKT1VWp8CR.jpg",
                    "group": "GroupLogin",
                    "url": f"tg://user?id={tg_user_id}",
                },
            ) as resp:
                if resp.status != 200:
                    logging.error(f"Bark notification failed with status: {resp.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Error during Bark notification: {e}")

    async def get_u2_log(self) -> list:
        """U2 log API"""
        try:
            async with self.session.get(
                "https://u2.kysdm.com/api/v1/log",
                params={
                    "uid": self.api_user_id,
                    "token": self.api_token,
                    "maximum": 10,
                },
            ) as resp:
                if resp.status != 200:
                    logging.error(f"Failed to fetch logs with status: {resp.status}")
                    return []
                data = await resp.json()
                return data.get("data", {}).get("log", [])
        except aiohttp.ClientError as e:
            logging.error(f"Error during U2 log retrieval: {e}")
            return []

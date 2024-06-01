import time
import sqlite3
from typing import Union


class SQLite:
    def __init__(self):
        self.conn = sqlite3.connect("data/bot.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_user_db(self) -> None:
        """创建数据库表"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id integer primary key AUTOINCREMENT,
                tg_id integer UNIQUE,
                u2_id integer,
                language varchar(128),
                record_time varchar(128)
            )
            """
        )
        self.conn.commit()

    def insert_user(self, tg_id: int, u2_id: int, language: str) -> None:
        """插入用户信息"""
        self.cursor.execute(
            """
            INSERT INTO user (tg_id, u2_id, language, record_time)
            VALUES (?, ?, ?, ?)
            """,
            (
                tg_id,
                u2_id,
                language,
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            ),
        )
        self.conn.commit()

    def inqury_user(self, tg_id: int = None, u2_id: int = None) -> Union[None, list]:
        """查询用户信息
        :param tg_id: Telegram 用户 ID
        :param u2_id: U2 用户 ID
        :return: 查询结果(列表) 0: id, 1: tg_id, 2: u2_id, 3: language, 4: record_time"""
        data = self.cursor.execute(
            """
            SELECT * FROM user WHERE tg_id = ? OR u2_id = ?
            """,
            (tg_id, u2_id),
        )
        return data.fetchall()

    def delete_user(self, tg_id: int = None, u2_id: int = None) -> None:
        """删除用户信息"""
        self.cursor.execute(
            """
            DELETE FROM user WHERE tg_id = ? OR u2_id = ?
            """,
            (tg_id, u2_id),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

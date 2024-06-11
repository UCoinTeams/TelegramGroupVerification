import time
import sqlite3
from typing import Union
from datetime import datetime


class SQLite:
    def __init__(self):
        self.conn = sqlite3.connect("data/bot.db", check_same_thread=False)
        self.logdb_conn = sqlite3.connect("data/admin_log.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.logdb_cursor = self.logdb_conn.cursor()

    def create_user_db(self) -> None:
        """创建用户数据库表"""
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

    def admin_log_db(self) -> None:
        """创建管理员日志数据库表"""
        self.logdb_cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS admin_log (
                id integer primary key AUTOINCREMENT,
                tg_id integer,
                username varchar(128),
                action text,
                operated_tg_id integer,
                operated_u2_id integer,
                record_time TIMESTAMP
            )
            """
        )
        self.logdb_conn.commit()

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

    def insert_admin_log(
        self,
        tg_id: int,
        username: str,
        action: str,
        operated_tg_id: int,
        operated_u2_id: int,
    ) -> None:
        """插入管理员日志"""
        self.logdb_cursor.execute(
            """
            INSERT INTO admin_log (tg_id, username, action, operated_tg_id, operated_u2_id, record_time)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                tg_id,
                username,
                action,
                operated_tg_id,
                operated_u2_id,
                datetime.now().timestamp() // 1,
            ),
        )
        self.logdb_conn.commit()

    def close(self):
        self.conn.close()

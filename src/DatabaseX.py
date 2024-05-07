# coding = utf-8

#   ——————————————————————————————————————————————————————————
#     DatabaseX 将重构并解决 Database 的低可靠性问题，将提供 容错、验证、
#   备份、恢复、日志记录等功能。
#   ——————————————————————————————————————————————————————————

import sqlite3
from Logger import logger


class DB:
    def __init__(self, path):
        log = logger("DatabaseX")   # 创建日志记录

        self.path = "../database/" + path

        self.conn = sqlite3.connect(self.path)  # 连接数据库

        log.debug("Connect to database successfully")

        self.cursor = self.conn.cursor()  # 创建游标

        self.columns = ["id", "name", "type", "tag", "quantity", "price", "consumables", "remark", "ascription"]


if __name__ == '__main__':
    db = DB("test.db")

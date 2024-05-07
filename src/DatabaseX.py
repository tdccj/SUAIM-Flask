# coding = utf-8

#   ——————————————————————————————————————————————————————————
#     DatabaseX 将重构并解决 Database 的低可靠性问题，将提供 容错、验证、
#   备份、恢复、日志记录等功能。
#   ——————————————————————————————————————————————————————————

import sqlite3
from src.Logger import logger


class DBX:
    def __init__(self, path):
        self.log = logger("DatabaseX")  # 创建日志记录

        self.path = "../database/" + path

        self.conn = sqlite3.connect(self.path)  # 连接数据库

        self.log.debug("Connect to database successfully")

        self.cursor = self.conn.cursor()  # 创建游标

        self.columns = ["id", "name", "type", "tag", "quantity", "price", "consumables", "remark", "ascription"]

    def get_normal_columns(self):
        # 获取默认列名
        return self.columns

    def create_table(self, table_name):
        # 创建表单

        #   ________________________________________
        #   name        INTEGER 名称
        #   type        TEXT    类型
        #   tag         TEXT    标签
        #   quantity    REAL    数量
        #   price       REAL    价值
        #   consumables TEXT    是否为消耗品(消耗品周期)
        #   remark      TEXT    备注
        #   ascription  TEXT    归属人
        #   ________________________________________

        try:
            self.cursor.execute(f'''CREATE TABLE "{table_name}" (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            type        TEXT    NOT NULL,
            tag         TEXT,
            quantity    REAL    NOT NULL,
            price       REAL,
            consumables TEXT,   
            remark      TEXT,
            ascription  TEXT    NOT NULL


            );''')

            self.conn.commit()  # 提交

            self.log.debug(f"Create to table {table_name} successfully")

            return {"status": "success", "message": f"Create to table {table_name} successfully"}

        except sqlite3.OperationalError as ex:
            self.log.debug(f"Create to table {table_name} failed , Because {ex}")
            if "already exists" in str(ex):
                return {"status": "failed", "message": f"Table {table_name} is already exists"}
            else:
                return {"status": "failed", "message": f"Create to table {table_name} failed"}


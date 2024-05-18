# coding = utf-8
import os
from datetime import datetime
import sqlite3

from src.DBX.DBInfo import DBInfoManager
#   ——————————————————————————————————————————————————————————
#     DatabaseX 将重构并解决 Database 的低可靠性问题，将提供 容错、验证、
#   备份、恢复、日志记录等功能。
#   ——————————————————————————————————————————————————————————

from src.DBX.Table import Table
from src.DBX.Item import Item
from src.Execute import ExeTools
from src.Logger import logger


class DBX:
    # DBX 现在使用多继承实现模块化开发
    def __init__(self, db_name):
        self.log = logger("DatabaseX")  # 创建日志记录

        self.db_name = db_name + (".db" if ".db" not in db_name else "")

        self.path = "../database/" + self.db_name

        self.conn = sqlite3.connect(self.path)  # 连接数据库

        self.log.debug(f"Connect to database '{self.db_name}' successfully")

        self.cursor = self.conn.cursor()  # 创建游标

        # 标准字段划分，不包含 show 字段
        self.columns = ["id", "name", "type", "tag", "quantity", "price", "consumables", "remark", "ascription"]

        self.Execute = ExeTools(self.conn, self.log)

        # 调用 DBX 的各个模块
        self.table = Table(self.columns, self.Execute, self.db_name)
        self.item = Item(self.columns, self.Execute, self.db_name, self.log)

        # 用于管理数据库信息
        self.db_info = DBInfoManager(self.table, self.item, self.db_name, self.log)
        self.db_info.manager_info()

    def result(self):
        # 获取 connect(init) 后的返回值
        return self.db_info

    def __del__(self):
        # todo 更新关闭时间
        self.conn.commit()
        self.conn.close()
        self.log.debug(f"Close database '{self.db_name}' successfully")

    @staticmethod
    def get_all_db():
        databases = os.listdir("../database/")
        databases = list(filter(lambda x: x.endswith(".db"), databases))
        res = ExeTools(None, logger("DatabaseX")).execute("", "Get all databases successfully", enable=False)
        res["result"] = databases
        return res

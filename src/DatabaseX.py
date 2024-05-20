# coding = utf-8
import os
import sqlite3
from typing import Callable

from src.DBX.DBInfo import DBInfoManager
#   ——————————————————————————————————————————————————————————
#     DatabaseX 将重构并解决 Database 的低可靠性问题，将提供 容错、验证、
#   备份、恢复、日志记录等功能。
#   ——————————————————————————————————————————————————————————

from src.DBX.Table import Table
from src.DBX.Item import Item
from src.Execute import ExeTools, ExeWrapper
from src.Logger import logger

from src.ErrorType import ReturnError

log = logger("DatabaseX")
exeDBX = ExeWrapper("DatabaseX", log).try_execute


class DBX:
    # DBX 现在使用多继承实现模块化开发
    def __init__(self, db_name):
        self.log = log  # 创建日志记录

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
    @exeDBX
    def get_all_db():
        databases = os.listdir("../database/")
        databases = list(filter(lambda x: x.endswith(".db"), databases))
        res = ExeTools(None, logger("DatabaseX")).execute("", "Get all databases", enable=False)
        res["result"] = databases
        return res

    @staticmethod
    @exeDBX
    def delete_db(db_name: str):
        return DBX._process_db(db_name, os.remove, "Delete", asc=False)

    @staticmethod
    def _process_db(db_name: str, func: Callable, handle: str, asc: bool = True, **kwargs):
        # 用于处理带有确认存在-执行-确认不存在逻辑的数据库os操作
        # 当 asc = False 时，逻辑为 确认不存在-执行-确认存在
        # 注意不得加 exeDBX 装饰器，而应在具体操作中加，不然会返回 None
        db_name = db_name + (".db" if ".db" not in db_name else "")
        path = f"../database/{db_name}"
        if os.path.exists(path) and asc:
            func(path)
            if not os.path.exists(path) and asc:
                return ExeTools.standard_output(True, f"{handle} database {db_name}")

        # todo 可以考虑细化 raise 的返回类型，在不同位置增加不同 raise
        # 如果失败
        raise ReturnError

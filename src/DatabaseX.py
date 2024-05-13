# coding = utf-8
import sqlite3

#   ——————————————————————————————————————————————————————————
#     DatabaseX 将重构并解决 Database 的低可靠性问题，将提供 容错、验证、
#   备份、恢复、日志记录等功能。
#   ——————————————————————————————————————————————————————————

from src.DBX.Table import Table
from src.DBX.Item import Item
from src.Execute import Execute
from src.Logger import logger


class DBX(Table, Item):
    # DBX 现在使用多继承实现模块化开发
    def __init__(self, db_name):
        self.log = logger("DatabaseX")  # 创建日志记录

        self.db_name = db_name

        self.path = "../database/" + self.db_name

        self.conn = sqlite3.connect(self.path)  # 连接数据库

        self.log.debug(f"Connect to database '{self.db_name}' successfully")

        self.cursor = self.conn.cursor()  # 创建游标

        # 标准字段划分，不包含 show 字段
        self.columns = ["id", "name", "type", "tag", "quantity", "price", "consumables", "remark", "ascription"]

        self.Execute = Execute(self.conn, self.log)

        # 将 init 后的静态对象传给父类，避免重复初始化
        Table.__init__(self, self.columns, self.Execute, self.db_name)
        Item.__init__(self, self.columns, self.Execute, self.db_name)

    def result(self):
        # 获取 connect(init) 后的返回值
        return self.Execute.execute("", f"Get database '{self.db_name}' connect result", enable=False)

    def __del__(self):
        self.conn.close()
        self.log.debug(f"Close database '{self.db_name}' successfully")


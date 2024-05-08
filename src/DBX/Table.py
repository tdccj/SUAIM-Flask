# coding = utf-8
import sqlite3
from src.Logger import logger
from src.Execute import Execute, Ignore, IgnoreList


class Table:

    def __init__(self, columns: list, execute: Execute):
        self.columns = columns
        self.Execute = execute

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

        query = f'''CREATE TABLE "{table_name}" (
             id          INTEGER PRIMARY KEY AUTOINCREMENT,
             name        TEXT    NOT NULL,
             type        TEXT    NOT NULL,
             tag         TEXT,
             quantity    REAL    NOT NULL,
             price       REAL,
             consumables TEXT,
             remark      TEXT,
             ascription  TEXT    NOT NULL


             );'''

        handle = f"Create table '{table_name}'"

        # 将 重复创建 等 不重要的报错 归为 info，将其他报错 设为 warning 以便排错
        il = IgnoreList(Ignore("already exists", f"Create table '{table_name}'", f"Table '{table_name}' is already "
                                                                                 f"exists"))

        return self.Execute.execute(query, handle, ignores=il)

    def delete_table(self, table_name):
        # 删除表

        query = f"DROP TABLE '{table_name}';"

        handle = f"Delete table '{table_name}'"

        il = IgnoreList(Ignore("no such table", f"Delete table '{table_name}'", f"Table '{table_name}' is not exists"))

        return self.Execute.execute(query, handle, ignores=il)

    def rename_table(self, old_name, new_name):
        # 修改表名

        query = f"ALTER TABLE '{old_name}' RENAME TO '{new_name}'"

        handle = f"Rename table '{old_name}' to '{new_name}'"

        il = IgnoreList(Ignore("no such table", f"Rename table '{old_name}' to '{new_name}'", f"Table '{old_name}' is "
                                                                                              f"not exists"))
        return self.Execute.execute(query, handle, ignores=il)

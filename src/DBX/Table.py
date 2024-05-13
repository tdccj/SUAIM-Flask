# coding = utf-8

from src.Execute import ExeTools, Ignore, IgnoreList


class Table:

    def __init__(self, columns: list, execute: ExeTools, db_name: str):
        self.columns = columns
        self.Execute = execute
        self.db_name = db_name

    def s_update_table(self, table_name: str):
        # 升级 v0.1.1-19 之前的表，为其添加 show 字段
        query = f"ALTER TABLE '{table_name}' ADD COLUMN 'show' INTEGER NOT NULL DEFAULT 1;"
        handle = f"Update table '{table_name}' to v0.1.1-19 in database '{self.db_name}'"
        return self.Execute.execute(query, handle)

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
        #   show        INTEGER 是否显示(主要用于标记删除)
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
             ascription  TEXT    NOT NULL,
             show        INTEGER NOT NULL DEFAULT 1,

             );'''

        handle = f"Create a table '{table_name}' in '{self.db_name}'"

        # 将 重复创建 等 不重要的报错 归为 info，将其他报错 设为 warning 以便排错
        il = IgnoreList(Ignore("already exists", f"Create a table '{table_name}' in database '{self.db_name}'",
                               f"Table '{table_name}' is already exists in database '{self.db_name}'"))

        return self.Execute.execute(query, handle, ignore_list=il)

    def delete_table(self, table_name):
        # 删除表

        query = f"DROP TABLE '{table_name}';"

        handle = f"Delete a table '{table_name}' in database '{self.db_name}'"

        il = IgnoreList(
            Ignore("no such table", f"Delete a table '{table_name}' in database '{self.db_name}'",
                   f"Table '{table_name}' is not exists in database '{self.db_name}'"))

        return self.Execute.execute(query, handle, ignore_list=il)

    def rename_table(self, old_name, new_name):
        # 修改表名

        query = f"ALTER TABLE '{old_name}' RENAME TO '{new_name}'"

        handle = f"Rename table '{old_name}' to '{new_name}' in database '{self.db_name}'"

        il = IgnoreList(
            Ignore(
                "no such table",
                f"Rename table '{old_name}' to '{new_name}' in database '{self.db_name}'",
                f"Table '{old_name}' is not exists in database '{self.db_name}'", ),
            Ignore(
                "there is already another table or index with this name",
                f"Rename table '{old_name}' to '{new_name}' in database '{self.db_name}'",
                f"Table '{new_name}' is already exists in database '{self.db_name}'", ),
        )
        return self.Execute.execute(query, handle, ignore_list=il)

    def get_table_all(self):
        # 获取所有表名
        query = "SELECT tbl_name FROM sqlite_master WHERE type='table'"

        handle = f"Get all tables from '{self.db_name}'"

        return self.Execute.execute(query, handle, fetchall=True)

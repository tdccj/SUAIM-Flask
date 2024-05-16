# coding = utf-8
from datetime import datetime
import sqlite3
import time

#   ——————————————————————————————————————————————————————————
#     DatabaseX 将重构并解决 Database 的低可靠性问题，将提供 容错、验证、
#   备份、恢复、日志记录等功能。
#   ——————————————————————————————————————————————————————————

from src.DBX.Table import Table
from src.DBX.Item import Item
from src.Execute import ExeTools, Query
from src.Logger import logger


class DBX(Table, Item):
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

        self.db_info_columns = ["name", "another_name", "version", "ascription", "create_time", "close_time", "remark"]

        self.Execute = ExeTools(self.conn, self.log)

        # 将 init 后的静态对象传给父类，避免重复初始化
        Table.__init__(self, self.columns, self.Execute, self.db_name)
        Item.__init__(self, self.columns, self.Execute, self.db_name)

        # 用于管理数据库信息
        self.db_info = self._manager_db_info()

    def result(self):
        # 获取 connect(init) 后的返回值
        return self.db_info

    def __del__(self):
        # todo 更新关闭时间
        self.conn.commit()
        self.conn.close()
        self.log.debug(f"Close database '{self.db_name}' successfully")

    def _create_db_info(self):
        # 创建服务器信息表
        return self.create_table(
            "db_info",
            Query('''CREATE TABLE 'db_info' (
                    name    TEXT    PRIMARY KEY ,
                    another_name TEXT    NOT NULL UNIQUE,
                    version  TEXT    NOT NULL,
                    ascription TEXT    NOT NULL,
                    create_time     TEXT    NOT NULL,
                    close_time     TEXT,
                    remark     TEXT
                )''')
        )

    def _manager_db_info(self):
        tables = self.get_table_all()

        status = False

        if ('db_info',) not in tables["result"]:
            self.log.info(f"Database '{self.db_name}' db_info table not found")
            # 创建数据库信息表
            create = self._create_db_info()
            if create["status"] == "success":
                self.log.debug(f"Database '{self.db_name}' db_info table creation successfully")
                tables = self.get_table_all()
                # 如果创建成功，则初始化数据库信息
                self._init_db_info(self.db_name)
            if ('db_info',) not in tables["result"]:
                self.log.warning(f"Database '{self.db_name}' db_info table creation failed")
            else:
                self.log.debug(f"Database '{self.db_name}' db_info table successfully found")
                status = True

        else:
            self.log.debug(f"Database '{self.db_name}' db_info table successfully found")
            status = True

        return self.get_items("db_info", None)

    def _init_db_info(self, db_name: str, db_another_name: str = None, ascription: str = "Default user"):
        if db_another_name is None:
            another_name = db_name
        else:
            another_name = db_another_name

        info = vars(DBInfo(db_name, another_name, "SUAIM-DBX-1.0", ascription))
        # self.create_item("db_info", dict(zip(self.db_info_columns)))
        # todo 等待应用DBInfo，记得自动预先生成
        self.create_item("db_info", info)


class DBInfo:
    def __init__(self,
                 name: str,
                 another_name: str,
                 version: str,
                 ascription: str,
                 create_time: str = int(datetime.timestamp(datetime.utcnow())),
                 close_time: str = None,  # 上一次正确关闭的时间
                 remark: str = None):
        self.name = name
        self.another_name = another_name
        self.version = version
        self.ascription = ascription
        self.create_time = create_time
        self.close_time = close_time
        self.remark = remark

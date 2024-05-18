# coding = utf-8
from datetime import datetime

from src.DBX.Item import Item
from src.DBX.Table import Table
from src.Execute import Query
from src.Logger import logger


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


class DBInfoManager:
    def __init__(self, table: Table, item: Item, db_name: str, log: logger):
        self.table = table
        self.item = item
        self.db_name = db_name
        self.log = log
        self.db_info_columns = ["name", "another_name", "version", "ascription", "create_time", "close_time",
                                "remark"]

    def create_table(self):
        # 创建服务器信息表
        return self.table.create_table(
            "db_info",
            Query('''CREATE TABLE 'db_info' (
                    id INTEGER    PRIMARY KEY AUTOINCREMENT,
                    name    TEXT    NOT NULL ,
                    another_name TEXT    NOT NULL,
                    version  TEXT    NOT NULL,
                    ascription TEXT    NOT NULL,
                    create_time     TEXT    NOT NULL,
                    close_time     TEXT,
                    remark     TEXT
                )''')
        )

    def manager_info(self):
        tables = self.table.get_table_all()

        status = False

        if ('db_info',) not in tables["result"]:
            self.log.info(f"Database '{self.db_name}' db_info table not found")
            # 创建数据库信息表
            create = self.create_table()
            if create["status"] == "success":
                self.log.debug(f"Database '{self.db_name}' db_info table creation successfully")
                tables = self.table.get_table_all()
                # 如果创建成功，则初始化数据库信息
                self.create_info(self.db_name)
            if ('db_info',) not in tables["result"]:
                self.log.warning(f"Database '{self.db_name}' db_info table creation failed")
            else:
                self.log.debug(f"Database '{self.db_name}' db_info table successfully found")
                status = True

        else:
            self.log.debug(f"Database '{self.db_name}' db_info table successfully found")
            status = True

        return self.item.get_items("db_info", None)

    def create_info(self, db_another_name: str = None, ascription: str = "Default user"):
        if db_another_name is None:
            another_name = self.db_name
        else:
            another_name = db_another_name

        info = vars(DBInfo(self.db_name, another_name, "SUAIM-DBX-0.1", ascription))

        return self.item.create_item("db_info", info)

    def get_latest_info(self):
        info = self.item.get_items("db_info", None)
        if info["status"] == "success":
            info["message"] = "Get the latest database information successfully"
            info["result"] = info["result"][-1]
        return info

    def update_latest_info(self, info: DBInfo):
        info = vars(info)
        index = self.get_latest_info()["result"][0]
        return self.item.update_item("db_info", index, list(info.keys()), list(info.values()))

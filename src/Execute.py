# coding = utf-8
from sqlite3 import Connection

from src import Logger


# ------------------------------
# Execute 模块用于 DBX 数据库操作，
# 尤其是简化 DBX 的异常处理步骤。
# ------------------------------


def execute(conn: Connection, query: str, handle: str, log: Logger, commit: bool = False, ignore: list = None):
    # 执行查询语句    query
    # 方法名    handle
    # 提交事务  commit=True
    # 忽略的异常类型   ignore
    try:

        conn.cursor().execute("")

        conn.commit()  # 提交

        self.log.debug(f"Create to table '{table_name}' successfully")

        return {"status": "success", "message": f"Create table '{table_name}' successfully"}

    except sqlite3.OperationalError as ex:
        if "already exists" in str(ex):
            self.log.info(f"Create table '{table_name}' failed , Because '{ex}'")
            return {"status": "failed", "message": f"Table '{table_name}' is already exists"}
        else:
            self.log.warning(f"Create table '{table_name}' failed , Because '{ex}'")
            return {"status": "failed", "message": f"Create table {table_name} failed"}

# coding = utf-8
import sqlite3
from sqlite3 import Connection

from src import Logger


# ------------------------------
# Execute 模块用于 DBX 数据库操作，
# 尤其是简化 DBX 的异常处理步骤。
# ------------------------------


class Ignore:
    def __init__(self, name: str, handle: str, message: str):
        self.name = name
        self.handle = handle
        self.message = message


class IgnoreList:
    def __init__(self, *args: Ignore):
        self.ignore = args


def execute(conn: Connection, query: str, handle: str, log: Logger, commit: bool = False,
            ignores: IgnoreList = None):
    # 执行查询语句    query
    # 方法名    handle
    # 提交事务  commit=True
    # 忽略的异常类型   ignore = [{type,handle,message}]
    try:

        conn.cursor().execute("")

        conn.commit()  # 提交

        log.debug(f"'{handle}' successfully")

        return {"status": "success", "message": f"{handle} successfully"}

    except sqlite3.OperationalError as ex:
        if ignores is not None:
            for i in ignores.ignore:
                if i.name in str(ex):
                    log.info(f"'{i.handle}' failed , Because '{ex}'")
                    return {"status": "failed", "message": f"'{i.message}'"}
                else:
                    log.waring(f"'{i.handle}' failed , Because '{ex}'")
                    return {"status": "failed", "message": f"{handle} failed"}
        else:
            log.waring(f"'{handle}' failed , Because '{ex}'")
            return {"status": "failed", "message": f"{handle} failed"}

# if __name__ == '__main__':
#     a = Ignore("1", "2", "3")
#     b = Ignore("11", "22", "33")
#     c = IgnoreList(a, b).ignore
#     for i in c:
#         print(i.name)

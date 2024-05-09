# coding = utf-8
import sqlite3
from sqlite3 import Connection

from src import Logger


# ------------------------------
# Execute 模块用于 DBX 数据库操作，
# 尤其是简化 DBX 的异常处理步骤。
# ------------------------------

class Response:
    def __init__(self, status: str, message: str, result: dict = None):
        self.status = status
        self.message = message
        self.result = result


class Ignore:
    def __init__(self, name: str, handle: str, message: str):
        self.name = name    # 报错中含有的名称特征
        self.handle = handle    # 用于日志记录的自定义方法名
        self.message = message  # 自定义返回信息


class IgnoreList:
    def __init__(self, *args: Ignore):
        self.ignore = args


class Execute:
    def __init__(self, conn: Connection, log: Logger):
        self.conn = conn
        self.log = log

    @staticmethod
    def __judge_fetchall(fetchall: bool, response: dict, fetch: dict):
        if fetchall is True:
            response.update(fetch)
            return response
        else:
            return response

    def execute(self,
                query: str,  # 查询语句
                handle: str,  # 自定义方法名
                commit: bool = False,  # 是否提交事务
                ignores: IgnoreList = None,  # 忽略的异常类型
                fetchall: bool = False,  # 是否有查询结果需要返回
                enable: bool = True,  # 是否执行查询语句（或仅作为输出标准化）
                ):
        # 在使用 enable = False 将函数用作标准输出时，
        # 需要传入 query = "" ，以避免出现异常。

        try:
            fetch = None
            if enable is True:
                fetch = self.conn.cursor().execute(query).fetchall()

            if commit is True:
                self.conn.commit()  # 提交

            self.log.debug(f'{handle} successfully')

            return self.__judge_fetchall(
                fetchall,
                {"status": "success", "message": f"{handle} successfully"},
                {"result": fetch})

        except sqlite3.OperationalError as ex:
            if ignores is not None:
                for i in ignores.ignore:
                    if i.name in str(ex):
                        self.log.info(f"{i.handle} failed , Because '{ex}'")
                        return {"status": "failed", "message": f"{i.message}"}

                    self.log.warning(f"{i.handle} failed , Because '{ex}'")
                return {"status": "failed", "message": f"{handle} failed"}
            else:
                self.log.warning(f"{handle} failed , Because '{ex}'")
                return {"status": "failed", "message": f"{handle} failed"}

# if __name__ == '__main__':
#     a = Ignore("1", "2", "3")
#     b = Ignore("11", "22", "33")
#     c = IgnoreList(a, b).ignore
#     for i in c:
#         print(i.name)

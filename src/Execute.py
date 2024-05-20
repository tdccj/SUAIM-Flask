# coding = utf-8
import sqlite3
from sqlite3 import Connection
from typing import Union

from src import Logger
from src.ErrorType import ReturnError


# -----------------------------------------
# Execute 模块用于在执行时提供异常处理和日志记录，
# 并提供标准化类对象。
# 尤其是简化 DBX 的异常处理步骤。
# -----------------------------------------


class ExeWrapper:
    # 通用函数装饰器，用于异常处理和记录log
    def __init__(self, name: str, log: Logger = None):
        self.name = name
        self.log = Logger.logger(self.name) if log is None else log

    def try_execute(self, func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                self.log.debug(f"{self.name} func {func.__module__}.{func.__name__}() is successfully,"
                               f" Parameter args:{args}, kwargs:{kwargs}")
                return res
            except ReturnError as e:
                self.log.warning(f"{self.name} func {func.__module__}.{func.__name__}() is failed,"
                                 f" Because '{e}', Parameter args:{args}, kwargs:{kwargs}")
                return ExeTools.standard_output(False,
                                                f"{self.name} func {func.__module__}.{func.__name__}() is",
                                                reason="Invalid return value, Maybe there is no found")
            except Exception as e:
                self.log.warning(f"{self.name} func {func.__module__}.{func.__name__}() is failed,"
                                 f" Because '{e}', Parameter args:{args}, kwargs:{kwargs}")
                return ExeTools.standard_output(False,
                                                f"{self.name} func {func.__module__}.{func.__name__}() is")

        # 将原函数名赋给装饰器函数，防止 flask 报错
        wrapper.__name__ = func.__name__

        return wrapper


class Limit:
    # 用于标准化传入 limit 截取范围
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class ItemData:
    # 用于标准化传入单条item数据
    def __init__(self,
                 name: str,
                 item_type: str,
                 quantity: float,
                 ascription: str,
                 tag: str = None,
                 price: float = None,
                 consumables: str = None,
                 remark: str = None):
        self.name = name
        self.type = item_type
        self.quantity = quantity
        self.ascription = ascription
        self.tag = tag
        self.price = price
        self.consumables = consumables
        self.remark = remark

        self.values = (name, item_type, quantity, ascription, tag, price, consumables, remark)


class Query:
    def __init__(self, command: str, values: tuple = None):
        # 为 Execute.execute 添加 query 的 values: tuple 支持，
        # 用以传入查询附加参数，防止 sql 注入
        # 示例：Query(query, (id_db,))
        self.command = command
        self.values = values


class Response:
    def __init__(self, status: str, message: str, result: dict = None):
        self.status = status
        self.message = message
        self.result = result


class Ignore:
    def __init__(self, feature: str, handle: str, message: str):
        self.feature = feature  # 报错中含有的要忽略的特征
        self.handle = handle  # 用于日志记录的自定义方法名
        self.message = message  # 自定义返回信息


class IgnoreList:
    def __init__(self, *args: Ignore):
        self.ignore = args


class ExeTools:
    # 用于 DBX 的执行/异常处理/标准化输出
    def __init__(self, conn: Union[Connection, None], log: Logger):
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
                query: Union[str, Query],  # 查询语句
                handle: str,  # 自定义方法名
                commit: bool = False,  # 是否提交事务
                ignore_list: IgnoreList = None,  # 忽略的异常类型
                fetchall: bool = False,  # 是否有查询结果需要返回
                enable: bool = True,  # 是否执行查询语句（或仅作为输出标准化）
                ):
        # 在使用 enable = False 将函数用作标准输出时，
        # 需要传入 query = "" ，以避免出现异常。

        # 用于 enable = False 时，可以不用传入conn
        if self.conn is None and enable is True:
            return {"status": "failed", "message": f"Cannot execute query, Because 'parameter conn is None'"}

        try:
            fetch = None
            if enable is True:
                if isinstance(query, str):
                    fetch = self.conn.cursor().execute(query).fetchall()
                elif isinstance(query, Query):
                    # print(query.command)
                    if query.values is None:
                        fetch = self.conn.cursor().execute(query.command).fetchall()
                    else:
                        fetch = self.conn.cursor().execute(query.command, query.values).fetchall()

                # else:
                #     # 可能不会出现此种情况
                #     self.log.info(f"{handle} failed , Because query is '{type(query)}' "
                #                   f", Need str or Query(command,values)")
                #     return {"status": "failed", "message": f"{handle} failed result is None"}

            if commit is True:
                self.conn.commit()  # 提交

            if fetchall is True and fetch is None:
                # 防止 fetchall 返回 None
                self.log.info(f'{handle} failed , Because \'result is None\'')
                return {"status": "failed", "message": f"{handle} failed result is None"}

            elif fetchall is True and fetch == []:
                # 防止 fetchall 返回 空列表
                self.log.info(f'{handle} failed , Because \'result is Empty List\'')
                return {"status": "failed", "message": f"{handle} failed result is Empty List"}

            else:
                self.log.debug(f'{handle} successfully')

                return self.__judge_fetchall(
                    fetchall,
                    {"status": "success", "message": f"{handle} successfully"},
                    {"result": fetch})

        except sqlite3.OperationalError as ex:
            if ignore_list is not None:
                for i in ignore_list.ignore:
                    if i.feature in str(ex):
                        self.log.info(f"{i.handle} failed , Because '{ex}'")
                        return {"status": "failed", "message": f"{i.message}"}

                    self.log.warning(f"{i.handle} failed , Because '{ex}'")
                return {"status": "failed", "message": f"{handle} failed"}
            else:
                self.log.warning(f"{handle} failed , Because '{ex}'")
                return {"status": "failed", "message": f"{handle} failed"}

    @staticmethod
    def standard_output(status: bool,
                        handle: str,
                        result=None,
                        log: Logger = None,
                        reason: str = None):
        res = {"status": ("success" if status else "failed"),
               "message": (handle + " successfully" if status else handle + " failed")}

        if result is not None:
            res["result"] = result

        if log is not None:
            log.debug(res["message"])

        if status is False and reason is not None:
            res["message"] += f", Because '{reason}'"

        return res

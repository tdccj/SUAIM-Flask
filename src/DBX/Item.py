# coding = utf-8
from typing import Union

from src import Logger
from src.Execute import (
    ExeTools,
    Query,
    IgnoreList,
    Ignore,
    ItemData,
    Limit
)


class Item:

    def __init__(self, columns: list, execute: ExeTools, db_name: str, log: Logger):
        self.columns = columns
        self.Execute = execute
        self.db_name = db_name
        self.log = log

    def get_item_data(self, table_name: str, item_id: int, index: str = "id"):
        # 查看某行数据，默认根据id

        query = f"SELECT * FROM '{table_name}' WHERE {index} = ?"

        handle = f"Get an item {item_id} data from table '{table_name}' in database '{self.db_name}'"

        # ignore = Ignore("")

        res = self.Execute.execute(
            Query(query, (item_id,)),
            handle,
            fetchall=True
        )

        return res

    def create_item(self, table_name: str, item: Union[ItemData, dict]):
        # 创建新物品
        if isinstance(item, ItemData):
            query = \
                f"INSERT INTO '{table_name}' (name,type,quantity,ascription,tag,price,consumables,remark) " \
                f"VALUES (?, ?, ?, ?, ?, ?, ?, ?);"

            handle = f"Create an standard item '{item.name}' from table '{table_name}' in database '{self.db_name}'"

            values = item.values
        else:
            values = tuple(item.values())

            q_values = ",".join(tuple(["?" for _ in item.values()]))

            fields = ",".join(tuple(item.keys()))

            query = \
                f"INSERT INTO '{table_name}' ({fields}) " \
                f"VALUES ({q_values});"

            handle = f"Create an item '{item}' from table '{table_name}' in database '{self.db_name}'"

            # print(query, values)

        res = self.Execute.execute(
            Query(query, values),
            handle,
            commit=True,
        )

        if res["status"] == "success":
            res1 = self.Execute.execute(
                "SELECT last_insert_rowid();",
                "Get the last inserted row id",
                fetchall=True,
                commit=True
            )
            res["result"] = res1["result"]

        return res

    def delete_item(self, table_name: str, id_db: int, real: bool = False):
        # 删除项，默认为软删除即标记删除，而非实质性删除，以提供容错性
        if real:
            query = Query(
                f"DELETE from '{table_name}' WHERE id = ?", (id_db,)
            )
            handle = f"Hard-Delete an item {id_db} from table '{table_name}' in database '{self.db_name}'"
        else:
            query = Query(f"UPDATE '{table_name}' SET show = 0 WHERE id = ?",
                          (id_db,))
            handle = f"Soft-delete an item {id_db} from table '{table_name}' in database '{self.db_name}'"

        return self.Execute.execute(query, handle, commit=True)

    def update_item(self, table_name: str, item_id: int, column_name: Union[str, list],
                    value: Union[str, int, float, bool, list], index: str = "id"):
        # 更新（修改）item项的特定数据

        query = f"UPDATE '{table_name}' SET '{column_name}' = ? WHERE {index} = ?"
        values = (value, item_id)

        # 用于处理传入为列表的情况
        if isinstance(column_name, list) and isinstance(column_name, list):
            if len(column_name) != len(value):
                res = self.Execute.execute(
                    "",
                    f"Update column '{column_name}' to value '{value}' for the item {item_id} "
                    f"in the table '{table_name}' database '{self.db_name}'")
                res["status"] = "failed"
                res["message"] = (
                        (f"Update column '{column_name}' to value '{value}' for the item {item_id} in the table "
                         f"'{table_name}' database '{self.db_name}'") +
                        "Because 'column_name and value is a list, but the length of them is not equal'")
                return res

            column_name = '"' + '" = ? ,"'.join(column_name) + '" = ?'
            values = tuple(value) + (item_id,)
            query = f"UPDATE '{table_name}' SET {column_name} WHERE {index} = ?"
        elif isinstance(column_name, str) or isinstance(column_name, tuple):
            res = self.Execute.execute(
                "",
                f"Update column '{column_name}' to value '{value}' for the item {item_id} "
                f"in the table '{table_name}' database '{self.db_name}'", enable=False)
            res["status"] = "failed"
            res["message"] = (
                    (f"Update column '{column_name}' to value '{value}' for the item {item_id} in the table "
                     f"'{table_name}' database '{self.db_name}'") +
                    "Because 'If one of column_name and value is a list, then the other must be a list as well'")
            return res

        info = self.get_item_data(table_name, item_id, index)

        # 判断是否存在有该 item
        if info["status"] == "success":
            res = self.Execute.execute(
                Query(
                    query,
                    values
                ),
                f"Update column '{column_name}' to value '{value}' for the item {item_id} "
                f"in the table '{table_name}' database '{self.db_name}'",
                commit=True
            )
            return res

        else:
            info["message"] = f"Not found item {item_id} from table '{table_name}' in database '{self.db_name}'"
            return info

    def get_items(self, table_name: str, limit: Union[Limit | None] = Limit(0, 100)):
        # 获取某个表的所有项
        res = self.Execute.execute(
            f"SELECT * FROM '{table_name}'",
            f"Get all items from table '{table_name}' in database '{self.db_name}'",
            fetchall=True,
            ignore_list=IgnoreList(
                Ignore("no such table",
                       f"Get all items from table '{table_name}' in database '{self.db_name}'",
                       f"No such table '{table_name}'"),
            ),

        )

        if limit is not None and res["status"] == "success":
            res["result"] = res["result"][limit.start:limit.end]
            res["message"] = f"Get {len(res['result'])} items from table '{table_name}' in database '{self.db_name}'"

        return res

    def count_item(self, table_name: str):
        # 统计表内总项数
        return self.Execute.execute(
            f"SELECT COUNT(*) FROM '{table_name}'",
            f"Count all items from table '{table_name}' in database '{self.db_name}'",
            fetchall=True
        )

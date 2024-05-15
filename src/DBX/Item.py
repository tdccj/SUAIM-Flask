# coding = utf-8
from typing import Union

from src.Execute import (
    ExeTools,
    Query,
    IgnoreList,
    Ignore,
    ItemData,
    Limit
)


class Item:

    def __init__(self, columns: list, execute: ExeTools, db_name: str):
        self.columns = columns
        self.Execute = execute
        self.db_name = db_name

    def get_item_data(self, table_name: str, item_id: int, ):
        # 根据id查看某行数据

        query = f"SELECT * FROM '{table_name}' WHERE id = ?"

        handle = f"Get an item {item_id} data from table '{table_name}' in database '{self.db_name}'"

        # ignore = Ignore("")

        res = self.Execute.execute(
            Query(query, (item_id,)),
            handle,
            fetchall=True
        )

        return res

    def create_item(self, table_name: str, item: ItemData):
        # 创建新物品
        query = \
            f"INSERT INTO '{table_name}' (name,type,quantity,ascription,tag,price,consumables,remark) " \
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?);"

        values = item.values

        res = self.Execute.execute(
            Query(query, values),
            f"Create an item '{item.name}' from table '{table_name}' in database '{self.db_name}'",
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

    def update_item(self, table_name: str, item_id: int, column_name: str, value: Union[str, int, float, bool]):
        # 更新（修改）item项的特定数据

        info = self.get_item_data(table_name, item_id)

        if info["status"] == "success":
            # 判断是否存在有该 item
            res = self.Execute.execute(
                Query(
                    f"UPDATE '{table_name}' SET '{column_name}' = ? WHERE id = ?",
                    (value, item_id)
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


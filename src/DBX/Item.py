# coding = utf-8

from src.Execute import Execute, Ignore, IgnoreList, Query


class Item:

    def __init__(self, columns: list, execute: Execute, db_name: str):
        self.columns = columns
        self.Execute = execute
        self.db_name = db_name

    # 根据id查看某行数据
    def get_item_data(self, table_name: str, item_id: int, ):
        query = f"SELECT * FROM {table_name} WHERE id = ?"

        handle = f"Get a item {item_id} data from table '{table_name}' in '{self.db_name}'"

        # ignore = Ignore("")

        res = self.Execute.execute(
            Query(query, (item_id,)),
            handle,
            fetchall=True
        )

        return res

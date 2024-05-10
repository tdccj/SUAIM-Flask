# coding = utf-8

from src.Execute import Execute, Query


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


class Item:

    def __init__(self, columns: list, execute: Execute, db_name: str):
        self.columns = columns
        self.Execute = execute
        self.db_name = db_name

    def get_item_data(self, table_name: str, item_id: int, ):
        # 根据id查看某行数据

        query = f"SELECT * FROM '{table_name}' WHERE id = ?"

        handle = f"Get a item {item_id} data from table '{table_name}' in '{self.db_name}'"

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
            f"Create a item '{item.name}' in database '{self.db_name}' table '{table_name}'",
            commit=True,
        )

        if res["status"] == "success":
            res1 = self.Execute.execute(
                "SELECT last_insert_rowid();",
                "Get the last inserted row id",
                fetchall=True
            )
            res["result"] = res1["result"]

        return res

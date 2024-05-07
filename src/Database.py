# coding = utf-8

# 这个库用来操作sqlite3数据库
import sqlite3
import warnings

tableName = ""


class DB:
    def __init__(self, path):
        warnings.warn("此方法已废弃，不推荐使用，等待重构为DatabaseX", DeprecationWarning)

        self.path = "../database/" + path

        self.conn = sqlite3.connect(self.path)  # 连接数据库
        print("数据库连接成功")
        self.cursor = self.conn.cursor()  # 创建游标

        self.columns = ["id", "name", "type", "tag", "quantity", "price", "consumables", "remark", "ascription"]

    def get_normal_columns(self):
        return self.columns

    # 连接列表
    def connect_table(self, table_name):
        global tableName
        tableName = table_name

        # 必填包括：name、type、quantity、ascription
        try:
            self.cursor.execute(f'''CREATE TABLE {table_name}(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            type        TEXT    NOT NULL,
            tag         TEXT,
            quantity    REAL    NOT NULL,
            price       REAL,
            consumables TEXT,   
            remark      TEXT,
            ascription  TEXT    NOT NULL
            
            
            );''')
            #   name        名称
            #   type        类型
            #   tag         标签
            #   quantity    数量
            #   price       价值
            #   consumables 是否为消耗品(消耗品周期)
            #   remark      备注
            #   ascription  归属人

            self.conn.commit()  # 提交
            print("表单创建成功")

        except sqlite3.OperationalError as ex:
            print(f"创建失败:{ex}", "\n*报错重名可以无视")

        # # 查看所有表单
        # self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")
        #
        # print(self.cursor.fetchall())  # 获取返回

        # # 查询所有列名（查询第一行）
        # self.cursor.execute(f"SELECT * FROM {tableName}")
        # name_list = [i[0] for i in self.cursor.description]
        # print(name_list)

    # 创建新物品
    def create_item(self, name: str, item_type: str, quantity: float, ascription: str, tag: str = None,
                    price: float = None,
                    consumables: str = None, remark: str = None):
        query = \
            f"INSERT INTO {tableName} (name,type,quantity,ascription,tag,price,consumables,remark) " \
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        values = (name, item_type, quantity, ascription, tag, price, consumables, remark)
        self.cursor.execute(query, values)
        self.conn.commit()

        # 查询结果
        self.cursor.execute(f"SELECT * FROM {tableName} WHERE name=?", (name,))
        # 传入元组是因为sqlite用迭代处理WHRER
        # 只查询一个元素必须传入只有一个元素的元组

        self.cursor.execute("SELECT last_insert_rowid();")
        row_id = self.cursor.fetchone()
        print(row_id)
        return row_id

    # 更新（修改）物品数据
    def update_item(self, column_name, id_db: int, data):
        self.cursor.execute(F"UPDATE {tableName} SET {column_name} = ? WHERE id = {id_db}", (data,))
        self.conn.commit()

    # 删除物品数据
    def delete_item(self, id_db: int):
        self.cursor.execute(f"DELETE from {tableName} WHERE id = {id_db}")
        self.conn.commit()

    # 删除表   谨慎操作！！
    def delete_table(self, db_table):
        self.cursor.execute(f"DROP TABLE {db_table};")

    # 修改表名
    def rename_table(self, old_name, new_name):
        try:
            self.cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
            return "success"
        except sqlite3.OperationalError as EX:
            print("error:", EX)
            return EX

    # 查看所有表
    def get_table_all(self):
        self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")
        return self.cursor.fetchall()

    # 查看表内的查看所有数据
    def get_item_all(self):
        self.cursor.execute(f"SELECT * FROM {tableName}")
        _fetch = self.cursor.fetchall()
        print(_fetch)
        return _fetch

    # 根据id查看某行数据
    def get_item_data(self, id_db: int):
        self.cursor.execute(f"SELECT * FROM {tableName} WHERE id = ?", (id_db,))
        _fetch = self.cursor.fetchone()
        print(_fetch)
        return _fetch

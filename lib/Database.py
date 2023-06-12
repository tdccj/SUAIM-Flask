# coding = utf-8
import sqlite3

tableName = ""


class DB:
    def __init__(self, path):
        self.path = path

        self.conn = sqlite3.connect(self.path)  # 连接数据库
        print("数据库连接成功")
        self.cursor = self.conn.cursor()  # 创建游标

    # 创建列表
    def create_table(self, table_name):
        global tableName
        tableName = table_name

        try:
            self.cursor.execute(f'''CREATE TABLE {table_name}(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            type        TEXT    NOT NULL,
            tag         TEXT,
            quantity    REAL    NOT NULL,
            price       REAL,
            consumables TEXT,   
            remark      TEXT
            
            
            );''')
            #   name        名称
            #   type        类型
            #   tag         标签
            #   quantity    数量
            #   price       价值
            #   consumables 是否为消耗品
            #   remark      备注

            self.conn.commit()  # 提交
            print("表单创建成功")

        except sqlite3.OperationalError as ex:
            print(f"创建失败:{ex}")

        # 查看所有表单
        self.cursor.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")

        print(self.cursor.fetchall())  # 获取返回

        # 查询所有列名（查询第一行）
        self.cursor.execute(f"SELECT * FROM {table_name}")
        name_list = [i[0] for i in self.cursor.description]
        print(name_list)

    # 创建新物品
    def create_item(self, name: str, item_type: str, quantity: float, tag: str = None, price: float = None,
                    consumables: str = None, remark: str = None):
        query = \
            f"INSERT INTO {tableName} (name,type,quantity,tag,price,consumables,remark) VALUES (?, ?, ?, ?, ?, ?, ?);"
        values = (name, item_type, quantity, tag, price, consumables, remark)
        self.cursor.execute(query, values)
        self.conn.commit()

        # 查询结果
        self.cursor.execute(f"SELECT * FROM {tableName} WHERE name=?", (name,))
        # 传入元组是因为sqlite用迭代处理WHRER
        # 只查询一个元素必须传入只有一个元素的元组
        print(self.cursor.fetchone())

    def show_data_all(self):
        self.cursor.execute(f"SELECT * FROM {tableName}")
        print(self.cursor.fetchall())


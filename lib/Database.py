# coding = utf-8
import sqlite3


class DB:
    def __init__(self, path):
        self.table = []
        self.table_names = []
        self.path = path
        self.conn = sqlite3.connect(self.path)  # 连接数据库
        print("数据库连接成功")
        self.cursor = self.conn.cursor()    # 创建游标

    def create(self, table_name):
        try:
            self.cursor.execute(f'''CREATE TABLE {table_name}(
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
        self.table_names = self.cursor.fetchall()   # 获取返回
        print(self.table_names)

        # 查询所有列名（查询第一行）
        self.cursor.execute(f"SELECT * FROM {table_name}")
        self.table = self.cursor.fetchall()
        print(self.table)

# coding = utf-8
import qrcode
from lib.Database import DB


# 这个库用于扫描


class SC:
    def __init__(self, _db, _table):
        self.db = DB(_db)
        self.db.create_table(_table)

    def create_code(self, _db, _table, _id):
        _text = f"SUAIM/{_db}/{_table}" + str(self.db.show_data_id(_id)[:-2]+(self.db.show_data_id(_id)[-1],))
        _img = qrcode.make(_text)
        with open("qrcode.png", "wb") as q:
            _img.save(q)

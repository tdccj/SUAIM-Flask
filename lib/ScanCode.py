# coding = utf-8
import qrcode
from lib.Database import DB


# 这个库用于扫描


class SC:
    def __init__(self, _db, _table):
        self.db = DB(_db)
        self.db.create_table(_table)

    # 创建二维码
    def create_code(self, _db, _table, _id):
        _text = f"SUAIM/{_db}/{_table}" + str(self.db.show_data_id(_id)[:-2] + (self.db.show_data_id(_id)[-1],))

        # 创建实例
        qr = qrcode.QRCode(version=2,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=200,
                           border=4)
        # 添加文本
        qr.add_data(_text)
        # 创建qrcode
        qr.make(fit=True)
        _img = qr.make_image()
        with open("qrcode.png", "wb") as q:
            _img.save(q)

    # 创建打印标签

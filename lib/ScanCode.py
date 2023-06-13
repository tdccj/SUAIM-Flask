# coding = utf-8
from lib.Database import DB


# 这个库用于生成和扫描二维码


class SC:
    def __init__(self, _db, _table):
        # 创建数据库实例
        self.db = DB(_db)  # 连接数据库
        self.db.create_table(_table)  # 连接表

        self._img = None  # 存放生成的二维码

    # 创建二维码
    def create_code(self, _db, _table, _id):
        import qrcode
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

        # 保存qrcode
        self._img = qr.make_image()
        with open("qrcode.png", "wb") as q:
            self._img.save(q)

    # 创建打印标签
    def create_print_label(self):
        from PIL import Image, ImageFont, ImageDraw
        with open("label_template/label_template_40mm×30mm.png", "rb") as _img:
            # 加载字体
            _font = ImageFont.truetype(font='font/HarmonyOS_Sans_SC/HarmonyOS_Sans_SC_Medium.ttf', size=20)

            # 创建实例打开图片
            _label = Image.open(_img)

            # 创建可绘制对象
            _draw = ImageDraw.Draw(_label)
            # 写入多行文本
            _draw.multiline_text((200, 200), "text", fill=(0, 0, 0), font=_font)

            _label.show()

            # todo 尚未测试，并且还剩图像

# coding = utf-8
from lib.Database import DB


# 这个库用于生成和扫描二维码


class SC:
    def __init__(self, _db, _table):
        # 创建数据库实例
        self._db = DB(_db)  # 连接数据库
        self._db.connect_table(_table)  # 连接表

        self._img = None  # 存放生成的二维码

    # 创建二维码
    def create_code(self, db, table, id_db):
        import qrcode
        text = f"SUAIM/{db}/{table}" + str(self._db.get_item_info(id_db)[:-2] + (self._db.get_item_info(id_db)[-1],))

        # 创建实例
        qr = qrcode.QRCode(version=2,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=20,
                           border=4)
        # 添加文本
        qr.add_data(text)
        # 创建qrcode
        qr.make(fit=True)

        # 保存qrcode
        self._img = qr.make_image()
        with open("qrcode.png", "wb") as q:
            self._img.save(q)

    # 创建打印标签
    def create_print_label(self, text: str):
        from PIL import Image, ImageFont, ImageDraw
        with open("label_template/label_template_40mm×30mm.png", "rb") as _img:
            # 加载字体
            font = ImageFont.truetype(font='font/HarmonyOS_Sans_SC/HarmonyOS_Sans_SC_Medium.ttf', size=30)

            # 创建实例打开图片
            img_label = Image.open(_img)
            # 创建可绘制对象
            img_draw = ImageDraw.Draw(img_label)

            # 复制图片并缩放
            copy = self._img.resize((200, 200))
            img_label.paste(copy, (110, 20))

            # 将字符串转成竖排文本并写上
            # 未来可以做个横排版切换选项
            # 最多支持18个字符
            num = 0
            for i in text:
                if i.encode('UTF-8').isalpha():
                    x = 15
                    y = 28
                    x += num // 6 * 40
                    y += num % 6 * 30
                    # print(num, x, y, 1)
                    img_draw.multiline_text((x, y), i, font=font, fill=(0, 0, 0))
                elif not i.encode('UTF-8').isalpha():
                    x = 15
                    y = 28
                    x += num // 6 * 40
                    y += num % 6 * 30
                    # print(num, x, y, 2)
                    img_draw.multiline_text((x, y), i, font=font, fill=(0, 0, 0))
                num += 1

            img_label.save("print_label.png")

    def printer_label(self):
        pass

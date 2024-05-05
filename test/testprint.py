# -*- coding: utf-8 -*-
import win32ui, time
from PIL import Image, ImageWin

hDC = win32ui.CreateDC()

hDC.CreatePrinterDC('P1 Label Printer')#
hDC.StartDoc("标签名")
hDC.StartPage()


Ctime = time.strftime("%y/%m/%d %H:%M",time.localtime())

DataList = [
    [170 , 14, '编号:', {'name': '宋体', 'height': 27}],

    ]

image = Image.open('../qrcode.png')
# image = image.resize((150, 150), Image.ANTIALIAS)  # 调整二维码图像大小以适应标签尺寸
image = image.crop((0, 0, image.width -10, image.height-10))
dib = ImageWin.Dib (image)
dib.draw (hDC.GetHandleOutput (), (10, 0, 150, 150))

for data in DataList:
    font = win32ui.CreateFont(data[3])
    hDC.SelectObject(font)
    hDC.TextOut(data[0], data[1], data[2])

# hDC.DrawText(txt,(ulc_x,ulc_y,lrc_x,lrc_y),win32con.DT_LEFT)

font = win32ui.CreateFont({'name':'宋体', 'height': 22,})
hDC.SelectObject(font)

#长文本换行
fsize  = 22  # 字体大小
min_x  = 40  # X轴最小值
max_x  = 500 # X轴最大值
text_x = 90  # 字X坐标
text_y = 100 # 字Y坐标

font = win32ui.CreateFont({'name':'宋体', 'height': fsize})
hDC.SelectObject(font)

# 替换原始代码中的长文本换行部分
# hDC.TextOut(min_x, text_y, text)
# while len(text) > 0:
#     text_y += fsize
#     if text_y > max_y:
#         text_y = max_y
#         text = text[int(len(text) / 2):]
#     hDC.TextOut(min_x, text_y, text[:20])
#     text = text[20:]

hDC.EndPage()
hDC.EndDoc()

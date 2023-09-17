# 代码的编码设置为utf-8
import win32print
import win32ui
from PIL import Image, ImageWin

# 定义常量，用于GetDeviceCaps

# 水平分辨率（每英寸水平像素数）
HORZRES = 8
# 垂直分辨率（每英寸垂直像素数）
VERTRES = 10
# 逻辑像素与物理像素的缩放因子（x轴）
LOGPIXELSX = 88
# 逻辑像素与物理像素的缩放因子（y轴）
LOGPIXELSY = 90
# 物理宽度（以像素为单位）
PHYSICALWIDTH = 110
# 物理高度（以像素为单位）
PHYSICALHEIGHT = 111
# 物理偏移量（x轴）
PHYSICALOFFSETX = 112
# 物理偏移量（y轴）
PHYSICALOFFSETY = 113


# 获取打印机
print_list = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
# print(print_list)
printer_index = 0
selected_printer = print_list[printer_index]
# print(selected_printer[2])
win32print.SetDefaultPrinter(selected_printer[2])


# 定义要打印的图片文件名
file_name = "print_label.png"

# 创建一个DC对象，用于与打印机进行交互
hDC = win32ui.CreateDC()
# 创建一个打印机DC，用于操作打印机
hDC.CreatePrinterDC(selected_printer[2])
# 获取打印机可打印区域
printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
# 获取打印机尺寸
printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
# 获取打印机边距
printer_margins = hDC.GetDeviceCaps(PHYSICALOFFSETX), hDC.GetDeviceCaps(PHYSICALOFFSETY)

print(printer_size)
print(printer_margins)

# 打开图片文件
bmp = Image.open(file_name)
# 如果图片宽度大于高度，则旋转90度
# if bmp.size[0] > bmp.size[1]:
#     bmp = bmp.rotate(90)

# 计算缩放比例
ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
scale = min(ratios)

# 开始打印
hDC.StartDoc(file_name)
hDC.StartPage()

# 创建一个Dib对象，用于处理图片
dib = ImageWin.Dib(bmp)
# 计算缩放后的图片尺寸
scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
# 计算缩放后的图片位置
x1 = int((printer_size[0] - scaled_width) / 2)
y1 = int((printer_size[1] - scaled_height) / 2)
x2 = x1 + scaled_width
y2 = y1 + scaled_height
# 将图片绘制到DC上
dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

# 结束打印页
hDC.EndPage()
# 结束打印
hDC.EndDoc()
# 删除DC
hDC.DeleteDC()

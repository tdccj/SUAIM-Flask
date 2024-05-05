# coding = utf-8

# dBName = "test.db"
# dBTable = "test_table"
#
# db = DB(dBName)
# db.connect_table(dBTable)
# db.create_item("testname", "testtype", 1, "td", "tag", 1, "no", "备注")
# db.update_item("name", 1, "one")
# db.delete_item(2)
# db.get_item_all()
# db.get_item_data(3)
# sc = SC(dBName, dBTable)
# sc.create_code(dBName, dBTable, 1)
# sc.create_print_label("标签wwadwad")


# import requests
#
# url = 'http://127.0.0.1:5000/api/test.db/test_table/create_item'
# data = {'name': "名字", 'type': '类型', 'quantity': 1, 'ascription': '归属人'}
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=data, headers=headers)
# if response.status_code == 200:
#     print('User created successfully')
# else:
#     print('Failed to create user')
# print(response)


# import requests
#
# url = 'http://127.0.0.1:5000/api/test.db/test_table/1/print_label'
# data = {'text': '内容'}
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=data, headers=headers)
# if response.status_code == 200:
#     print('User created successfully')
# else:
#     print('Failed to create user')
# print(response)

# db = DB('test.db')
# db.connect_table('hi')
# print(db.get_table_all())
# db.delete_table('hi')
# print(db.get_table_all())


# import requests
#
# url = 'http://127.0.0.1:5000/api/delete/test.db/hi'
# response = requests.delete(url)
# if response.status_code == 200:
#     print('successfully')
# else:
#     print('Failed')
# print(response)


# import requests
#
# url = 'http://127.0.0.1:5000/api/delete/test.db/test_table/1'
# response = requests.delete(url)
# if response.status_code == 200:
#     print('successfully')
# else:
#     print('Failed')
# print(response)


# db = DB('test.db')
# db.connect_table('a')
# print(db.get_table_all())
# db.rename_table('a','c')
# print(db.get_table_all())


# import requests
#
# url = 'http://127.0.0.1:5000/api/rename/test.db/table'
# data = {'old_name': 'd',"new_name":'e'}
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=data, headers=headers)
# re = response.content
# print(re)

#
# import requests
#
# url = 'http://127.0.0.1:5000/api/update/test.db/test_table/4'
# data = {'column_name': 'name', "data": 'up'}
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=data, headers=headers)
# re = response.content
# print(re)

# import src.Printer as Printer
# Printer.printer("qrcode.png","test","name","type","ascription")

# import requests
#
# url = 'http://127.0.0.1:5000/api/print_label'
# data = {'qr_path': './qrcode.png', "_id": '1', "_name": '2', "_type": '3', "_ascription": '4'}
# headers = {'Content-Type': 'application/json'}
# response = requests.post(url, json=data, headers=headers)
# re = response.content
# print(re)

# import requests
#
# url = 'http://127.0.0.1:5000/api/print_label/test.db/test_table/3'
# response = requests.get(url)
# if response.status_code == 200:
#     print('successfully')
# else:
#     print('Failed')
# print(response)


# db = "test.db"
# tb = "Tracked_Vehicle_Database3"
# sc = SC(db, tb)
# sc.create_code(db, tb, 17)

# coding = utf-8
import openpyxl

xlsx_file = input("Enter the name of the file: ")
db = "SAIUM_TDhome.db"  # 数据库名称
tb = "Tracked_Vehicle_Database"    # 表名称

# open the file
wb = openpyxl.load_workbook(xlsx_file)
sheet = wb.active

# get the values and create it  em
for row in sheet.values:
    print(row[1])


# # Check table
# url = f"http://127.0.0.1:5000/api/connect/{db}/{tb}"
# response = requests.get(url)
# if response.status_code == 200:
#     print('connect_successfully')
# else:
#     print('connect_Failed')
# print(response.text)

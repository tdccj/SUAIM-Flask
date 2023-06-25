# coding = utf-8

from lib.Database import DB
from lib.ScanCode import SC

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


import requests

url = 'http://127.0.0.1:5000/api/update/test.db/test_table/4'
data = {'column_name': 'name', "data": 'up'}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
re = response.content
print(re)

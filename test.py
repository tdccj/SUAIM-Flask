# coding = utf-8

from lib.Database import DB
from lib.ScanCode import SC

dBName = "test.db"
dBTable = "test_table"

db = DB(dBName)
db.connect_table(dBTable)
db.create_item("testname", "testtype", 1, "td", "tag", 1, "no", "备注")
# db.update_item("name", 1, "one")
# db.delete_item(2)
db.get_item_all()
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


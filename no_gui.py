# coding = utf-8
import openpyxl
import requests
from urllib.parse import quote

xlsx_file = input("Enter the name of the file: ")
db = "test.db"
tb = "Tracked_Vehicle_Database3"

# open the file
wb = openpyxl.load_workbook(xlsx_file)
sheet = wb.active

# get the values and create it  em
for row in sheet.values:
    for value in row:

        # 替换空格为下划线
        value = str(value)
        value = value.replace(" ", "_")
        # 将特殊字符url编码
        value = quote(value)
        print(value)

        # 添加
        url = f'http://127.0.0.1:5000/api/create/{db}/{tb}/item'
        data = {'name': f"{value}", 'type': '元器件', 'quantity': 0, 'ascription': 'tdccj'}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print('User created successfully')
        else:
            print('Failed to create item')
        row_id = response.json()["id"][0]
        print(row_id)

        # 打印
        url = f"http://127.0.0.1:5000/api/print_label/{db}/{tb}/{row_id}"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            print('print_successfully')
        else:
            print('print_Failed')

# Check table
url = f"http://127.0.0.1:5000/api/connect/{db}/{tb}"
response = requests.get(url)
if response.status_code == 200:
    print('connect_successfully')
else:
    print('connect_Failed')
print(response.text)

# coding = utf-8
from lib.Database import DB
from flask import Flask, jsonify, request, send_file
from gevent import pywsgi
from lib.ScanCode import SC

app = Flask(__name__)

# 将默认url字符集改成utf-8，以接收中文
app.url_map.charset = 'utf-8'


# 以id查询物品信息
@app.route('/api/get/<string:db_path>/<string:db_table>/<int:item_id>', methods=['GET'])
def get_item_data(db_path, db_table, item_id):
    # 连接数据库列表并查询
    db = DB(db_path)
    db.connect_table(db_table)
    row = db.get_item_data(item_id)

    # 判断查询结果是否为空
    if row is None:
        return jsonify({'error': 'item not found'}), 404

    # 处理数据
    item_info = {'id': row[0], 'name': row[1], 'type': row[2], 'tag': row[3], 'quantity': row[4], 'price': row[5],
                 'consumables': row[6], 'remark': row[7], 'ascription': row[8]}

    # 返回响应
    return jsonify(item_info)


# 获取所有列表
@app.route('/api/get/<string:db_path>/table_all', methods=['GET'])
def get_table_all(db_path):
    db = DB(db_path)
    return db.get_table_all()


# 用于获取列表内的所有数据
@app.route('/api/get/<string:db_path>/<string:db_table>/all_data', methods=['GET'])
def get_all_data(db_path, db_table):
    # 连接并查询
    db = DB(db_path)
    db.connect_table(db_table)
    all_data = db.get_item_all()

    # 判断查询结果是否为空
    if all_data is None:
        return jsonify({'error': 'data not found in this table'}), 404
    print(all_data)

    return jsonify(all_data)


# 获取QRCode
@app.route('/api/get/<string:db_path>/<string:db_table>/<int:db_id>/qrcode', methods=['GET'])
def get_qrcode(db_path, db_table, db_id):
    # 创建qrcode
    sc = SC(db_path, db_table)
    sc.create_code(db_path, db_table, db_id)

    # 读取并返回qrcode
    qrcode_path = 'qrcode.png'
    return send_file(qrcode_path, mimetype='image/jpeg')


# 创建QRCode并获取打印标签
@app.route('/api/get/<string:db_path>/<string:db_table>/<int:db_id>/print_label', methods=['POST'])
def create_print_label(db_path, db_table, db_id):
    # 从json中获取字符
    data = request.get_json()
    text = data['text']

    # 创建qrcode
    sc = SC(db_path, db_table)
    sc.create_code(db_path, db_table, db_id)
    sc.create_print_label(text)

    # 读取并返回print_label
    label_path = 'print_label.png'
    return send_file(label_path, mimetype='image/jpeg')


# 连接或创建数据库
@app.route('/api/connect/<string:db_path>', methods=['GET'])
def connect_database(db_path):
    DB(db_path)
    return db_path


# 连接或创建表单
@app.route('/api/connect/<string:db_path>/<string:db_table>', methods=['GET'])
def connect_table(db_path, db_table):
    re = db_table
    db = DB(db_path)
    db.connect_table(db_table)
    return re


# 在表中创建新物品
@app.route('/api/create/<string:db_path>/<string:db_table>/item', methods=['POST'])
def create_item(db_path, db_table):
    # connect database
    db = DB(db_path)
    db.connect_table(db_table)

    # get data
    data = request.get_json()
    name = data['name']
    item_type = data['type']
    quantity = data['quantity']
    ascription = data['ascription']
    try:
        tag = data['tag']
        price = data['price']
        consumables = data['consumables']
        remark = data['remark']
    except KeyError:
        tag = None
        price = None
        consumables = None
        remark = None

    # create item
    db.create_item(name, item_type, quantity, ascription, tag, price, consumables, remark)
    return jsonify({'result': 'success'}), 200


# 删除表
@app.route('/api/delete/<string:db_path>/<string:db_table>', methods=['DELETE'])
def delete_table(db_path, db_table):
    print(db_path,db_table)
    db = DB(db_path)
    db.delete_table(db_table)
    return "successfully"


# 用于获取表内所有name，未完成，暂且废弃
# @app.route('/api/<string:db_path>/<string:db_table>/name', methods=['GET'])
# def get_all_name(db_path, db_table):
#     db = DB(db_path)
#     db.connect_table(db_table)
#     all_name = db.get_item_all()


if __name__ == '__main__':
    # 设置端口并运行
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()

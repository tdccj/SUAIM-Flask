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


# 连接或创建表单，并返回内容
@app.route('/api/connect/<string:db_path>/<string:db_table>', methods=['GET'])
def connect_table(db_path, db_table):
    db = DB(db_path)
    db.connect_table(db_table)
    all_data = db.get_item_all()

    # 判断查询结果是否为空
    if all_data is None:
        return jsonify({'error': 'data not found in this table'}), 404
    print(all_data)

    return jsonify(all_data)


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
    print(db_path, db_table)
    db = DB(db_path)
    db.delete_table(db_table)
    return "successfully"


# 删除物品
@app.route('/api/delete/<string:db_path>/<string:db_table>/<int:db_id>', methods=['DELETE'])
def delete_item(db_path, db_table, db_id):
    db = DB(db_path)
    db.connect_table(db_table)
    db.delete_item(db_id)
    return "successfully"


# 修改表名
@app.route('/api/rename/<string:db_path>/table', methods=['POST'])
def rename_table(db_path):
    data = request.get_json()
    old_name = data["old_name"]
    new_name = data["new_name"]

    db = DB(db_path)
    re = db.rename_table(old_name, new_name)

    return str(re)


# 修改物品
@app.route('/api/update/<string:db_path>/<string:db_table>/<int:db_id>', methods=['POST'])
def update_item(db_path, db_table, db_id):
    # 更新数据库中的项。
    #
    # 参数:
    #   db_path - 数据库路径
    #   db_table - 数据表名称
    #   db_id - 要更新的项的ID
    #
    # 返回:   更新后的项数据
    #
    # Raises:
    #   无异常抛出。

    # 从请求的JSON数据中获取要更新的列名和数据
    column_name = request.get_json()['column_name']
    data = request.get_json()['data']

    # 连接到指定的数据库
    db = DB(db_path)

    # 连接到指定的数据表
    db.connect_table(db_table)

    # 使用给定的列名、ID和数据更新数据表中的项
    db.update_item(column_name, db_id, data)

    # 获取更新后的项数据
    item = db.get_item_data(db_id)

    # 返回更新后的项数据
    return str(item)


# 用于获取表内所有name，未完成，暂且废弃
# @app.route('/api/<string:db_path>/<string:db_table>/name', methods=['GET'])
# def get_all_name(db_path, db_table):
#     db = DB(db_path)
#     db.connect_table(db_table)
#     all_name = db.get_item_all()


# # 用于获取列表内的所有数据 已废弃，被connect_table取代
# @app.route('/api/get/<string:db_path>/<string:db_table>/all_data', methods=['GET'])
# def get_all_data(db_path, db_table):
#     # 连接并查询
#     db = DB(db_path)
#     db.connect_table(db_table)
#     all_data = db.get_item_all()
#
#     # 判断查询结果是否为空
#     if all_data is None:
#         return jsonify({'error': 'data not found in this table'}), 404
#     print(all_data)
#
#     return jsonify(all_data)


if __name__ == '__main__':
    # 设置端口并运行
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()

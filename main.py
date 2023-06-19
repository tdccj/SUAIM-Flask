# coding = utf-8
from lib.Database import DB
from flask import Flask, jsonify, request, send_file
from gevent import pywsgi
from lib.ScanCode import SC

app = Flask(__name__)


# 以id查询物品信息
@app.route('/api/<string:db_path>/<string:db_table>/<int:item_id>', methods=['GET'])
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


# 用于获取列表内的所有数据
@app.route('/api/<string:db_path>/<string:db_table>', methods=['GET'])
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


# 用于获取表内所有name，未完成，暂且废弃
# @app.route('/api/<string:db_path>/<string:db_table>/name', methods=['GET'])
# def get_all_name(db_path, db_table):
#     db = DB(db_path)
#     db.connect_table(db_table)
#     all_name = db.get_item_all()


# 获取qrcode
@app.route('/api/<string:db_path>/<string:db_table>/<string:db_id>/get_qrcode', methods=['GET'])
def get_qrcode(db_path, db_table, db_id):
    # 创建qrcode
    sc = SC(db_path, db_table)
    sc.create_code(db_path, db_table, db_id)

    # 读取并返回qrcode
    qrcode_path = 'qrcode.png'
    return send_file(qrcode_path, mimetype='image/jpeg')


# 在表中创建新物品
@app.route('/api/<string:db_path>/<string:db_table>/create_item', methods=['POST'])
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


if __name__ == '__main__':
    # 设置端口并运行
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()

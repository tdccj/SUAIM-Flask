# coding = utf-8
import warnings

from flask import Blueprint, request, jsonify, send_file
from src.Database import DB
from src.Printer import printer
from src.ScanCode import SC

qr_bp = Blueprint('api_qrCore', __name__)


@qr_bp.route('/api/get/<string:db_path>/<string:db_table>/<int:db_id>/qrcode', methods=['GET'])
def get_qrcode(db_path, db_table, db_id):
    # 获取QRCode

    # 创建qrcode
    sc = SC(db_path, db_table)
    print(db_path, db_table, db_id)
    sc.create_code(db_path, db_table, db_id)

    # 读取并返回qrcode
    qrcode_path = '../qrcode.png'
    return send_file(qrcode_path, mimetype='image/jpeg')


@qr_bp.route('/api/get/<string:db_path>/<string:db_table>/<int:db_id>/print_label', methods=['POST'])
def create_print_label(db_path, db_table, db_id):
    # 创建QRCode并获取打印标签

    # 从json中获取字符
    data = request.get_json()
    text = data['text']

    # 创建qrcode
    sc = SC(db_path, db_table)
    sc.create_code(db_path, db_table, db_id)
    sc.create_print_label(text)

    # 读取并返回print_label
    label_path = '../print_label.png'
    return send_file(label_path, mimetype='image/jpeg')


@qr_bp.route('/api/print_label/<string:db_path>/<string:db_table>/<int:db_id>', methods=['GET'])
def print_label_simple(db_path, db_table, db_id):
    # 简单快速调用打印机打印标签

    # 创建qrcode
    sc = SC(db_path, db_table)
    sc.create_code(db_path, db_table, db_id)

    # 读取并返回qrcode
    qrcode_path = '../qrcode.png'
    # 连接数据库列表并查询
    db = DB(db_path)
    db.connect_table(db_table)
    row = db.get_item_data(db_id)

    # 判断查询结果是否为空
    if row is None:
        return jsonify({'status': 'error', 'error': 'item not found', 'def': 'print_label_simple'}), 404

    # 处理数据
    item_info = {'id': row[0], 'name': row[1], 'type': row[2], 'tag': row[3], 'quantity': row[4], 'price': row[5],
                 'consumables': row[6], 'remark': row[7], 'ascription': row[8]}
    print(item_info)

    # 调用打印机打印标签
    printer(qr_path=qrcode_path, _id=item_info['id'], _name=item_info['name'], _type=item_info['type'],
            _ascription=item_info['ascription'])
    return jsonify({'status': 'success', 'def': 'print_label_simple'}), 200

# @app.route('/api/print_label', methods=['POST'])
# def print_label():
#     # 调用打印机打印标签（暂时弃用）
#
#     warnings.warn("some_old_function is deprecated", DeprecationWarning)    # 标记过时
#
#     data = request.get_json()
#     qr_path = data['qr_path']
#     _id = data['_id']
#     _name = data['_name']
#     _type = data['_type']
#     _ascription = data['_ascription']
#
#     # 调用打印机打印标签
#     printer(qr_path=qr_path, _id=_id, _name=_name, _type=_type, _ascription=_ascription)
#     return "successfully"

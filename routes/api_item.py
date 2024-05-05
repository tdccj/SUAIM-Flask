# coding = utf-8
from flask import Blueprint, request, jsonify
from src.Database import DB

item_bp = Blueprint('api_item', __name__)


@item_bp.route('/api/get/<string:db_path>/<string:db_table>/<int:item_id>', methods=['GET'])
def get_item_data(db_path, db_table, item_id):
    # 以id查询物品信息

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
    return jsonify({'result': 'success', "data": item_info, 'def': 'get_item_data'}), 200


@item_bp.route('/api/create/<string:db_path>/<string:db_table>/item', methods=['POST'])
def create_item(db_path, db_table):
    # 在表中创建新物品

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
    row_id = db.create_item(name, item_type, quantity, ascription, tag, price, consumables, remark)
    return jsonify({'result': 'success', "id": row_id, 'def': 'create_item'}), 200


@item_bp.route('/api/delete/<string:db_path>/<string:db_table>/<int:db_id>', methods=['DELETE'])
def delete_item(db_path, db_table, row_id):
    # 删除物品
    db = DB(db_path)
    db.connect_table(db_table)
    db.delete_item(row_id)
    return jsonify({'result': 'success', "id": row_id, 'def': 'delete_item'}), 200


@item_bp.route('/api/update/<string:db_path>/<string:db_table>/<int:db_id>', methods=['POST'])
def update_item(db_path, db_table, db_id):
    # 修改物品

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

    db = DB(db_path)
    db.connect_table(db_table)

    db.update_item(column_name, db_id, data)

    # 获取更新后的项数据
    item = db.get_item_data(db_id)

    return jsonify({'result': 'success', "item": str(item), 'def': 'update_item'}), 200

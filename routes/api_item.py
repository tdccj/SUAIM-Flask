# coding = utf-8
from flask import Blueprint, request, jsonify

from src.DBX.Item import ItemData
from src.Database import DB
from src.DatabaseX import DBX

from routes.api import try_execute

item_bp = Blueprint('api_item', __name__)


@item_bp.route('/api/get/<string:db_path>/<string:db_table>/<int:item_id>', methods=['GET'])
@try_execute
def get_item_data(db_path, db_table, item_id):
    # 以id查询物品信息
    db = DBX(db_path)
    return jsonify(db.get_item_data(db_table, item_id)), 200


@item_bp.route('/api/create/<string:db_path>/<string:db_table>/item', methods=['POST'])
@try_execute
def create_item(db_path, db_table):
    # 在表中创建新物品

    # connect database
    db = DBX(db_path)

    # get data
    data = request.get_json()

    return jsonify(db.create_item(db_table, ItemData(**data))), 200


@item_bp.route('/api/delete/<string:db_path>/<string:db_table>/<int:db_id>', methods=['DELETE', 'POST'])
@try_execute
def delete_item(db_path, db_table, row_id):
    # 删除物品
    db = DBX(db_path)

    if request.method == 'POST':
        real = bool(request.get_json()["real"])
        return jsonify(db.delete_item(db_table, row_id, real)), 200

    elif request.method == 'DELETE':
        return jsonify(db.delete_item(db_table, row_id)), 200


@item_bp.route('/api/update/<string:db_path>/<string:db_table>/<int:db_id>', methods=['POST'])
@try_execute
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

    return jsonify({'status': 'success', "item": str(item), 'def': 'update_item'}), 200


@item_bp.route('/api/get/<string:db_path>/<string:db_table>/all', methods=['GET'])
@try_execute
def get_all_item(db_path, db_table):
    # 连接表单，返回所有item
    db = DB(db_path)
    db.connect_table(db_table)
    all_data = db.get_item_all()
    columns = db.get_normal_columns()

    # 判断查询结果是否为空
    if all_data is None:
        return jsonify({'error': 'data not found in this table'}), 404
    # print(all_data)

    return jsonify({'status': "success", "columns": columns,
                    "data": all_data, 'def': 'get_all_item'}), 200

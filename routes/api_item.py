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
    db = DBX(db_path)

    # 从请求的JSON数据中获取要更新的列名和数据
    column_name = request.get_json()['column_name']
    data = request.get_json()['data']

    return jsonify(db.update_item(db_table, db_id, column_name, data)), 200


@item_bp.route('/api/get/<string:db_path>/<string:db_table>/items', methods=['GET'])
@try_execute
def get_items(db_path, db_table):
    # 连接表单，返回所有item
    db = DBX(db_path)
    return jsonify(db.get_items(db_table)), 200

# coding = utf-8

from flask import Blueprint, request, jsonify
from src.DatabaseX import DBX
from routes.api import try_execute

tb_bp = Blueprint('api_table', __name__)


@tb_bp.route('/api/create/<string:db_path>/table', methods=['POST'])
@try_execute
def create_table(db_path):
    # 连接或创建表单，并返回内容

    data = request.get_json()

    db = DBX(db_path)

    return jsonify(db.table.create_table(data["table_name"])), 200


@tb_bp.route('/api/delete/<string:db_path>/<string:db_table>', methods=['DELETE'])
@try_execute
def delete_table(db_path, db_table):
    # 删除表
    db = DBX(db_path)

    return jsonify(db.table.delete_table(db_table)), 200


@tb_bp.route('/api/rename/<string:db_path>/table', methods=['POST'])
@try_execute
def rename_table(db_path):
    # 修改表名
    data = request.get_json()
    old_name = data["old_name"]
    new_name = data["new_name"]

    db = DBX(db_path)

    return jsonify(db.table.rename_table(old_name, new_name)), 200


@tb_bp.route('/api/get/<string:db_path>/all', methods=['GET'])
@try_execute
def get_table_all(db_path):
    # 获取数据库中的所有列表
    db = DBX(db_path)
    return jsonify(db.table.get_table_all()), 200


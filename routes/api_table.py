# coding = utf-8

from flask import Blueprint, request, jsonify
from src.Database import DB
from src.DatabaseX import DBX

tb_bp = Blueprint('api_table', __name__)


@tb_bp.route('/api/create/<string:db_path>/<string:db_table>', methods=['GET'])
def create_table(db_path, db_table):
    # 连接或创建表单，并返回内容
    db = DBX(db_path)
    info = db.create_table(db_table)

    return jsonify({'status': info["status"], "message": info["message"], 'table': f'{db_path}/{db_table}',
                    'def': 'create_table'}), 200


@tb_bp.route('/api/delete/<string:db_path>/<string:db_table>', methods=['DELETE'])
def delete_table(db_path, db_table):
    # 删除表
    # print(db_path, db_table)
    db = DBX(db_path)
    db.delete_table(db_table)
    return jsonify({'status': "success", 'def': 'delete_table'}), 200


@tb_bp.route('/api/rename/<string:db_path>/table', methods=['POST'])
def rename_table(db_path):
    # 修改表名
    data = request.get_json()
    old_name = data["old_name"]
    new_name = data["new_name"]

    db = DB(db_path)
    re = db.rename_table(old_name, new_name)

    return jsonify({'status': str(re), 'def': 'rename_table'}), 200


@tb_bp.route('/api/get/<string:db_path>/all', methods=['GET'])
def get_table_all(db_path):
    # 获取数据库中的所有列表
    db = DB(db_path)
    return jsonify({'status': 'success', "tables": db.get_table_all(), 'def': 'get_table_all'}), 200

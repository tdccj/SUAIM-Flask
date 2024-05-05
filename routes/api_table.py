# coding = utf-8

from flask import Blueprint, request, jsonify
from src.Database import DB

tb_bp = Blueprint('api_table', __name__)


@tb_bp.route('/api/connect/<string:db_path>/<string:db_table>', methods=['GET'])
def connect_table(db_path, db_table):
    # 连接或创建表单，并返回内容
    db = DB(db_path)
    db.connect_table(db_table)

    return jsonify({'table': f'{db_path}/{db_table}'})


@tb_bp.route('/api/get/<string:db_path>/<string:db_table>', methods=['GET'])
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

    return jsonify({"columns": columns,
                    "data": all_data})


@tb_bp.route('/api/delete/<string:db_path>/<string:db_table>', methods=['DELETE'])
def delete_table(db_path, db_table):
    # 删除表
    # print(db_path, db_table)
    db = DB(db_path)
    db.delete_table(db_table)
    return "successfully"


@tb_bp.route('/api/rename/<string:db_path>/table', methods=['POST'])
def rename_table(db_path):
    # 修改表名
    data = request.get_json()
    old_name = data["old_name"]
    new_name = data["new_name"]

    db = DB(db_path)
    re = db.rename_table(old_name, new_name)

    return str(re)

# @app.route('/api/<string:db_path>/<string:db_table>/name', methods=['GET'])
# def get_all_name(db_path, db_table):
#     用于获取表内所有name，未完成，暂且废弃

#     db = DB(db_path)
#     db.connect_table(db_table)
#     all_name = db.get_item_all()


# @app.route('/api/get/<string:db_path>/<string:db_table>/all_data', methods=['GET'])
# def get_all_data(db_path, db_table):
#     用于获取列表内的所有数据 已废弃，被connect_table取代

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

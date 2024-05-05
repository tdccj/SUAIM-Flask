# coding = utf-8
from flask import Blueprint, request, jsonify
from src.Database import DB

db_bp = Blueprint('api_database', __name__)


@db_bp.route('/api/connect/<string:db_path>', methods=['GET'])
def connect_database(db_path):
    # 连接或创建数据库
    DB(db_path)
    return jsonify(db_path)


@db_bp.route('/api/get/<string:db_path>/table_all', methods=['GET'])
def get_table_all(db_path):
    # 获取数据库中的所有列表
    db = DB(db_path)
    return jsonify(db.get_table_all())

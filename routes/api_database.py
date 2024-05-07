# coding = utf-8
from flask import Blueprint, jsonify
from src.Database import DB
from src.DatabaseX import DBX

db_bp = Blueprint('api_database', __name__)


@db_bp.route('/api/connect/<string:db_path>', methods=['GET'])
def connect_database(db_path):
    # 连接或创建数据库
    DBX(db_path)
    return jsonify({'status': 'success', "database": db_path, 'def': 'connect_database'}), 200


@db_bp.route('/api/get/<string:db_path>', methods=['GET'])
def get_table_all(db_path):
    # 获取数据库中的所有列表
    db = DB(db_path)
    return jsonify({'status': 'success', "tables": db.get_table_all(), 'def': 'get_table_all'}), 200

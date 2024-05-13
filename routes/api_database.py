# coding = utf-8
from flask import Blueprint, jsonify
from src.DatabaseX import DBX

from src.Execute import ApiExecute


db_bp = Blueprint('api_database', __name__)


@db_bp.route('/api/connect/<string:db_path>', methods=['GET'])
@ApiExecute()
def connect_database(db_path):
    # 连接或创建数据库
    return jsonify(DBX(db_path).result()), 200

# coding = utf-8
from lib.Database import DB
from flask import Flask, jsonify

app = Flask(__name__)


# 以id查询物品信息
@app.route('/api/<string:db_path>/<string:db_table>/<int:item_id>', methods=['GET'])
def get_item_info(db_path,db_table, item_id):
    # 查询数据
    db = DB(db_path)
    db.connect_table(db_table)
    row = db.get_item_info(item_id)

    # 判断查询结果是否为空
    if row is None:
        return jsonify({'error': 'User not found'}), 404

    # 处理数据
    item_info = {'id': row[0], 'name': row[1], 'type': row[2], 'tag': row[3], 'quantity': row[4], 'price': row[5],
                 'consumables': row[6], 'remark': row[7], 'ascription': row[8]}

    # 返回响应
    return jsonify(item_info)


if __name__ == '__main__':
    app.run(debug=True)

# coding = utf-8
from src.Database import DB
from flask import Flask
from gevent import pywsgi
from routes.api import api_bp
from routes.api_database import db_bp
from routes.api_table import tb_bp
from routes.api_item import item_bp
from routes.api_qrcore import qr_bp


app = Flask(__name__)

# 注册蓝图（从模块导入路由）
app.register_blueprint(api_bp)
app.register_blueprint(db_bp)
app.register_blueprint(tb_bp)
app.register_blueprint(item_bp)
app.register_blueprint(qr_bp)

# 将默认url字符集改成utf-8，以接收中文
app.url_map.charset = 'utf-8'

if __name__ == '__main__':
    # 设置端口并运行
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()

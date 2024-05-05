# coding = utf-8

from flask import Blueprint
from markdown import markdown

index_bp = Blueprint('index_bp', __name__)


@index_bp.route('/api')
def index():
    # 在首页显示 api 文档

    # 虽然在这里写读取可能会造成性能损失，但考虑到热更新问题，姑且写在这里
    file = open('api.md', 'r', encoding='utf-8').read()

    html = markdown(file)

    return html

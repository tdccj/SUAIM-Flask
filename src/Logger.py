# coding = utf-8
import logging
from logging.handlers import TimedRotatingFileHandler
import os


def logger(name: str):
    path = f"../log/{name}"

    if not os.path.exists(path):
        os.makedirs(path)  # 创建日志文件夹

    # 配置日志
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)  # 设置默认日志级别

    # 一天记录一个文件，保留最近七天
    handler = TimedRotatingFileHandler(f'{path}/{name}.log', when="d", interval=1, backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    handler.suffix = "%Y-%m-%d-%h.log"

    _logger.addHandler(handler)
    return _logger

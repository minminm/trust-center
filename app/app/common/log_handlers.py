"""
Log Handlers

This module contains utility functions to set up logging
consistently
"""

import logging
import sys
import os
from flask import Flask


def init_logging(app: Flask, logger_name: str):
    """Set up logging for production"""
    app.logger.propagate = False

    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    # gunicorn_logger = logging.getLogger(logger_name)
    # if gunicorn_logger and gunicorn_logger.hasHandlers():
    #     app.logger.handlers = gunicorn_logger.handlers
    #     app.logger.setLevel(gunicorn_logger.level)
    # else:
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d] %(message)s",
        "%Y-%m-%d %H:%M:%S %z",
    )
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)

    app.logger.info("Logging handler established")


def setup_comprehensive_logging(app: Flask):
    # 清除现有处理器
    del app.logger.handlers[:]

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # 添加处理器
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    # 配置其他库的日志
    logging.getLogger("socketio").setLevel(logging.INFO)
    logging.getLogger("engineio").setLevel(logging.INFO)
    logging.getLogger("flask_cors").setLevel(logging.INFO)

    # 可选：文件日志
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

"""
Log Handlers

This module contains utility functions to set up logging
consistently
"""

import logging

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

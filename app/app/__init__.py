"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""

import sys

from flasgger import Swagger
from flask import Flask

from app import config
from app.service import register_routes
from extension import db, jwt


############################################################
# Initialize the Flask instance
############################################################
def create_app():
    """Initialize the core application."""
    # Create Flask application
    app = Flask(__name__)
    app.config.from_object(config)

    app.json.sort_keys = False
    app.json.ensure_ascii = False

    jwt.init_app(app)

    register_routes(app)

    with app.app_context():
        from .common import error_handlers  # noqa: F401, E402
        from .common import log_handlers

        # Set up logging for production

        log_handlers.init_logging(app, "gunicorn.error")

        app.logger.info(70 * "*")
        app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
        app.logger.info(70 * "*")

        app.logger.info("Service initialized!")

    return app

"""
Web Server Gateway Interface (WSGI) entry point
"""

import os
import sys
import threading

from flasgger import Swagger
from flask_cors import CORS
from flask_socketio import SocketIO

from app import create_app
from app.common.utils import get_server_ip
from extension import db

PORT = int(os.getenv("PORT", "8080"))

app = create_app()

CORS(app, supports_credentials=True)
Swagger(app)
socketio = SocketIO(app)

db.init_app(app)

# 必须放在 db 创建后，不然会有循环依赖 (models.py 依赖 db, init_db 依赖 models.py)
from app.db.db import init_db

with app.app_context():
    try:
        init_db(db)
    except Exception as error:  # pylint: disable=broad-except
        app.logger.critical("%s: Cannot continue", error)
        # gunicorn requires exit code 4 to stop spawning workers when they die
        sys.exit(4)

if __name__ == "__main__":
    print(f"Server starting on http://{get_server_ip()}:{PORT}...")
    socketio.run(app)

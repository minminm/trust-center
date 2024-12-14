from collections import defaultdict
from datetime import datetime
import json
import threading
from typing import DefaultDict, Dict
from flask_socketio import emit
from flask import current_app as app, request
from app.db.models import Monitor, get_trust_log_table, get_trust_log_table_model
from extension import socketio
from sqlalchemy.orm.exc import NoResultFound
from extension import db
import secrets
import asyncio

namespace = "/bmc"

activate_clients: Dict[str, Dict] = {}
lock = threading.Lock()

# 全局字典，用于执行结果
certification_results = {}
certification_locks = {}
update_base_results = {}
update_base_locks = {}


@socketio.on("connect", namespace)
def handle_connect():
    identity = request.headers.get("identity")

    app.logger.info(
        "BMC Client connected, ip=%s, identity=%s", request.remote_addr, identity
    )

    record: Monitor = Monitor.query.filter(Monitor.identity == identity).one()

    with lock:
        activate_clients[request.sid]["monitor_id"] = record.id

    app.logger.info(activate_clients)


@socketio.on("disconnect", namespace)
def handle_disconnect():
    monitor_id = activate_clients[request.sid]["monitor_id"]
    record: Monitor = Monitor.query.filter(Monitor.id == monitor_id).one()
    # 断开连接, 设置状态为 断电 & 不可信
    record.logout_at = datetime.now()
    record.power_status = 2
    record.trust_status = 2

    db.session.commit()

    with lock:
        activate_clients.pop(request.sid)

    app.logger.info(f"Client disconnected, id={monitor_id}")

from datetime import datetime
import json
import threading
from typing import Dict
from flask_socketio import emit
from flask import current_app as app, request
from app.db.models import Monitor, get_trust_log_table, get_trust_log_table_model
from extension import socketio
from sqlalchemy.orm.exc import NoResultFound
from extension import db
import secrets

namespace = "/host"

activate_clients: Dict[str, Dict] = {}
lock = threading.Lock()


@socketio.on("connect", namespace)
def handle_connect():
    identity = request.headers.get("identity")

    app.logger.info(
        "Client connected, ip=%s, identity=%s", request.remote_addr, identity
    )
    try:
        record = Monitor.query.filter(Monitor.identity == identity).one()
    except NoResultFound:
        record = Monitor(
            ip=request.remote_addr, power_status=1, trust_status=1, identity=identity
        )
        db.session.add(record)
        db.session.flush()
        # 动态创建表
        TRUST_LOG = get_trust_log_table(record.id)
        db.metadata.create_all(db.engine, [TRUST_LOG])
        app.logger.info(record.id)
        TRUST_LOG_MODEL = get_trust_log_table_model(record.id)

    # 生成随机数种子, 用于双方加密/解密
    random_key = secrets.token_urlsafe(16)

    with lock:
        activate_clients[request.sid] = {
            "random_key": random_key,
            "monitor_id": record.id,
        }

    app.logger.info(activate_clients)
    db.session.commit()

    emit("random_key", random_key, namespace=namespace)
    emit("certify", namespace=namespace)


@socketio.on("receive_key", namespace)
def handle_key(data):
    monitor_id = activate_clients[request.sid]["monitor_id"]
    # record: Monitor = Monitor.query.filter(Monitor.id == monitor_id).one()

    # db.session.commit()

    app.logger.info(f"Received key, id={monitor_id}, key={data}")


# 接收可信校验 log ; 需判断是否为初始 log -> 通过 TrustLog 表是否为空来判断
@socketio.on("receive_certify_log", namespace)
def handle_certify_log(data):
    monitor_id = activate_clients[request.sid]["monitor_id"]
    monitor_record: Monitor = Monitor.query.filter(Monitor.id == monitor_id).one()

    if "error" in data:
        app.logger.info(f"Error from client: {data['error']}")
    else:
        file_name = data.get("file_name")
        file_content = data.get("file_content")
        app.logger.info(
            f"Received file {file_name} from client. Content length: {len(file_content)} bytes."
        )
        try:
            content_str: str = file_content.decode("utf-8")
        except UnicodeDecodeError as e:
            app.logger.error(f"Failed to decode file content: {e}")
            return
        lines = content_str.splitlines()
        app.logger.info(f"File {file_name} contains {len(lines)} lines.")

        TRUST_LOG = get_trust_log_table_model(monitor_id)
        for i, line in enumerate(lines, start=1):
            app.logger.info(f"Line {i}: {line}")
            items = line.split()
            log_record = TRUST_LOG(
                pcr=[int(i) for i in items[0].split(",")],
                base_value=items[1],
                path=items[4],
            )
            db.session.add(log_record)
        db.session.commit()


@socketio.on("disconnect", namespace)
def handle_disconnect():
    monitor_id = activate_clients[request.sid]["monitor_id"]
    record: Monitor = Monitor.query.filter(Monitor.id == monitor_id).one()
    # 断开连接, 设置状态为 断电 & 不可信
    record.lougout_at = datetime.now()
    record.power_status = 2
    record.trust_status = 2

    db.session.commit()

    with lock:
        activate_clients.pop(request.sid)

    app.logger.info(f"Client disconnected, id={monitor_id}")

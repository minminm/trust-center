from calendar import c
import sys
from os import name
from time import sleep
from typing import List, Sequence
from threading import Event, Lock
from flasgger import swag_from
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_, false, or_
from sqlalchemy.orm.exc import NoResultFound

import app.common.status as status
from app.common.response import failed, success
from app.db.models import CertifyLog, Monitor, get_trust_log_table_model
from app.schemas.common import PaginatingList, ParamWithId, ParamWithIp
from app.schemas.monitor import (
    CertifyLogInfo,
    CertifyLogParams,
    MonitorInfo,
    MonitorSearchParams,
    TrustLogInfo,
    TrustLogParams,
)
from extension import db, socketio
from app.socket.host import (
    activate_clients as activate_host_clients,
    certification_results,
    certification_locks,
    update_base_results,
    update_base_locks,
)
from app.socket.bmc import activate_clients as activate_bmc_clients

import asyncio

view_trust_manage = Blueprint("trust_manage", __name__)


@view_trust_manage.route("/getMonitorList", methods=["POST"])
@jwt_required()
def get_monitor_list():
    search_params = MonitorSearchParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.ip:
        filters.append(Monitor.ip.like(f"%{search_params.ip}%"))
    if search_params.power_status:
        filters.append(Monitor.power_status == search_params.power_status)
    if search_params.trust_status:
        filters.append(Monitor.trust_status == search_params.trust_status)
    if search_params.remark:
        filters.append(Monitor.remark.like(f"%{search_params.remark}%"))

    app.logger.info(filters.__len__())

    pagination = (
        Monitor.query.order_by(Monitor.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(item: Monitor) -> MonitorInfo:
        return MonitorInfo(
            id=item.id,
            ip=item.ip,
            power_status=str(item.power_status),
            trust_status=str(item.trust_status),
            remark=item.remark,
            create_at=item.created_at,
            logout_at=item.logout_at,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[MonitorInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/getMonitorInfo", methods=["GET"])
@jwt_required()
def get_monitor_info():
    id = ParamWithId(**request.args).id

    try:
        monitor = Monitor.query.filter(Monitor.id == id).one()
    except NoResultFound:
        # Host not found
        return failed(status.HTTP_404_NOT_FOUND, "Host不存在")

    def convert(item: Monitor) -> MonitorInfo:
        return MonitorInfo(
            id=item.id,
            ip=item.ip,
            power_status=str(item.power_status),
            trust_status=str(item.trust_status),
            remark=item.remark,
            create_at=item.created_at,
            logout_at=item.logout_at,
            update_base_at=item.update_base_at,
            certify_at=item.certify_at,
            certify_times=item.certify_times,
        )

    data = convert(monitor)

    TRUST_LOG = get_trust_log_table_model(id)
    data.base_log_num = TRUST_LOG.query().count()
    # data.trust_log_num = 0

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/getTrustLogList", methods=["POST"])
@jwt_required()
def get_trust_log_list():
    search_params = TrustLogParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    TRUST_LOG = get_trust_log_table_model(search_params.id)

    filters = []
    if search_params.path:
        filters.append(TRUST_LOG.path.like(f"%{search_params.path}%"))
    if search_params.log_status:
        filters.append(TRUST_LOG.log_status == search_params.log_status)
    if search_params.base_value:
        filters.append(TRUST_LOG.base_value.like(f"%{search_params.base_value}%"))

    app.logger.info(filters.__len__())

    pagination = (
        TRUST_LOG.query()
        .order_by(TRUST_LOG.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(item) -> TrustLogInfo:
        return TrustLogInfo(
            id=item.id,
            pcr=item.pcr,
            path=item.path,
            log_status=item.log_status,
            base_value=item.base_value,
            verify_value=item.verify_value,
            update_at=item.update_at,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[TrustLogInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/getCertifyLogList", methods=["POST"])
@jwt_required()
def get_certify_log_list():
    search_params = CertifyLogParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.ip:
        filters.append(CertifyLog.ip.like(f"%{search_params.ip}%"))
    if search_params.log_status:
        filters.append(CertifyLog.log_status == search_params.log_status)
    if search_params.create_by:
        filters.append(CertifyLog.create_by.like(f"%{search_params.create_by}%"))

    app.logger.info(filters.__len__())

    pagination = (
        CertifyLog.query.order_by(CertifyLog.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(item: CertifyLog) -> CertifyLogInfo:
        return CertifyLogInfo(
            id=item.id,
            ip=item.ip,
            log_status=item.log_status,
            success_num=item.success_num,
            failed_num=item.failed_num,
            not_verify_num=item.not_verify_num,
            create_by=item.create_by,
            create_at=item.created_at,
            certify_times=item.certify_times,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[CertifyLogInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/powerOn", methods=["POST"])
@jwt_required()
def power_on():
    id = ParamWithId(**request.args).id

    target_sid = None
    for sid, values in activate_bmc_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    socketio.emit("power_on", room=target_sid, namespace="/bmc")

    return success()


@view_trust_manage.route("/powerOff", methods=["POST"])
@jwt_required()
def power_off():
    id = ParamWithId(**request.args).id

    target_sid = None
    for sid, values in activate_bmc_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    socketio.emit("power_off", room=target_sid, namespace="/bmc")

    return success()


@view_trust_manage.route("/reboot", methods=["POST"])
@jwt_required()
def reboot():
    id = ParamWithId(**request.args).id

    target_sid = None
    for sid, values in activate_bmc_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    socketio.emit("reboot", room=target_sid, namespace="/bmc")

    return success()


@view_trust_manage.route("/certify", methods=["POST"])
@jwt_required()
def certify():
    id = ParamWithId(**request.args).id

    monitor_record: Monitor = Monitor.query.filter(Monitor.id == id).one()

    target_sid = None
    for sid, values in activate_host_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    # 为此次校验创建事件和锁
    result_event = Event()
    result_lock = Lock()

    # 使用唯一标识符存储事件和锁
    certification_results[id] = None
    certification_locks[id] = {"event": result_event, "lock": result_lock}

    socketio.emit("certify", room=target_sid, namespace="/host")

    result_received = result_event.wait(timeout=5)
    if not result_received:
        return failed(code=status.SERVICE_1001_CERTIFY_TIMEOUT, msg="校验超时")

    # 获取并返回结果
    with certification_locks[id]["lock"]:
        result = certification_results[id]
        app.logger.info(result)

        trust: bool = result["failed"] == 0

        certify_log = CertifyLog(
            ip=monitor_record.ip,
            log_status=(1 if trust else 2),
            success_num=result["success"],
            failed_num=result["failed"],
            not_verify_num=result["not_verify"],
            created_at=result["certify_at"],
            create_by=get_jwt_identity(),
            certify_times=result["certify_times"],
        )
        db.session.add(certify_log)
        monitor_record.trust_status = 1 if trust else 2
        db.session.commit()

        # 清理
        del certification_results[id]
        del certification_locks[id]

    return success(data="可信" if trust else "不可信")


@view_trust_manage.route("/updateBase", methods=["POST"])
@jwt_required()
def update_base():
    id = ParamWithId(**request.args).id

    target_sid = None
    for sid, values in activate_host_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    result_event = Event()
    result_lock = Lock()

    update_base_results[id] = None
    update_base_locks[id] = {"event": result_event, "lock": result_lock}

    socketio.emit("update_base", room=target_sid, namespace="/host")

    result_received = result_event.wait(timeout=5)
    if not result_received:
        return failed(code=status.SERVICE_1002_UPDATE_BASE_TIMEOUT, msg="校验超时")

    with update_base_locks[id]["lock"]:
        result = update_base_results[id]

        del update_base_results[id]
        del update_base_locks[id]

    return success(data=f"新的基准值数量：{result['base_num']}")


@view_trust_manage.route("/batchPowerOn", methods=["POST"])
@jwt_required()
def batch_power_on():
    return success()


@view_trust_manage.route("/batchPowerOff", methods=["POST"])
@jwt_required()
def batch_power_off():
    return success()


@view_trust_manage.route("/batchCertify", methods=["POST"])
@jwt_required()
def batch_certify():
    return success()


@view_trust_manage.route("/batchUpdateBase", methods=["POST"])
@jwt_required()
def batch_update_base():
    return success()



# by don  for ai
@view_trust_manage.route("/getMonitorList_AI", methods=["POST"])
def get_monitor_list_ai():
    search_params = MonitorSearchParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.ip:
        filters.append(Monitor.ip.like(f"%{search_params.ip}%"))
    if search_params.power_status:
        filters.append(Monitor.power_status == search_params.power_status)
    if search_params.trust_status:
        filters.append(Monitor.trust_status == search_params.trust_status)
    if search_params.remark:
        filters.append(Monitor.remark.like(f"%{search_params.remark}%"))

    app.logger.info(filters.__len__())

    pagination = (
        Monitor.query.order_by(Monitor.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(item: Monitor) -> MonitorInfo:
        return MonitorInfo(
            id=item.id,
            ip=item.ip,
            power_status=str(item.power_status),
            trust_status=str(item.trust_status),
            remark=item.remark,
            create_at=item.created_at,
            logout_at=item.logout_at,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[MonitorInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/getMonitorInfo_AI", methods=["GET"])
def get_monitor_info_ai():

    ip = ParamWithIp(**request.args).ip
    try:
        monitor = Monitor.query.filter(Monitor.ip == ip).one()
    except NoResultFound:
        # Host not found
        return failed(status.HTTP_404_NOT_FOUND, "Host不存在")

    def convert(item: Monitor) -> MonitorInfo:
        return MonitorInfo(
            id=item.id,
            ip=item.ip,
            power_status=str(item.power_status),
            trust_status=str(item.trust_status),
            remark=item.remark,
            create_at=item.created_at,
            logout_at=item.logout_at,
            update_base_at=item.update_base_at,
            certify_at=item.certify_at,
            certify_times=item.certify_times,
        )

    data = convert(monitor)

    TRUST_LOG = get_trust_log_table_model(id)
    data.base_log_num = TRUST_LOG.query().count()
    # data.trust_log_num = 0

    return success(data.model_dump(by_alias=True, exclude_none=True))

# TODO
@view_trust_manage.route("/getTrustLogList_AI", methods=["POST"])
def get_trust_log_list_ai():
    search_params = TrustLogParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    TRUST_LOG = get_trust_log_table_model(search_params.id)

    filters = []
    if search_params.path:
        filters.append(TRUST_LOG.path.like(f"%{search_params.path}%"))
    if search_params.log_status:
        filters.append(TRUST_LOG.log_status == search_params.log_status)
    if search_params.base_value:
        filters.append(TRUST_LOG.base_value.like(f"%{search_params.base_value}%"))

    app.logger.info(filters.__len__())

    pagination = (
        TRUST_LOG.query()
        .order_by(TRUST_LOG.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(item) -> TrustLogInfo:
        return TrustLogInfo(
            id=item.id,
            pcr=item.pcr,
            path=item.path,
            log_status=item.log_status,
            base_value=item.base_value,
            verify_value=item.verify_value,
            update_at=item.update_at,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[TrustLogInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/getCertifyLogList_AI", methods=["POST"])
def get_certify_log_list_ai():
    search_params = CertifyLogParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.ip:
        filters.append(CertifyLog.ip.like(f"%{search_params.ip}%"))
    if search_params.log_status:
        filters.append(CertifyLog.log_status == search_params.log_status)
    if search_params.create_by:
        filters.append(CertifyLog.create_by.like(f"%{search_params.create_by}%"))

    app.logger.info(filters.__len__())

    pagination = (
        CertifyLog.query.order_by(CertifyLog.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(item: CertifyLog) -> CertifyLogInfo:
        return CertifyLogInfo(
            id=item.id,
            ip=item.ip,
            log_status=item.log_status,
            success_num=item.success_num,
            failed_num=item.failed_num,
            not_verify_num=item.not_verify_num,
            create_by=item.create_by,
            create_at=item.created_at,
            certify_times=item.certify_times,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[CertifyLogInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_trust_manage.route("/powerOn_AI", methods=["POST"])
def power_on_ai():
    ip = ParamWithIp(**request.args).ip
    id = Monitor.query.filter(Monitor.ip == ip).one().id
    target_sid = None
    for sid, values in activate_bmc_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    socketio.emit("power_on", room=target_sid, namespace="/bmc")

    return success()


@view_trust_manage.route("/powerOff_AI", methods=["POST"])
def power_off_ai():
    ip = ParamWithIp(**request.args).ip
    id = Monitor.query.filter(Monitor.ip == ip).one().id
    target_sid = None
    for sid, values in activate_bmc_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    socketio.emit("power_off", room=target_sid, namespace="/bmc")

    return success()


@view_trust_manage.route("/reboot_AI", methods=["POST"])
def reboot_ai():
    ip = ParamWithIp(**request.args).ip
    id = Monitor.query.filter(Monitor.ip == ip).one().id

    target_sid = None
    for sid, values in activate_bmc_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    socketio.emit("reboot", room=target_sid, namespace="/bmc")

    return success()


@view_trust_manage.route("/certify_AI", methods=["POST"])
def certify_ai():
    ip = ParamWithIp(**request.args).ip
    id = Monitor.query.filter(Monitor.ip == ip).one().id

    monitor_record: Monitor = Monitor.query.filter(Monitor.id == id).one()

    target_sid = None
    for sid, values in activate_host_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    # 为此次校验创建事件和锁
    result_event = Event()
    result_lock = Lock()

    # 使用唯一标识符存储事件和锁
    certification_results[id] = None
    certification_locks[id] = {"event": result_event, "lock": result_lock}

    socketio.emit("certify", room=target_sid, namespace="/host")

    result_received = result_event.wait(timeout=5)
    if not result_received:
        return failed(code=status.SERVICE_1001_CERTIFY_TIMEOUT, msg="校验超时")

    # 获取并返回结果
    with certification_locks[id]["lock"]:
        result = certification_results[id]
        app.logger.info(result)

        trust: bool = result["failed"] == 0

        certify_log = CertifyLog(
            ip=monitor_record.ip,
            log_status=(1 if trust else 2),
            success_num=result["success"],
            failed_num=result["failed"],
            not_verify_num=result["not_verify"],
            created_at=result["certify_at"],
            create_by=get_jwt_identity(),
            certify_times=result["certify_times"],
        )
        db.session.add(certify_log)
        monitor_record.trust_status = 1 if trust else 2
        db.session.commit()

        # 清理
        del certification_results[id]
        del certification_locks[id]

    return success(data="可信" if trust else "不可信")


@view_trust_manage.route("/updateBase_AI", methods=["POST"])
def update_base_ai():
    ip = ParamWithIp(**request.args).ip
    id = Monitor.query.filter(Monitor.ip == ip).one().id

    target_sid = None
    for sid, values in activate_host_clients.items():
        if values["monitor_id"] == id:
            target_sid = sid
            break

    result_event = Event()
    result_lock = Lock()

    update_base_results[id] = None
    update_base_locks[id] = {"event": result_event, "lock": result_lock}

    socketio.emit("update_base", room=target_sid, namespace="/host")

    result_received = result_event.wait(timeout=5)
    if not result_received:
        return failed(code=status.SERVICE_1002_UPDATE_BASE_TIMEOUT, msg="校验超时")

    with update_base_locks[id]["lock"]:
        result = update_base_results[id]

        del update_base_results[id]
        del update_base_locks[id]

    return success(data=f"新的基准值数量：{result['base_num']}")
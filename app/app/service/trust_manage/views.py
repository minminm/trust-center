import sys
from os import name
from time import sleep
from typing import List, Sequence

from flasgger import swag_from
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_, false, or_
from sqlalchemy.orm.exc import NoResultFound

import app.common.status as status
from app.common.response import failed, success
from app.db.models import Monitor, get_trust_log_table_model
from app.schemas.common import PaginatingList, ParamWithId
from app.schemas.monitor import (
    MonitorInfo,
    MonitorSearchParams,
    TrustLogInfo,
    TrustLogParams,
)
from extension import db, socketio

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


@view_trust_manage.route("/powerOn", methods=["POST"])
@jwt_required()
def power_on():
    return success()


@view_trust_manage.route("/powerOff", methods=["POST"])
@jwt_required()
def power_off():
    return success()


@view_trust_manage.route("/certify", methods=["POST"])
@jwt_required()
def certify():
    id = ParamWithId(**request.args).id
    socketio.emit("certify", namespace="/host")

    return success()


@view_trust_manage.route("/updateBase", methods=["POST"])
@jwt_required()
def update_base():
    return success()


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

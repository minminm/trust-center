from os import name
import sys
from time import sleep
from flasgger import swag_from
from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_, false
from flask import current_app as app
from app.db.models import Monitor
import app.common.status as status
from sqlalchemy import or_
from app.common.response import success, failed
from app.schemas.common import PaginatingList
from app.schemas.monitor import MonitorSearchParams, MonitorInfo
from typing import Sequence, List
from extension import db

view_trust_manage = Blueprint("trust_manage", __name__)


@view_trust_manage.route("/getMonitorList", methods=["POST"])
@jwt_required()
def get_monitor_list():
    app.logger.error(request.get_json())
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
            logout_at=item.lougout_at,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[MonitorInfo](
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

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
from app.db.models import ConstantRoute, Menu, Permission, Role, User
from app.schemas.common import PaginatingList, ParamWithId, ParamWithIds
from app.schemas.permission import (PermInfo, PermInsertModel,
                                    PermSearchParams, PermUpdateModel)
from app.schemas.role import RoleInfo, RoleSearchParams
from app.service.helper import get_perm_ids_by_name, get_perm_names_by_id
from extension import db

view_perm = Blueprint("perm", __name__)


@view_perm.route("/getAllPerms", methods=["GET"])
@jwt_required()
def get_all_perms():
    perms: List[Permission] = Permission.query.all()

    def convert(perm: Permission) -> PermInfo:
        return PermInfo(
            id=perm.id,
            name=perm.name,
            code=perm.code,
        )

    data = [
        convert(perm).model_dump(by_alias=True, exclude_none=True) for perm in perms
    ]

    return success(data)


@view_perm.route("/getPermList", methods=["POST"])
@jwt_required()
def get_perm_list():
    app.logger.error(request.get_json())
    search_params = PermSearchParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.name:
        filters.append(Permission.name.like(f"%{search_params.name}%"))
    if search_params.code:
        filters.append(Permission.code.like(f"%{search_params.code}%"))
    if search_params.desc:
        filters.append(Permission.description.like(f"%{search_params.desc}%"))
    if search_params.status:
        filters.append(Permission.deleted == search_params.status)

    app.logger.info(filters.__len__())

    pagination = (
        Permission.query.order_by(Permission.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(perm: Permission) -> PermInfo:
        return PermInfo(
            id=perm.id,
            status=perm.deleted,
            name=perm.name,
            code=perm.code,
            description=perm.description,
            create_at=perm.created_at,
            update_at=perm.updated_at,
            create_by=perm.create_by,
            update_by=perm.update_by,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[PermInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_perm.route("/updatePermission", methods=["POST"])
@jwt_required()
def update_perm():
    app.logger.info(request.get_json())
    update_model = PermUpdateModel(**request.get_json())

    role: Permission = Permission.query.get(update_model.id)
    if role is None:
        return failed(status.HTTP_404_NOT_FOUND, "权限不存在")

    role.name = update_model.name or role.name
    role.code = update_model.code or role.code
    role.description = update_model.desc or role.description
    if role.deleted != update_model.status:
        role.deleted = update_model.status

    db.session.commit()

    app.logger.info("Update permission success.")

    return success()


@view_perm.route("/addPermission", methods=["POST"])
@jwt_required()
def add_perm():
    app.logger.info(request.get_json())
    insert_model = PermInsertModel(**request.get_json())

    perm = Permission(
        name=insert_model.name,
        code=insert_model.code,
        deleted=insert_model.status,
        description=insert_model.desc,
    )

    db.session.add(perm)
    db.session.commit()

    return success()


@view_perm.route("/deletePermission", methods=["DELETE"])
@jwt_required()
def delete_perm():
    delete_params = ParamWithId(**request.args.to_dict())

    db.session.delete(Permission.query.get(delete_params.id))
    db.session.commit()

    return success()


@view_perm.route("/batchDeletePermission", methods=["DELETE"])
@jwt_required()
def batch_delete_perm():
    delete_params = ParamWithIds(**request.get_json())

    delete_nums = Permission.query.filter(Permission.id.in_(delete_params.ids)).delete()
    db.session.commit()

    app.logger.info("Delte Nums: %s", delete_nums)

    return success()

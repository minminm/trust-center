from os import name
import sys
from time import sleep
from flasgger import swag_from
from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_, false
from flask import current_app as app
from app.db.models import ConstantRoute, User, Role, Menu
from sqlalchemy.orm.exc import NoResultFound
import app.common.status as status
from sqlalchemy import or_
from app.common.response import success, failed
from app.schemas.common import PaginatingList
from app.schemas.role import (
    RoleBatchDeleteParams,
    RoleDeleteParams,
    RoleInsertModel,
    RoleSearchParams,
    RoleInfo,
    RoleUpdateModel,
)
from typing import Sequence, List
from extension import db
from app.service.helper import get_perm_ids_by_name, get_perm_names_by_id

view_role = Blueprint("role", __name__)


@view_role.route("/getAllRoles", methods=["GET"])
@jwt_required()
def get_all_roles():
    roles: List[Role] = Role.query.all()

    def convert(role: Role) -> RoleInfo:
        return RoleInfo(
            id=role.id,
            name=role.name,
            code=role.code,
        )

    data = [
        convert(role).model_dump(by_alias=True, exclude_none=True) for role in roles
    ]

    return success(data)


@view_role.route("/getRoleList", methods=["POST"])
@jwt_required()
def get_role_list():
    search_params = RoleSearchParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.name:
        filters.append(Role.name.like(f"%{search_params.name}%"))
    if search_params.code:
        filters.append(Role.code.like(f"%{search_params.code}%"))
    if search_params.perms:
        filters.append(
            Role.perm_ids.contains(get_perm_ids_by_name(search_params.perms))
        )

    app.logger.info(filters.__len__())

    pagination = (
        Role.query.order_by(Role.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    def convert(role: Role) -> RoleInfo:
        return RoleInfo(
            id=role.id,
            status=role.deleted,
            name=role.name,
            code=role.code,
            description=role.description,
            perms=get_perm_names_by_id(role.perm_ids),
            create_at=role.created_at,
            update_at=role.updated_at,
            create_by=role.create_by,
            update_by=role.update_by,
        )

    app.logger.info("pagination result: %s", pagination.total)

    data = PaginatingList[RoleInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_role.route("/updateRole", methods=["POST"])
@jwt_required()
def update_role():
    app.logger.info("in update role")
    app.logger.info(request.get_json())
    update_model = RoleUpdateModel(**request.get_json())

    role: Role = Role.query.get(update_model.id)
    if role is None:
        return failed(status.HTTP_404_NOT_FOUND, "角色不存在")

    role.name = update_model.name or role.name
    role.code = update_model.code or role.code
    role.description = update_model.desc or role.description
    if role.deleted != update_model.status:
        role.deleted = update_model.status
    role.perm_ids = get_perm_ids_by_name(update_model.perms)

    db.session.commit()

    app.logger.info("Update role success.")

    return success()


@view_role.route("/addRole", methods=["POST"])
@jwt_required()
def add_role():
    app.logger.info(request.get_json())
    insert_model = RoleInsertModel(**request.get_json())

    role = Role(
        name=insert_model.name,
        code=insert_model.code,
        deleted=insert_model.status,
        perm_ids=get_perm_ids_by_name(insert_model.perms),
    )

    db.session.add(role)
    db.session.commit()

    return success()


@view_role.route("/deleteRole", methods=["DELETE"])
@jwt_required()
def delete_role():
    delete_params = RoleDeleteParams(**request.args.to_dict())

    db.session.delete(Role.query.get(delete_params.id))
    db.session.commit()

    return success()


@view_role.route("/batchDeleteRole", methods=["DELETE"])
@jwt_required()
def batch_delete_role():
    delete_params = RoleBatchDeleteParams(**request.get_json())

    delete_nums = Role.query.filter(Role.id.in_(delete_params.ids)).delete()
    db.session.commit()

    app.logger.info("Delte Nums: %s", delete_nums)

    return success()

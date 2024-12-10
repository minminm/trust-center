from os import name
import sys
from time import sleep
from turtle import update
from flasgger import swag_from
from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_, false
from flask import current_app as app
from extension import db
from app.db.models import ConstantRoute, User, Role, Menu
from sqlalchemy.orm.exc import NoResultFound
import app.common.status as status
from sqlalchemy import or_
from app.common.response import success, failed
from app.schemas.common import PaginatingList
from app.schemas.user import (
    UserBatchDeleteParams,
    UserDeleteParams,
    UserInsertModel,
    UserSearchParams,
    UserInfo,
    UserUpdateModel,
)
from typing import Sequence, List

from app.service.helper import get_role_names_by_id, get_role_ids_by_name

view_user = Blueprint("user", __name__)


@view_user.route("/getUserList", methods=["POST"])
@jwt_required()
def get_user_list():
    search_params = UserSearchParams(**request.get_json())

    app.logger.info("search parmas: %s", search_params)

    filters = []
    if search_params.name:
        filters.append(User.username.like(f"%{search_params.name}%"))
    if search_params.nickname:
        filters.append(User.nickname.like(f"%{search_params.nickname}%"))
    if search_params.gender is not None:
        filters.append(User.gender == search_params.gender)
    if search_params.status is not None:
        filters.append(User.deleted == search_params.status)
    if search_params.email:
        filters.append(User.email.like(f"%{search_params.email}%"))
    if search_params.roles:
        filters.append(
            User.role_ids.contains(get_role_ids_by_name(search_params.roles))
        )

    app.logger.info(filters.__len__())

    pagination = (
        User.query.order_by(User.id)
        .filter(and_(*filters))
        .paginate(
            page=search_params.current, per_page=search_params.size, error_out=False
        )
    )

    app.logger.info("pagination result: %s", pagination.total)

    def convert(user: User) -> UserInfo:
        return UserInfo(
            id=user.id,
            status=user.deleted,
            username=user.username,
            nickname=user.nickname,
            gender=user.gender,
            email=user.email,
            roles=get_role_names_by_id(user.role_ids),
            create_at=user.created_at,
            update_at=user.updated_at,
            logout_at=user.logout_at,
            create_by=user.create_by,
            update_by=user.update_by,
        )

    data = PaginatingList[UserInfo](
        current=pagination.page,
        size=pagination.per_page,
        total=pagination.total,
        records=[convert(item) for item in pagination.items],
    )

    return success(data.model_dump(by_alias=True, exclude_none=True))


@view_user.route("/updateUser", methods=["POST"])
@jwt_required()
def update_user():
    app.logger.info(request.get_json())
    update_model = UserUpdateModel(**request.get_json())

    user: User = User.query.get(update_model.id)
    if user is None:
        return failed(status.HTTP_404_NOT_FOUND, "用户不存在")

    user.username = update_model.username or user.username
    user.nickname = update_model.nickname or user.nickname
    if user.deleted != update_model.status:
        user.deleted = update_model.status
    if user.gender != update_model.gender:
        user.gender = update_model.gender
    user.role_ids = get_role_ids_by_name(update_model.roles)

    db.session.commit()

    app.logger.info("Update user success.")

    return success()


@view_user.route("/addUser", methods=["POST"])
@jwt_required()
def add_user():
    app.logger.info(request.get_json())
    insert_model = UserInsertModel(**request.get_json())

    user = User(
        username=insert_model.username,
        deleted=insert_model.status,
        nickname=insert_model.nickname,
        gender=insert_model.gender,
        email=insert_model.email,
        role_ids=get_role_ids_by_name(insert_model.roles),
    )

    db.session.add(user)
    db.session.commit()

    return success()


@view_user.route("/deleteUser", methods=["DELETE"])
@jwt_required()
def delete_user():
    delete_params = UserDeleteParams(**request.args.to_dict())

    db.session.delete(User.query.get(delete_params.id))
    db.session.commit()

    return success()


@view_user.route("/batchDeleteUser", methods=["DELETE"])
@jwt_required()
def batch_delete_user():
    delete_params = UserBatchDeleteParams(**request.get_json())

    delete_nums = User.query.filter(User.id.in_(delete_params.ids)).delete()
    db.session.commit()

    app.logger.info("Delte Nums: %s", delete_nums)

    return success()

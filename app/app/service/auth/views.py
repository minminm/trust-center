from ast import List
from typing import Sequence

from flasgger import swag_from
from flask import Blueprint
from flask import current_app as app
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from sqlalchemy.orm.exc import NoResultFound

import app.common.status as status
from app.common.response import failed, success
from app.db.models import Permission, Role, User
from app.schemas.auth import LoginRequest, LoginToken, UserInfo

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():

    login_data = LoginRequest(**request.get_json())

    try:
        user: User = User.query.filter(
            User.username == login_data.username,
            User.password == login_data.password,
            User.deleted == 1,
        ).one()
    except NoResultFound:
        return failed(status.HTTP_401_UNAUTHORIZED, "用户名或密码错误")

    token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)

    data = LoginToken(token=token, refreshToken=refresh_token)

    app.logger.info(data)

    return success(data.model_dump())


@auth.route("/refreshToken", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)

    # app.logger.info(identity)

    return success(data={"token": token})


@auth.route("/getUserInfo", methods=["GET"])
@jwt_required()
def get_user_info():
    identity = get_jwt_identity()

    try:
        # Fetch active user
        user: User = User.query.filter(
            User.username == identity,
            User.deleted == 1,
        ).one()
    except NoResultFound:
        # User not found
        return failed(status.HTTP_404_NOT_FOUND, "用户不存在")

    # Get user's roles and permissions
    roles: Sequence[Role] = Role.query.filter(Role.id.in_(user.role_ids)).all()
    perm_ids = set().union(*(role.perm_ids for role in roles))
    perms: Sequence[Permission] = Permission.query.filter(
        Permission.id.in_(perm_ids)
    ).all()

    # Prepare response data
    role_codes = [role.code for role in roles]
    perm_codes = [perm.code for perm in perms]

    app.logger.info("roles = %s, perms = %s", role_codes, perm_codes)

    data = UserInfo(id=user.id, name=user.username, roles=role_codes, perms=perm_codes)

    return success(data=data.model_dump(by_alias=True))

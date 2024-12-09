from os import name
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
from app.schemas.user import UserSearchParams, UserInfo
from typing import Sequence, List

from app.service.helper import get_role_codes

view_user = Blueprint("user", __name__)


@view_user.route("/getUserList", methods=["GET"])
@jwt_required()
def get_user_list():
    search_params = UserSearchParams(**request.args.to_dict())

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
    app.logger.info(filters.__len__())

    pagination = User.query.filter(and_(*filters)).paginate(
        page=search_params.current, per_page=search_params.size, error_out=False
    )

    app.logger.info("pagination result: %s", pagination.total)

    def convert(user: User) -> UserInfo:
        return UserInfo(
            id=user.id,
            name=user.username,
            nickname=user.nickname,
            gender=user.gender,
            status=user.deleted,
            email=user.email,
            roles=get_role_codes(user.role_ids),
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

from os import name
import sys
from time import sleep
from flasgger import swag_from
from flask import Blueprint
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_, false
from flask import current_app as app
from app.db.models import ConstantRoute, Permission, User, Role, Menu
from sqlalchemy.orm.exc import NoResultFound
import app.common.status as status
from sqlalchemy import or_
from app.common.response import success, failed
from app.schemas.common import PaginatingList
from app.schemas.permission import PermInfo
from app.schemas.role import RoleSearchParams, RoleInfo
from typing import Sequence, List

from app.service.helper import get_perm_ids_by_name, get_perm_names_by_id

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

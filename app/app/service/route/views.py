from os import name
from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import false
from flask import current_app as app
from app.db.models import ConstantRoute, User, Role, Menu
from sqlalchemy.orm.exc import NoResultFound
import app.common.status as status

from app.common.response import success, failed
from app.schemas.route import Route, RouteMeta, UserRoute
from typing import Sequence, List

view_route = Blueprint("route", __name__)


@view_route.route("/getUserRoutes", methods=["GET"])
@jwt_required()
def get_user_routes():
    username = get_jwt_identity()
    try:
        # Fetch active user
        user: User = User.query.filter(
            User.username == username,
            User.deleted == 1,
        ).one()
    except NoResultFound:
        # User not found
        return failed(status.HTTP_404_NOT_FOUND, "用户不存在")

    # Get user's roles and menus
    roles: Sequence[Role] = Role.query.filter(Role.id.in_(user.role_ids)).all()
    menu_ids = set().union(*(role.menu_ids for role in roles))
    menus: Sequence[Menu] = Menu.query.filter(Menu.id.in_(menu_ids)).all()

    def convert(menu: Menu) -> Route:
        return Route(
            id=menu.id,
            parent_id=menu.parent_id,
            name=menu.route_name,
            path=menu.route_path,
            component=menu.component,
            props=menu.props,
            meta=RouteMeta(
                title=menu.menu_name,
                i18n_key=menu.i18n_key,
                icon=menu.icon,
                order=menu.order,
                constant=False,
                hide_in_menu=menu.hide_in_menu,
            ),
        )

    def build_menu_tree(menus: Sequence[Menu]) -> List[Route]:
        routes = [convert(menu) for menu in menus]

        routes_map = {route.id: route for route in routes}

        for route in routes:
            if route.parent_id != 0:
                parent_route = routes_map.get(route.parent_id)
                if parent_route:
                    if parent_route.children is None:
                        parent_route.children = []
                    parent_route.children.append(route)

        return [route for route in routes if route.parent_id == 0]

    data = UserRoute(routes=build_menu_tree(menus), home="home")

    return success(data=data.model_dump(by_alias=True, exclude_none=True))


@view_route.route("/getConstantRoutes", methods=["GET"])
def get_constant_routes():
    routes: Sequence[ConstantRoute] = ConstantRoute.query.all()

    def convert(route: ConstantRoute) -> Route:
        return Route(
            name=route.name,
            path=route.path,
            component=route.component,
            props=route.props,
            meta=RouteMeta(
                title=route.title,
                i18n_key=route.i18n_key,
                constant=True,
                hide_in_menu=route.hide_in_menu,
            ),
        )

    data = [
        convert(route).model_dump(by_alias=True, exclude_none=True) for route in routes
    ]

    return success(data=data)

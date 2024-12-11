from flasgger import swag_from
from flask import Blueprint, Flask, current_app, request

from app.common.response import success
from app.service.auth.views import auth
from app.service.core.views import core
from app.service.route.views import view_route
from app.service.user.views import view_user
from app.service.role.views import view_role
from app.service.permission.views import view_perm
from app.service.trust_manage.views import view_trust_manage


def register_routes(app: Flask):
    app.register_blueprint(core, url_prefix="/core")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(view_route, url_prefix="/route")
    app.register_blueprint(view_user, url_prefix="/user")
    app.register_blueprint(view_role, url_prefix="/role")
    app.register_blueprint(view_perm, url_prefix="/perm")
    app.register_blueprint(view_trust_manage, url_prefix="/trustManage")

from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.common.response import success
from app.db.models import User

core = Blueprint("core", __name__)


@core.route("/")
def index():
    """Root URL response"""
    data = {
        "name": "Monitor Backend",
        "version": "0.1",
        # "paths", url_for("list_inventory", _external=True),
    }
    return success(data=data)


@core.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return success(msg="Healthy")


@core.route("/jwt")
@jwt_required()
def test_jwt():
    return success(msg="Healthy")


@core.route("/test")
def test():
    from extension import db

    data = User(username="test", nickname="TEST", password="sss")
    db.session.add(data)
    db.session.commit()
    return success(msg="Success")

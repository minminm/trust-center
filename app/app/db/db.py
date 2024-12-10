from turtle import title
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from app.common.utils import get_server_ip

from .models import Menu, Permission, Role, User, ConstantRoute


def init_db(db: SQLAlchemy):
    db.drop_all()
    db.create_all()
    mock_user(db)
    mock_role(db)
    mock_permission(db)
    mock_menu(db)
    mock_constant_route(db)


def mock_user(db: SQLAlchemy):
    db.session.query(User).delete()
    users = [
        User(
            # id=1,
            username="super",
            nickname="Super",
            gender=1,
            password="123456",
            role_ids=[1, 2, 3, 4],
        ),
        User(
            # id=2,
            username="admin",
            nickname="Admin",
            gender=2,
            password="123456",
            role_ids=[1, 2],
        ),
        User(
            # id=3,
            username="simin",
            nickname="小明",
            gender=1,
            email="xiongsimin19@163.com",
            password="123456",
            role_ids=[1, 3],
        ),
        User(
            # id=4,
            username="empty",
            nickname="Empty",
            gender=1,
            password="123456",
            role_ids=[],
        ),
    ]
    db.session.add_all(users)
    db.session.commit()


def mock_role(db: SQLAlchemy):
    db.session.query(Role).delete()
    roles = [
        Role(
            # id=1,
            name="超级管理员",
            code="SUPER",
            description="超级管理员，拥有所有权限",
            perm_ids=[i for i in range(1, 17)],
            menu_ids=[],
        ),
        Role(
            # id=2,
            name="管理员",
            code="ADMIN",
            description="管理员，拥有查看和添加权限",
            perm_ids=[1, 2, 5, 6, 9, 10, 13, 14],
            menu_ids=[],
        ),
        Role(
            # id=3,
            name="普通用户",
            code="USER",
            description="普通用户，拥有查看权限",
            perm_ids=[1, 5, 9, 13],
            menu_ids=[i for i in range(20)],
        ),
    ]
    db.session.add_all(roles)
    db.session.commit()


def mock_permission(db: SQLAlchemy):
    permissions = [
        Permission(
            id=1, name="查看用户", code="VIEW_USER", description="查看所有用户信息"
        ),
        Permission(id=2, name="添加用户", code="ADD_USER", description="添加新用户"),
        Permission(
            id=3,
            name="更新用户",
            code="UPDATE_USER",
            description="更新用户基本信息和角色",
        ),
        Permission(id=4, name="删除用户", code="REMOVE_USER", description="删除用户"),
        Permission(
            id=5, name="查看角色", code="VIEW_ROLE", description="查看所有角色信息"
        ),
        Permission(id=6, name="添加角色", code="ADD_ROLE", description="添加新角色"),
        Permission(
            id=7,
            name="更新角色",
            code="UPDATE_ROLE",
            description="更新角色基本信息和权限",
        ),
        Permission(id=8, name="删除角色", code="REMOVE_ROLE", description="删除角色"),
        Permission(id=9, name="查看权限", code="VIEW_PERM", description="查看所有权限"),
        Permission(id=10, name="添加权限", code="ADD_PERM", description="添加新权限"),
        Permission(
            id=11, name="更新权限", code="UPDATE_PERM", description="更新权限信息"
        ),
        Permission(id=12, name="删除权限", code="REMOVE_PERM", description="删除权限"),
        Permission(
            id=13, name="查看菜单", code="VIEW_MENU", description="查看所有菜单信息"
        ),
        Permission(id=14, name="添加菜单", code="ADD_MENU", description="添加新菜单"),
        Permission(
            id=15, name="更新菜单", code="UPDATE_MENU", description="更新菜单信息"
        ),
        Permission(id=16, name="删除菜单", code="REMOVE_MENU", description="删除菜单"),
    ]
    db.session.add_all(permissions)
    db.session.commit()


def mock_menu(db: SQLAlchemy):
    menus = [
        # 首页, order: 1
        Menu(
            id=1,
            parent_id=0,
            menu_type=2,
            menu_name="首页",
            route_name="home",
            route_path="/home",
            component="layout.base$view.home",
            order=1,
            i18n_key="route.home",
            icon="mdi:monitor-dashboard",
            icon_type=1,
        ),
        # 异常页, order: 3
        Menu(
            id=2,
            parent_id=0,
            menu_type=1,
            menu_name="异常页",
            route_name="exception",
            route_path="/exception",
            component="layout.base",
            order=3,
            i18n_key="route.exception",
            icon="ant-design:exception-outlined",
            icon_type=1,
        ),
        Menu(
            id=3,
            parent_id=2,
            menu_type=2,
            menu_name="403",
            route_name="exception_403",
            route_path="/exception/403",
            component="view.403",
            order=1,
            i18n_key="route.exception_403",
            icon="ic:baseline-block",
            icon_type=1,
        ),
        Menu(
            id=4,
            parent_id=2,
            menu_type=2,
            menu_name="404",
            route_name="exception_404",
            route_path="/exception/404",
            component="view.404",
            order=2,
            i18n_key="route.exception_404",
            icon="ic:baseline-web-asset-off",
            icon_type=1,
        ),
        Menu(
            id=5,
            parent_id=2,
            menu_type=2,
            menu_name="500",
            route_name="exception_500",
            route_path="/exception/500",
            component="view.500",
            order=3,
            i18n_key="route.exception_500",
            icon="ic:baseline-wifi-off",
            icon_type=1,
        ),
        # 系统管理, order: 4
        Menu(
            id=6,
            parent_id=0,
            menu_type=1,
            menu_name="系统管理",
            route_name="manage",
            route_path="/manage",
            component="layout.base",
            order=3,
            i18n_key="route.manage",
            icon="carbon:cloud-service-management",
            icon_type=1,
        ),
        Menu(
            id=7,
            parent_id=6,
            menu_type=2,
            menu_name="用户管理",
            route_name="manage_user",
            route_path="/manage/user",
            component="view.manage_user",
            order=1,
            i18n_key="route.manage_user",
            icon="ic:round-manage-accounts",
            icon_type=1,
        ),
        Menu(
            id=8,
            parent_id=6,
            menu_type=2,
            menu_name="角色管理",
            route_name="manage_role",
            route_path="/manage/role",
            component="view.manage_role",
            order=2,
            i18n_key="route.manage_role",
            icon="carbon:user-role",
            icon_type=1,
        ),
        Menu(
            id=9,
            parent_id=6,
            menu_type=2,
            menu_name="菜单管理",
            route_name="manage_menu",
            route_path="/manage/menu",
            component="view.manage_menu",
            order=4,
            i18n_key="route.manage_menu",
            icon="material-symbols:route",
            icon_type=1,
        ),
        # 关于, order: 7
        Menu(
            id=10,
            parent_id=0,
            menu_type=1,
            menu_name="关于",
            route_name="aboute",
            route_path="/about",
            component="layout.base$view.about",
            order=7,
            i18n_key="route.about",
            icon="fluent:book-information-24-regular",
            icon_type=1,
        ),
        # 文档, order: 2
        # Menu(
        #     id=11,
        #     parent_id=0,
        #     menu_type=1,
        #     menu_name="文档",
        #     route_name="document",
        #     route_path="/document",
        #     component="layout.base",
        #     order=7,
        #     i18n_key="route.document",
        #     icon="mdi:file-document-multiple-outline",
        #     icon_type=1,
        # ),
    ]
    db.session.add_all(menus)
    db.session.commit()


def mock_constant_route(db: SQLAlchemy):
    routes = [
        ConstantRoute(
            id=1,
            name="login",
            path="/login/pwd-login",
            component="layout.blank$view.login",
            props=1,
            title="login",
            i18n_key="route.login",
        ),
        ConstantRoute(
            id=2,
            name="403",
            path="/403",
            component="layout.blank$view.403",
            title="403",
            i18n_key="route.403",
        ),
        ConstantRoute(
            id=3,
            name="404",
            path="/404",
            component="layout.blank$view.404",
            title="404",
            i18n_key="route.404",
        ),
        ConstantRoute(
            id=4,
            name="500",
            path="/500",
            component="layout.blank$view.500",
            title="500",
            i18n_key="route.500",
        ),
    ]

    db.session.add_all(routes)
    db.session.commit()

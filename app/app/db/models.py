from datetime import datetime
from turtle import title

from sqlalchemy import Boolean, Column, DateTime, Integer, SmallInteger, String, func
from sqlalchemy.dialects.postgresql import ARRAY

from extension import db


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), comment="用户名")
    nickname = Column(String(255), comment="用户昵称")
    password = Column(String(255), comment="密码")
    gender = Column(SmallInteger, default=1, comment="性别, 1: 男, 2: 女")
    email = Column(String(255), comment="邮箱")
    role_ids = Column(ARRAY(Integer), default=[], comment="用户角色ID列表")
    deleted = Column(SmallInteger, default=1, comment="状态, 1: 启用, 2: 禁用")
    created_at = Column(
        DateTime(timezone=True), default=func.now(), comment="记录创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="最后更新时间",
    )
    logout_at = Column(
        DateTime(timezone=True), nullable=True, comment="用户最后在线时间"
    )
    create_by = Column(Integer, nullable=True, comment="记录的创建者ID")
    update_by = Column(Integer, nullable=True, comment="记录的更新者ID")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, nickname={self.nickname}, role_ids={self.role_ids} created_at={self.created_at})>"


class Role(db.Model):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(255), comment="角色名")
    code = Column(String(255), comment="角色编码")
    description = Column(String(255), comment="角色描述")
    deleted = Column(SmallInteger, default=1, comment="状态, 1: 启用, 2: 禁用")
    perm_ids = Column(ARRAY(Integer), default=[], comment="角色权限ID列表")
    menu_ids = Column(ARRAY(Integer), default=[], comment="角色菜单ID列表")
    created_at = Column(
        DateTime(timezone=True), default=func.now(), comment="记录创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="最后更新时间",
    )
    create_by = Column(Integer, nullable=True, comment="记录的创建者ID")
    update_by = Column(Integer, nullable=True, comment="记录的更新者ID")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, created_at={self.created_at})>"


class Permission(db.Model):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(255), comment="权限名")
    code = Column(String(255), comment="权限编码")
    description = Column(String(255), comment="权限描述")
    deleted = Column(SmallInteger, default=1, comment="状态, 1: 启用, 2: 禁用")
    created_at = Column(
        DateTime(timezone=True), default=func.now(), comment="记录创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="最后更新时间",
    )
    create_by = Column(Integer, nullable=True, comment="记录的创建者ID")
    update_by = Column(Integer, nullable=True, comment="记录的更新者ID")

    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name}, created_at={self.created_at})>"


class Menu(db.Model):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    parent_id = Column(Integer, nullable=True, comment="父菜单ID")
    menu_type = Column(SmallInteger, default=0, comment="菜单类型, 0: 目录, 1: 菜单")
    menu_name = Column(String(255), nullable=False, comment="菜单名称")
    route_name = Column(String(255), nullable=False, comment="路由名称")
    route_path = Column(String(255), nullable=False, comment="路由路径")
    component = Column(String(255), nullable=False, comment="组件名")
    props = Column(SmallInteger, default=0, comment="是否将路由参数传递, 0: 否, 1: 是")
    i18n_key = Column(String(255), nullable=False, comment="i18n键")
    deleted = Column(SmallInteger, default=1, comment="状态, 1: 启用, 2: 禁用")
    hide_in_menu = Column(
        SmallInteger, default=0, comment="是否在菜单中隐藏, 0: 否, 1: 是"
    )
    activate_menu = Column(String(255), nullable=True, comment="高亮的菜单")
    order = Column(SmallInteger, default=0, comment="菜单顺序")
    icon = Column(String(255), nullable=False, comment="图标")
    icon_type = Column(
        SmallInteger, default=0, comment="图标类型, 0: 本地图标, 1: 其他图标"
    )
    created_at = Column(
        DateTime(timezone=True), default=func.now(), comment="记录创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="最后更新时间",
    )
    create_by = Column(Integer, nullable=True, comment="记录的创建者ID")
    update_by = Column(Integer, nullable=True, comment="记录的更新者ID")

    def __repr__(self):
        return f"<Menu(id={self.id}, menu_name={self.menu_name}, created_at={self.created_at})>"


class ConstantRoute(db.Model):
    __tablename__ = "constant_route"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(255), comment="路由名称")
    path = Column(String(255), comment="路由路径")
    component = Column(String(255), comment="组件名")
    props = Column(SmallInteger, default=0, comment="是否将路由参数传递, 0: 否, 1: 是")

    title = Column(String(255), comment="标题")
    i18n_key = Column(String(255), comment="i18n键名")
    hide_in_menu = Column(
        SmallInteger, default=1, comment="是否在菜单中隐藏, 0: 不隐藏, 1: 隐藏"
    )

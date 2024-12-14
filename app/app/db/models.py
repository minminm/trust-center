from datetime import datetime
import functools
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
        Boolean, default=False, comment="是否在菜单中隐藏, false: 否, true: 是"
    )
    active_menu = Column(String(255), nullable=True, comment="高亮的菜单")
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


class Monitor(db.Model):
    __tablename__ = "monitor"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="主键ID, 同时也是对应的基准值表id",
    )
    ip = Column(String(255), comment="IP地址")
    power_status = Column(SmallInteger, default=2, comment="电源状态, 1: 上电, 2: 断电")
    trust_status = Column(
        SmallInteger, default=2, comment="可信状态, 1: 可信, 2: 不可信"
    )
    identity = Column(String(255), comment="身份标识, 首次连接时提供")
    remark = Column(String(255), comment="备注")
    created_at = Column(
        DateTime(timezone=True), default=func.now(), comment="首次连接时间"
    )
    logout_at = Column(
        DateTime(timezone=True),
        comment="最后在线时间",
    )
    update_base_at = Column(
        DateTime(timezone=True),
        comment="最后一次更新基准值时间",
    )
    certify_at = Column(
        DateTime(timezone=True),
        comment="最后一次进行可信校验时间",
    )
    certify_times = Column(
        Integer,
        default=0,
        comment="可信检验次数（每次重启清零）",
    )


@functools.cache
def get_trust_log_table(host_id: int):

    # class TrustLog(db.Model):
    __tablename__ = f"trust_log_{host_id}"

    return db.Table(
        __tablename__,
        db.metadata,
        Column(
            "id",
            Integer,
            primary_key=True,
            autoincrement=True,
            comment="主键ID",
        ),
        Column("pcr", ARRAY(Integer), default=[], comment="用到的PCR寄存器槽位列表"),
        Column("path", String(255), comment="文件路径"),
        Column("base_value", String(255), comment="基准值"),
        Column("verify_value", String(255), comment="最新log值"),
        Column(
            "log_status",
            SmallInteger,
            comment="状态, 1: 未校验; 2: 校验成功; 3: 校验失败",
        ),
        Column(
            "update_at",
            DateTime(timezone=True),
            onupdate=func.now(),
            comment="更新时间",
        ),
    )


def get_trust_log_table_model(host_id: int):
    class BaseModel:
        """基础模型类"""

        @classmethod
        def query(cls):
            return db.session.query(cls)

    trust_log_table = get_trust_log_table(host_id)

    # 使用 type 动态生成 Model 类
    model_class = type(
        f"TrustLogModel_{host_id}",  # 动态类名
        (BaseModel, db.Model),  # 继承基础类和 SQLAlchemy 的 Model
        {
            "__table__": trust_log_table,  # 绑定表
        },
    )

    return model_class


class CertifyLog(db.Model):
    __tablename__ = "certify_log"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="主键ID, 同时也是对应的基准值表id",
    )
    ip = Column(String(255), comment="IP地址")
    log_status = Column(SmallInteger, comment="状态, 1: 校验成功; 2: 校验失败")
    success_num = Column(Integer, comment="校验成功日志条数")
    failed_num = Column(Integer, comment="校验失败日志条数")
    not_verify_num = Column(Integer, comment="未校验日志条数")
    created_at = Column(DateTime(timezone=True), comment="校验完成时间")
    create_by = Column(String(255), comment="发起校验的用户")
    certify_times = Column(
        Integer,
        default=0,
        comment="可信检验次数（每次重启清零）",
    )

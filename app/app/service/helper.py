from typing import Sequence

from app.db.models import Permission, Role


def get_role_names_by_id(role_ids: list[int]) -> list[str]:
    roles: Sequence[Role] = Role.query.filter(Role.id.in_(role_ids)).all()
    return [role.name for role in roles]


def get_role_ids_by_name(role_names: list[str]) -> list[int]:
    roles: Sequence[Role] = Role.query.filter(Role.name.in_(role_names)).all()
    return [role.id for role in roles]


def get_perm_names_by_id(perm_ids: list[int]) -> list[str]:
    perms: Sequence[Permission] = Permission.query.filter(
        Permission.id.in_(perm_ids)
    ).all()
    return [perm.name for perm in perms]


def get_perm_ids_by_name(perm_names: list[str]) -> list[int]:
    perms: Sequence[Permission] = Permission.query.filter(
        Permission.name.in_(perm_names)
    ).all()
    return [perm.id for perm in perms]

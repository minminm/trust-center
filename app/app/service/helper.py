from typing import Sequence
from app.db.models import Role


def get_role_codes(role_ids: list[int]) -> list[str]:
    roles: Sequence[Role] = Role.query.filter(Role.id.in_(role_ids)).all()
    return [role.code for role in roles]

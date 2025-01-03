from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import (CommonRecord, PaginaingCommonParams,
                                PaginaingResopnseParams)


class RoleSearchParams(PaginaingCommonParams):
    name: Optional[str] = Field(default=None, alias="roleName")
    code: Optional[str] = Field(default=None, alias="roleCode")
    desc: Optional[str] = Field(default=None, alias="roleDesc")
    status: Optional[int] = None
    perms: Optional[list[str]] = Field(default=None, alias="rolePerms")


class RoleInfo(CommonRecord):
    name: str = Field(serialization_alias="roleName")
    code: str = Field(serialization_alias="roleCode")
    description: Optional[str] = Field(default=None, serialization_alias="roleDesc")
    perms: Optional[list[str]] = Field(default=None, serialization_alias="rolePerms")


class RoleUpdateModel(BaseModel):
    id: int
    status: int
    name: Optional[str] = Field(default=None, alias="roleName")
    code: Optional[str] = Field(default=None, alias="rolecode")
    desc: Optional[str] = Field(default=None, alias="roleDesc")
    perms: list[str] = Field(alias="rolePerms")


class RoleInsertModel(BaseModel):
    status: int
    name: str = Field(alias="roleName")
    code: str = Field(alias="roleCode")
    desc: Optional[str] = Field(default=None, alias="roleDesc")
    perms: list[str] = Field(alias="rolePerms")

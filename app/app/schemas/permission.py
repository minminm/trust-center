from app.schemas.common import (
    PaginaingCommonParams,
    PaginaingResopnseParams,
    CommonRecord,
)
from typing import List, Optional
from pydantic import BaseModel, Field


class PermSearchParams(PaginaingCommonParams):
    name: Optional[str] = Field(default=None, alias="permName")
    code: Optional[str] = Field(default=None, alias="permCode")
    desc: Optional[str] = Field(default=None, alias="permDesc")
    status: Optional[int] = None


class PermInfo(CommonRecord):
    name: str = Field(serialization_alias="permName")
    code: str = Field(serialization_alias="permCode")
    description: Optional[str] = Field(default=None, serialization_alias="permDesc")


class PermUpdateModel(BaseModel):
    id: int
    status: int
    name: Optional[str] = Field(default=None, alias="permName")
    code: Optional[str] = Field(default=None, alias="permcode")
    desc: Optional[str] = Field(default=None, alias="permDesc")


class PermInsertModel(BaseModel):
    status: int
    name: str = Field(alias="PermName")
    code: str = Field(alias="PermCode")
    desc: Optional[str] = Field(default=None, alias="permDesc")


class PermDeleteParams(BaseModel):
    id: int


class PermBatchDeleteParams(BaseModel):
    ids: list[int]

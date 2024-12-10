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


class PermInfo(CommonRecord):
    name: str = Field(serialization_alias="permName")
    code: str = Field(serialization_alias="permCode")
    description: Optional[str] = Field(default=None, serialization_alias="permDesc")

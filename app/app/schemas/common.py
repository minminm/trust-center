from typing import List, Optional, TypeVar, Generic
from datetime import datetime

from pydantic import BaseModel, Field


class PaginaingCommonParams(BaseModel):
    current: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=10, le=100)


class PaginaingResopnseParams(BaseModel):
    current: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=10, le=100)
    total: int


T = TypeVar("T")


class PaginatingList(Generic[T], PaginaingResopnseParams):
    records: List[T] = Field(default=[])


class CommonRecord(BaseModel):
    id: int
    status: Optional[int] = 1
    create_at: Optional[datetime] = Field(
        default=None, serialization_alias="createTime"
    )
    update_at: Optional[datetime] = Field(
        default=None, serialization_alias="updateTime"
    )
    create_by: Optional[int] = Field(default=None, serialization_alias="createBy")
    update_by: Optional[int] = Field(default=None, serialization_alias="updateBy")

from typing import List, Optional, TypeVar, Generic

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

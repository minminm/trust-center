from datetime import datetime
from token import OP
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import (CommonRecord, PaginaingCommonParams,
                                PaginaingResopnseParams)


class UserSearchParams(PaginaingCommonParams):
    name: Optional[str] = Field(default=None, alias="userName")
    nickname: Optional[str] = Field(default=None, alias="nickName")
    gender: Optional[int] = Field(default=None, alias="userGender")
    status: Optional[int] = None
    email: Optional[str] = Field(default=None, alias="userEmail")
    roles: Optional[list[str]] = Field(default=None, alias="userRoles")


class UserInfo(CommonRecord):
    username: str = Field(serialization_alias="userName")
    nickname: str = Field(serialization_alias="nickName")
    gender: Optional[int] = Field(default=0, serialization_alias="userGender")
    email: Optional[str] = Field(default=None, serialization_alias="userEmail")
    roles: list[str] = Field(serialization_alias="userRoles")
    logout_at: Optional[datetime] = Field(serialization_alias="logoutTime")


class UserUpdateModel(BaseModel):
    id: int
    status: int
    username: Optional[str] = Field(default=None, alias="userName")
    nickname: Optional[str] = Field(default=None, alias="nickName")
    gender: Optional[int] = Field(default=1, alias="userGender")
    email: Optional[str] = Field(default=None, alias="userEmail")
    roles: list[str] = Field(alias="userRoles")


class UserInsertModel(BaseModel):
    status: int
    username: str = Field(alias="userName")
    nickname: Optional[str] = Field(default=None, alias="nickName")
    gender: Optional[int] = Field(default=1, alias="userGender")
    email: Optional[str] = Field(default=None, alias="userEmail")
    roles: list[str] = Field(alias="userRoles")

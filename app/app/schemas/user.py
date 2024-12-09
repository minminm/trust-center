from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import PaginaingCommonParams, PaginaingResopnseParams


class UserSearchParams(PaginaingCommonParams):
    name: Optional[str] = Field(default=None, alias="userName")
    nickname: Optional[str] = Field(default=None, alias="nickName")
    gender: Optional[int] = Field(default=None, alias="userGender")
    status: Optional[int] = None
    email: Optional[str] = Field(default=None, alias="userEmail")


class UserInfo(BaseModel):
    id: int
    name: str = Field(serialization_alias="userName")
    nickname: str = Field(serialization_alias="nickName")
    gender: int = Field(serialization_alias="userGender")
    status: int
    email: Optional[str] = Field(default=None, serialization_alias="userEmail")
    roles: list[str] = Field(serialization_alias="userRoles")
    create_at: datetime = Field(serialization_alias="createTime")
    update_at: Optional[datetime] = Field(serialization_alias="updateTime")
    logout_at: Optional[datetime] = Field(serialization_alias="logoutTime")
    create_by: Optional[int] = Field(serialization_alias="createBy")
    update_by: Optional[int] = Field(serialization_alias="updateBy")

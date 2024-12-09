from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

"""
alias: 对输入进行转换, 会使用 alias 的别名进行校验, 常用于接收前端传来的数据
serialization_alias: 对输出进行转换, dump_json 开启了 by_alias=True 时会使用 serialization_alias 的别名,
常用于返回给前端数据
"""


class LoginRequest(BaseModel):
    username: str = Field(alias="userName")
    password: str


class LoginToken(BaseModel):
    token: str
    refreshToken: str


class UserInfo(BaseModel):
    id: int = Field(serialization_alias="userId")
    name: str = Field(serialization_alias="userName")
    roles: list[str]
    perms: list[str]

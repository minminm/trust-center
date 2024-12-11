from datetime import datetime
from app.schemas.common import (
    PaginaingCommonParams,
    PaginaingResopnseParams,
    CommonRecord,
)
from typing import List, Optional
from pydantic import BaseModel, Field


class MonitorSearchParams(PaginaingCommonParams):
    ip: Optional[str] = Field(default=None, alias="ipAddress")
    remark: Optional[str] = None
    power_status: Optional[int] = Field(default=None, alias="powerStatus")
    trust_status: Optional[int] = Field(default=None, alias="trustStatus")


class MonitorInfo(BaseModel):
    id: int
    ip: str = Field(serialization_alias="ipAddress")
    power_status: str = Field(serialization_alias="powerStatus")
    trust_status: str = Field(serialization_alias="trustStatus")
    remark: Optional[str] = None
    create_at: datetime = Field(serialization_alias="createTime")
    logout_at: Optional[datetime] = Field(
        default=None, serialization_alias="logoutTime"
    )

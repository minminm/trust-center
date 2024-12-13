from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_serializer

from app.schemas.common import (
    CommonRecord,
    PaginaingCommonParams,
    PaginaingResopnseParams,
)


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
    update_base_at: Optional[datetime] = Field(
        default=None, serialization_alias="updateBaseTime"
    )
    certify_at: Optional[datetime] = Field(
        default=None, serialization_alias="certifyTime"
    )

    @field_serializer("create_at", "logout_at", "update_base_at", "certify_at")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

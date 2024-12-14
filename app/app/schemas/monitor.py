from datetime import datetime
from tkinter import NO
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
    certify_times: Optional[int] = Field(default=0, serialization_alias="certifyTimes")
    base_log_num: Optional[int] = Field(default=None, serialization_alias="baseLogNum")
    trust_log_num: Optional[int] = Field(
        default=None, serialization_alias="trustLogNum"
    )
    mistrust_log_num: Optional[int] = Field(
        default=None, serialization_alias="mistrustLogNum"
    )

    @field_serializer("create_at", "logout_at", "update_base_at", "certify_at")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class TrustLogParams(PaginaingCommonParams):
    id: int
    path: Optional[str] = None
    log_status: Optional[int] = Field(default=None, alias="logStatus")
    base_value: Optional[str] = Field(default=None, alias="baseValue")


class TrustLogInfo(CommonRecord):
    log_status: int = Field(serialization_alias="logStatus")
    pcr: list[int]
    path: str
    base_value: str = Field(serialization_alias="baseValue")
    verify_value: Optional[str] = Field(default=None, serialization_alias="verifyValue")
    update_at: Optional[datetime] = Field(
        default=None, serialization_alias="updateTime"
    )

    @field_serializer("update_at")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")


class CertifyLogParams(PaginaingCommonParams):
    ip: Optional[str] = Field(default=None, alias="ipAddress")
    log_status: Optional[int] = Field(default=None, alias="logStatus")
    create_by: Optional[str] = Field(default=None, alias="createBy")
    begin_at: Optional[datetime] = Field(default=None, alias="beginTime")
    end_at: Optional[datetime] = Field(default=None, alias="endTime")


class CertifyLogInfo(BaseModel):
    ip: str = Field(serialization_alias="ipAddress")
    log_status: int = Field(serialization_alias="logStatus")
    success_num: int = Field(serialization_alias="successNum")
    failed_num: int = Field(serialization_alias="failedNum")
    not_verify_num: int = Field(serialization_alias="notVerifyNum")
    certify_times: int = Field(serialization_alias="certifyTimes")
    create_at: Optional[datetime] = Field(
        default=None, serialization_alias="createTime"
    )
    create_by: Optional[str] = Field(default=None, serialization_alias="createBy")

    @field_serializer("create_at")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

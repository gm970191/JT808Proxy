"""
车辆信息数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VehicleBase(BaseModel):
    """车辆基础信息"""
    terminal_phone: str = Field(..., description="终端手机号")
    vehicle_id: Optional[str] = Field(None, description="车辆ID")
    plate_number: Optional[str] = Field(None, description="车牌号")
    vehicle_type: Optional[str] = Field(None, description="车辆类型")
    manufacturer: Optional[str] = Field(None, description="制造商")
    model: Optional[str] = Field(None, description="型号")
    color: Optional[str] = Field(None, description="颜色")

class VehicleCreate(VehicleBase):
    """创建车辆信息"""
    pass

class VehicleUpdate(BaseModel):
    """更新车辆信息"""
    vehicle_id: Optional[str] = Field(None, description="车辆ID")
    plate_number: Optional[str] = Field(None, description="车牌号")
    vehicle_type: Optional[str] = Field(None, description="车辆类型")
    manufacturer: Optional[str] = Field(None, description="制造商")
    model: Optional[str] = Field(None, description="型号")
    color: Optional[str] = Field(None, description="颜色")

class VehicleResponse(VehicleBase):
    """车辆信息响应"""
    id: int = Field(..., description="车辆ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

class VehicleChangeLog(BaseModel):
    """车辆变更日志"""
    id: int = Field(..., description="日志ID")
    terminal_phone: str = Field(..., description="终端手机号")
    field_name: str = Field(..., description="变更字段名")
    old_value: Optional[str] = Field(None, description="原值")
    new_value: Optional[str] = Field(None, description="新值")
    change_time: datetime = Field(..., description="变更时间")

    class Config:
        from_attributes = True

class VehicleListResponse(BaseModel):
    """车辆列表响应"""
    vehicles: list[VehicleResponse] = Field(..., description="车辆列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    size: int = Field(..., description="页大小") 
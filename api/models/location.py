"""
定位信息数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class LocationData(BaseModel):
    """定位数据"""
    id: int = Field(..., description="记录ID")
    terminal_phone: str = Field(..., description="终端手机号")
    msg_seq: int = Field(..., description="消息流水号")
    alarm_flag: int = Field(..., description="报警标志")
    status: int = Field(..., description="状态")
    latitude: float = Field(..., description="纬度")
    longitude: float = Field(..., description="经度")
    altitude: int = Field(..., description="高程")
    speed: int = Field(..., description="速度")
    direction: int = Field(..., description="方向")
    time: datetime = Field(..., description="时间")
    mileage: int = Field(..., description="里程")
    fuel_consumption: int = Field(..., description="油耗")
    alarm_event_id: int = Field(..., description="报警事件ID")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True

class LocationQuery(BaseModel):
    """定位数据查询参数"""
    terminal_phone: str = Field(..., description="终端手机号")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    limit: Optional[int] = Field(100, description="限制条数")

class LocationResponse(BaseModel):
    """定位数据响应"""
    locations: List[LocationData] = Field(..., description="定位数据列表")
    total: int = Field(..., description="总数")
    terminal_phone: str = Field(..., description="终端手机号")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")

class LocationStats(BaseModel):
    """定位数据统计"""
    terminal_phone: str = Field(..., description="终端手机号")
    total_records: int = Field(..., description="总记录数")
    date_range: str = Field(..., description="日期范围")
    avg_speed: float = Field(..., description="平均速度")
    max_speed: int = Field(..., description="最大速度")
    total_mileage: int = Field(..., description="总里程")
    alarm_count: int = Field(..., description="报警次数") 
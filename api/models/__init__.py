"""
数据模型包
"""

from api.models.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleChangeLog,
    VehicleListResponse
)

from api.models.location import (
    LocationData,
    LocationQuery,
    LocationResponse,
    LocationStats
)

__all__ = [
    # 车辆相关模型
    "VehicleBase",
    "VehicleCreate", 
    "VehicleUpdate",
    "VehicleResponse",
    "VehicleChangeLog",
    "VehicleListResponse",
    
    # 定位相关模型
    "LocationData",
    "LocationQuery",
    "LocationResponse",
    "LocationStats"
] 
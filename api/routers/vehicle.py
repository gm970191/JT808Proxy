"""
车辆管理API路由
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import logging

from api.models.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleChangeLog,
    VehicleListResponse
)
from api.services.vehicle_service import VehicleService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/vehicles", tags=["车辆管理"])

# 依赖注入
def get_vehicle_service():
    """获取车辆服务实例"""
    return VehicleService()

@router.post("/", response_model=VehicleResponse)
async def create_vehicle(
    vehicle: VehicleCreate,
    service: VehicleService = Depends(get_vehicle_service)
):
    """创建车辆信息"""
    try:
        result = service.create_vehicle(vehicle)
        logger.info(f"创建车辆信息成功: {vehicle.terminal_phone}")
        return result
    except Exception as e:
        logger.error(f"创建车辆信息失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=VehicleListResponse)
async def get_vehicles(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="页大小"),
    terminal_phone: Optional[str] = Query(None, description="终端手机号"),
    plate_number: Optional[str] = Query(None, description="车牌号"),
    service: VehicleService = Depends(get_vehicle_service)
):
    """获取车辆列表"""
    try:
        result = service.get_vehicles(
            page=page,
            size=size,
            terminal_phone=terminal_phone,
            plate_number=plate_number
        )
        return result
    except Exception as e:
        logger.error(f"获取车辆列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取车辆列表失败")

@router.get("/{terminal_phone}", response_model=VehicleResponse)
async def get_vehicle(
    terminal_phone: str,
    service: VehicleService = Depends(get_vehicle_service)
):
    """获取单个车辆信息"""
    try:
        vehicle = service.get_vehicle_by_phone(terminal_phone)
        if not vehicle:
            raise HTTPException(status_code=404, detail="车辆不存在")
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取车辆信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取车辆信息失败")

@router.put("/{terminal_phone}", response_model=VehicleResponse)
async def update_vehicle(
    terminal_phone: str,
    vehicle_update: VehicleUpdate,
    service: VehicleService = Depends(get_vehicle_service)
):
    """更新车辆信息"""
    try:
        result = service.update_vehicle(terminal_phone, vehicle_update)
        if not result:
            raise HTTPException(status_code=404, detail="车辆不存在")
        logger.info(f"更新车辆信息成功: {terminal_phone}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新车辆信息失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{terminal_phone}")
async def delete_vehicle(
    terminal_phone: str,
    service: VehicleService = Depends(get_vehicle_service)
):
    """删除车辆信息"""
    try:
        success = service.delete_vehicle(terminal_phone)
        if not success:
            raise HTTPException(status_code=404, detail="车辆不存在")
        logger.info(f"删除车辆信息成功: {terminal_phone}")
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除车辆信息失败: {e}")
        raise HTTPException(status_code=500, detail="删除车辆信息失败")

@router.get("/{terminal_phone}/changes", response_model=List[VehicleChangeLog])
async def get_vehicle_changes(
    terminal_phone: str,
    limit: int = Query(50, ge=1, le=200, description="限制条数"),
    service: VehicleService = Depends(get_vehicle_service)
):
    """获取车辆变更历史"""
    try:
        changes = service.get_vehicle_changes(terminal_phone, limit)
        return changes
    except Exception as e:
        logger.error(f"获取车辆变更历史失败: {e}")
        raise HTTPException(status_code=500, detail="获取车辆变更历史失败")

@router.get("/stats/summary")
async def get_vehicle_stats(
    service: VehicleService = Depends(get_vehicle_service)
):
    """获取车辆统计信息"""
    try:
        stats = service.get_vehicle_stats()
        return stats
    except Exception as e:
        logger.error(f"获取车辆统计信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取车辆统计信息失败") 
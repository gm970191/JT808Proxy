"""
定位数据API路由
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import date
import logging

from api.models.location import (
    LocationQuery,
    LocationResponse,
    LocationStats
)
from api.services.location_service import LocationService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/locations", tags=["定位数据"])

# 依赖注入
def get_location_service():
    """获取定位服务实例"""
    return LocationService()

@router.get("/{terminal_phone}", response_model=LocationResponse)
async def get_location_data(
    terminal_phone: str,
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    limit: int = Query(100, ge=1, le=1000, description="限制条数"),
    service: LocationService = Depends(get_location_service)
):
    """获取定位数据"""
    try:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="开始日期不能大于结束日期")
        
        result = service.get_location_data(
            terminal_phone=terminal_phone,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取定位数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取定位数据失败")

@router.get("/{terminal_phone}/latest")
async def get_latest_location(
    terminal_phone: str,
    service: LocationService = Depends(get_location_service)
):
    """获取最新定位数据"""
    try:
        location = service.get_latest_location(terminal_phone)
        if not location:
            raise HTTPException(status_code=404, detail="未找到定位数据")
        return location
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取最新定位数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取最新定位数据失败")

@router.get("/{terminal_phone}/stats", response_model=LocationStats)
async def get_location_stats(
    terminal_phone: str,
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    service: LocationService = Depends(get_location_service)
):
    """获取定位数据统计"""
    try:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="开始日期不能大于结束日期")
        
        stats = service.get_location_stats(
            terminal_phone=terminal_phone,
            start_date=start_date,
            end_date=end_date
        )
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取定位数据统计失败: {e}")
        raise HTTPException(status_code=500, detail="获取定位数据统计失败")

@router.get("/{terminal_phone}/alarms")
async def get_alarm_data(
    terminal_phone: str,
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    limit: int = Query(50, ge=1, le=200, description="限制条数"),
    service: LocationService = Depends(get_location_service)
):
    """获取报警数据"""
    try:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="开始日期不能大于结束日期")
        
        alarms = service.get_alarm_data(
            terminal_phone=terminal_phone,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        return {
            "terminal_phone": terminal_phone,
            "start_date": start_date,
            "end_date": end_date,
            "alarms": alarms,
            "total": len(alarms)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取报警数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取报警数据失败")

@router.get("/{terminal_phone}/track")
async def get_track_data(
    terminal_phone: str,
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    min_interval: int = Query(60, ge=10, description="最小时间间隔(秒)"),
    service: LocationService = Depends(get_location_service)
):
    """获取轨迹数据"""
    try:
        if start_date > end_date:
            raise HTTPException(status_code=400, detail="开始日期不能大于结束日期")
        
        track = service.get_track_data(
            terminal_phone=terminal_phone,
            start_date=start_date,
            end_date=end_date,
            min_interval=min_interval
        )
        return {
            "terminal_phone": terminal_phone,
            "start_date": start_date,
            "end_date": end_date,
            "track_points": track,
            "total_points": len(track)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取轨迹数据失败: {e}")
        raise HTTPException(status_code=500, detail="获取轨迹数据失败")

@router.get("/stats/overview")
async def get_location_overview(
    service: LocationService = Depends(get_location_service)
):
    """获取定位数据概览"""
    try:
        overview = service.get_location_overview()
        return overview
    except Exception as e:
        logger.error(f"获取定位数据概览失败: {e}")
        raise HTTPException(status_code=500, detail="获取定位数据概览失败") 
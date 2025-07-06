from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import psutil
import os
from ..services.monitor_service import MonitorService

router = APIRouter(prefix="/monitor", tags=["监控"])

# 创建监控服务实例
monitor_service = MonitorService()

@router.get("/connections")
async def get_connections():
    """获取连接列表"""
    try:
        connections = monitor_service.get_connections()
        return {
            "code": 200,
            "message": "获取连接列表成功",
            "data": connections
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取连接列表失败: {str(e)}")

@router.get("/system")
async def get_system_status():
    """获取系统状态"""
    try:
        status = monitor_service.get_system_status()
        return {
            "code": 200,
            "message": "获取系统状态成功",
            "data": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统状态失败: {str(e)}")

@router.get("/realtime")
async def get_real_time_data():
    """获取实时监控数据"""
    try:
        data = monitor_service.get_real_time_data()
        return {
            "code": 200,
            "message": "获取实时数据成功",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取实时数据失败: {str(e)}")

@router.get("/performance")
async def get_performance_stats(
    period: str = Query("day", description="统计周期: hour, day, week")
):
    """获取性能统计"""
    try:
        stats = monitor_service.get_performance_stats(period)
        return {
            "code": 200,
            "message": "获取性能统计成功",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取性能统计失败: {str(e)}")

@router.delete("/connections/{connection_id}")
async def disconnect_connection(connection_id: str):
    """断开指定连接"""
    try:
        success = monitor_service.disconnect_connection(connection_id)
        if success:
            return {
                "code": 200,
                "message": "断开连接成功",
                "data": None
            }
        else:
            raise HTTPException(status_code=404, detail="连接不存在")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"断开连接失败: {str(e)}") 
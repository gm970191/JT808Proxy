"""
车辆服务层
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from api.models.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleChangeLog,
    VehicleListResponse
)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jt808proxy.storage.database import DatabaseManager

logger = logging.getLogger(__name__)

class VehicleService:
    """车辆服务类"""
    
    def __init__(self):
        """初始化车辆服务"""
        self.db_manager = DatabaseManager()
    
    def create_vehicle(self, vehicle: VehicleCreate) -> VehicleResponse:
        """创建车辆信息"""
        try:
            # 检查终端手机号是否已存在
            existing = self.db_manager.get_vehicle_by_phone(vehicle.terminal_phone)
            if existing:
                raise ValueError(f"终端手机号 {vehicle.terminal_phone} 已存在")
            
            # 创建车辆信息
            vehicle_id = self.db_manager.create_vehicle(
                terminal_phone=vehicle.terminal_phone,
                vehicle_id=vehicle.vehicle_id,
                plate_number=vehicle.plate_number,
                vehicle_type=vehicle.vehicle_type,
                manufacturer=vehicle.manufacturer,
                model=vehicle.model,
                color=vehicle.color
            )
            
            # 获取创建的车辆信息
            vehicle_data = self.db_manager.get_vehicle_by_phone(vehicle.terminal_phone)
            return VehicleResponse(**vehicle_data)
            
        except Exception as e:
            logger.error(f"创建车辆信息失败: {e}")
            raise
    
    def get_vehicles(
        self,
        page: int = 1,
        size: int = 20,
        terminal_phone: Optional[str] = None,
        plate_number: Optional[str] = None
    ) -> VehicleListResponse:
        """获取车辆列表"""
        try:
            # 计算偏移量
            offset = (page - 1) * size
            
            # 获取车辆列表
            vehicles_data = self.db_manager.get_vehicles(
                offset=offset,
                limit=size,
                terminal_phone=terminal_phone,
                plate_number=plate_number
            )
            
            # 获取总数
            total = self.db_manager.get_vehicles_count(
                terminal_phone=terminal_phone,
                plate_number=plate_number
            )
            
            # 转换为响应模型
            vehicles = [VehicleResponse(**vehicle) for vehicle in vehicles_data]
            
            return VehicleListResponse(
                vehicles=vehicles,
                total=total,
                page=page,
                size=size
            )
            
        except Exception as e:
            logger.error(f"获取车辆列表失败: {e}")
            raise
    
    def get_vehicle_by_phone(self, terminal_phone: str) -> Optional[VehicleResponse]:
        """根据终端手机号获取车辆信息"""
        try:
            vehicle_data = self.db_manager.get_vehicle_by_phone(terminal_phone)
            if vehicle_data:
                return VehicleResponse(**vehicle_data)
            return None
        except Exception as e:
            logger.error(f"获取车辆信息失败: {e}")
            raise
    
    def update_vehicle(
        self,
        terminal_phone: str,
        vehicle_update: VehicleUpdate
    ) -> Optional[VehicleResponse]:
        """更新车辆信息"""
        try:
            # 检查车辆是否存在
            existing = self.db_manager.get_vehicle_by_phone(terminal_phone)
            if not existing:
                return None
            
            # 准备更新数据
            update_data = {}
            if vehicle_update.vehicle_id is not None:
                update_data['vehicle_id'] = vehicle_update.vehicle_id
            if vehicle_update.plate_number is not None:
                update_data['plate_number'] = vehicle_update.plate_number
            if vehicle_update.vehicle_type is not None:
                update_data['vehicle_type'] = vehicle_update.vehicle_type
            if vehicle_update.manufacturer is not None:
                update_data['manufacturer'] = vehicle_update.manufacturer
            if vehicle_update.model is not None:
                update_data['model'] = vehicle_update.model
            if vehicle_update.color is not None:
                update_data['color'] = vehicle_update.color
            
            if not update_data:
                # 没有需要更新的数据
                return VehicleResponse(**existing)
            
            # 更新车辆信息
            self.db_manager.update_vehicle(terminal_phone, update_data)
            
            # 获取更新后的车辆信息
            updated_vehicle = self.db_manager.get_vehicle_by_phone(terminal_phone)
            return VehicleResponse(**updated_vehicle)
            
        except Exception as e:
            logger.error(f"更新车辆信息失败: {e}")
            raise
    
    def delete_vehicle(self, terminal_phone: str) -> bool:
        """删除车辆信息"""
        try:
            # 检查车辆是否存在
            existing = self.db_manager.get_vehicle_by_phone(terminal_phone)
            if not existing:
                return False
            
            # 删除车辆信息
            self.db_manager.delete_vehicle(terminal_phone)
            return True
            
        except Exception as e:
            logger.error(f"删除车辆信息失败: {e}")
            raise
    
    def get_vehicle_changes(
        self,
        terminal_phone: str,
        limit: int = 50
    ) -> List[VehicleChangeLog]:
        """获取车辆变更历史"""
        try:
            changes_data = self.db_manager.get_vehicle_changes(
                terminal_phone=terminal_phone,
                limit=limit
            )
            
            return [VehicleChangeLog(**change) for change in changes_data]
            
        except Exception as e:
            logger.error(f"获取车辆变更历史失败: {e}")
            raise
    
    def get_vehicle_stats(self) -> Dict[str, Any]:
        """获取车辆统计信息"""
        try:
            stats = self.db_manager.get_vehicle_stats()
            return stats
        except Exception as e:
            logger.error(f"获取车辆统计信息失败: {e}")
            raise 
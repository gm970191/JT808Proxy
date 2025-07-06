"""
定位服务层
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from ..models.location import (
    LocationData,
    LocationQuery,
    LocationResponse,
    LocationStats
)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jt808proxy.storage.database import DatabaseManager

logger = logging.getLogger(__name__)

class LocationService:
    """定位服务类"""
    
    def __init__(self):
        """初始化定位服务"""
        self.db_manager = DatabaseManager()
    
    def get_location_data(
        self,
        terminal_phone: str,
        start_date: date,
        end_date: date,
        limit: int = 100
    ) -> LocationResponse:
        """获取定位数据"""
        try:
            # 获取定位数据
            locations_data = self.db_manager.get_location_data(
                terminal_phone=terminal_phone,
                start_date=start_date,
                end_date=end_date,
                limit=limit
            )
            
            # 转换为响应模型
            locations = [LocationData(**location) for location in locations_data]
            
            return LocationResponse(
                locations=locations,
                total=len(locations),
                terminal_phone=terminal_phone,
                start_date=start_date,
                end_date=end_date
            )
            
        except Exception as e:
            logger.error(f"获取定位数据失败: {e}")
            raise
    
    def get_latest_location(self, terminal_phone: str) -> Optional[LocationData]:
        """获取最新定位数据"""
        try:
            location_data = self.db_manager.get_latest_location(terminal_phone)
            if location_data:
                return LocationData(**location_data)
            return None
        except Exception as e:
            logger.error(f"获取最新定位数据失败: {e}")
            raise
    
    def get_location_stats(
        self,
        terminal_phone: str,
        start_date: date,
        end_date: date
    ) -> LocationStats:
        """获取定位数据统计"""
        try:
            stats_data = self.db_manager.get_location_stats(
                terminal_phone=terminal_phone,
                start_date=start_date,
                end_date=end_date
            )
            
            return LocationStats(**stats_data)
            
        except Exception as e:
            logger.error(f"获取定位数据统计失败: {e}")
            raise
    
    def get_alarm_data(
        self,
        terminal_phone: str,
        start_date: date,
        end_date: date,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """获取报警数据"""
        try:
            alarms_data = self.db_manager.get_alarm_data(
                terminal_phone=terminal_phone,
                start_date=start_date,
                end_date=end_date,
                limit=limit
            )
            
            return alarms_data
            
        except Exception as e:
            logger.error(f"获取报警数据失败: {e}")
            raise
    
    def get_track_data(
        self,
        terminal_phone: str,
        start_date: date,
        end_date: date,
        min_interval: int = 60
    ) -> List[Dict[str, Any]]:
        """获取轨迹数据"""
        try:
            track_data = self.db_manager.get_track_data(
                terminal_phone=terminal_phone,
                start_date=start_date,
                end_date=end_date,
                min_interval=min_interval
            )
            
            return track_data
            
        except Exception as e:
            logger.error(f"获取轨迹数据失败: {e}")
            raise
    
    def get_location_overview(self) -> Dict[str, Any]:
        """获取定位数据概览"""
        try:
            overview = self.db_manager.get_location_overview()
            return overview
        except Exception as e:
            logger.error(f"获取定位数据概览失败: {e}")
            raise 
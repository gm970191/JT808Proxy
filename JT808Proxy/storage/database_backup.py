"""
数据库管理模块
实现SQLite数据库初始化、每日分表、车辆信息管理等功能
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import os

logger = logging.getLogger(__name__)


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "jt808proxy.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # 使查询结果支持列名访问
            
            # 创建基础表
            self._create_base_tables()
            logger.info(f"数据库初始化成功: {self.db_path}")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def _create_base_tables(self):
        """创建基础表"""
        cursor = self.conn.cursor()
        
        # 车辆信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                terminal_phone TEXT UNIQUE NOT NULL,
                vehicle_id TEXT,
                plate_number TEXT,
                vehicle_type TEXT,
                manufacturer TEXT,
                model TEXT,
                color TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 车辆变更日志表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_change_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                terminal_phone TEXT NOT NULL,
                field_name TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 系统配置表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_key TEXT UNIQUE NOT NULL,
                config_value TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        logger.info("基础表创建完成")
    
    def get_location_table_name(self, target_date: date = None) -> str:
        """获取定位数据表名"""
        if target_date is None:
            target_date = date.today()
        return f"jt0200_{target_date.strftime('%Y%m%d')}"
    
    def create_location_table(self, target_date: date = None):
        """创建定位数据表（每日分表）"""
        if target_date is None:
            target_date = date.today()
        
        table_name = self.get_location_table_name(target_date)
        cursor = self.conn.cursor()
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                terminal_phone TEXT NOT NULL,
                msg_seq INTEGER NOT NULL,
                alarm_flag INTEGER,
                status INTEGER,
                latitude REAL,
                longitude REAL,
                altitude INTEGER,
                speed INTEGER,
                direction INTEGER,
                time TIMESTAMP,
                mileage INTEGER,
                fuel_consumption INTEGER,
                alarm_event_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_terminal_time 
            ON {table_name} (terminal_phone, time)
        """)
        
        self.conn.commit()
        logger.info(f"定位数据表创建完成: {table_name}")
    
    def insert_location_data(self, terminal_phone: str, msg_seq: int, location_data: Dict[str, Any]):
        """插入定位数据"""
        target_date = date.today()
        table_name = self.get_location_table_name(target_date)
        
        # 确保表存在
        self.create_location_table(target_date)
        
        cursor = self.conn.cursor()
        cursor.execute(f"""
            INSERT INTO {table_name} (
                terminal_phone, msg_seq, alarm_flag, status, latitude, longitude,
                altitude, speed, direction, time, mileage, fuel_consumption, alarm_event_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            terminal_phone, msg_seq,
            location_data.get('alarm_flag', 0),
            location_data.get('status', 0),
            location_data.get('latitude', 0.0),
            location_data.get('longitude', 0.0),
            location_data.get('altitude', 0),
            location_data.get('speed', 0),
            location_data.get('direction', 0),
            location_data.get('time', datetime.now()),
            location_data.get('mileage', 0),
            location_data.get('fuel_consumption', 0),
            location_data.get('alarm_event_id', 0)
        ))
        
        self.conn.commit()
        logger.debug(f"定位数据插入成功: {terminal_phone}, 表: {table_name}")
    
    def insert_or_update_vehicle(self, terminal_phone: str, vehicle_data: Dict[str, Any]):
        """插入或更新车辆信息"""
        cursor = self.conn.cursor()
        
        # 检查车辆是否存在
        cursor.execute("SELECT * FROM vehicles WHERE terminal_phone = ?", (terminal_phone,))
        existing_vehicle = cursor.fetchone()
        
        if existing_vehicle:
            # 更新现有车辆信息
            self._update_vehicle_info(terminal_phone, vehicle_data, existing_vehicle)
        else:
            # 插入新车辆信息
            self._insert_vehicle_info(terminal_phone, vehicle_data)
    
    def _insert_vehicle_info(self, terminal_phone: str, vehicle_data: Dict[str, Any]):
        """插入新车辆信息"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO vehicles (
                terminal_phone, vehicle_id, plate_number, vehicle_type,
                manufacturer, model, color
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            terminal_phone,
            vehicle_data.get('vehicle_id'),
            vehicle_data.get('plate_number'),
            vehicle_data.get('vehicle_type'),
            vehicle_data.get('manufacturer'),
            vehicle_data.get('model'),
            vehicle_data.get('color')
        ))
        
        self.conn.commit()
        logger.info(f"新车辆信息插入成功: {terminal_phone}")
    
    def _update_vehicle_info(self, terminal_phone: str, vehicle_data: Dict[str, Any], existing_vehicle):
        """更新车辆信息并记录变更"""
        cursor = self.conn.cursor()
        
        # 检查字段变更
        fields_to_check = ['vehicle_id', 'plate_number', 'vehicle_type', 'manufacturer', 'model', 'color']
        changes = []
        
        for field in fields_to_check:
            old_value = existing_vehicle[field]
            new_value = vehicle_data.get(field)
            if old_value != new_value:
                changes.append((field, old_value, new_value))
        
        # 记录变更日志
        for field, old_value, new_value in changes:
            cursor.execute("""
                INSERT INTO vehicle_change_logs (terminal_phone, field_name, old_value, new_value)
                VALUES (?, ?, ?, ?)
            """, (terminal_phone, field, old_value, new_value))
        
        # 更新车辆信息
        cursor.execute("""
            UPDATE vehicles SET
                vehicle_id = ?, plate_number = ?, vehicle_type = ?,
                manufacturer = ?, model = ?, color = ?, updated_at = CURRENT_TIMESTAMP
            WHERE terminal_phone = ?
        """, (
            vehicle_data.get('vehicle_id'),
            vehicle_data.get('plate_number'),
            vehicle_data.get('vehicle_type'),
            vehicle_data.get('manufacturer'),
            vehicle_data.get('model'),
            vehicle_data.get('color'),
            terminal_phone
        ))
        
        self.conn.commit()
        if changes:
            logger.info(f"车辆信息更新成功: {terminal_phone}, 变更字段: {[c[0] for c in changes]}")
    
    def get_vehicle_info(self, terminal_phone: str) -> Optional[Dict]:
        """获取车辆信息"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE terminal_phone = ?", (terminal_phone,))
        vehicle = cursor.fetchone()
        
        if vehicle:
            return dict(vehicle)
        return None
    
    def get_location_data(self, terminal_phone: str, start_date: date, end_date: date) -> List[Dict]:
        """获取定位数据"""
        cursor = self.conn.cursor()
        results = []
        
        current_date = start_date
        while current_date <= end_date:
            table_name = self.get_location_table_name(current_date)
            
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            if cursor.fetchone():
                cursor.execute(f"""
                    SELECT * FROM {table_name} 
                    WHERE terminal_phone = ? AND DATE(time) BETWEEN ? AND ?
                    ORDER BY time
                """, (terminal_phone, start_date, end_date))
                
                for row in cursor.fetchall():
                    results.append(dict(row))
            
            current_date = current_date.replace(day=current_date.day + 1)
        
        return results
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭") 
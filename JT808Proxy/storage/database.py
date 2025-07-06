"""
数据库管理模块
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "jt808proxy.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()

    def init_database(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_base_tables()

    def _create_base_tables(self):
        cursor = self.conn.cursor()
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS location_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                terminal_phone TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                altitude REAL,
                speed REAL,
                direction INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                alarm_flag INTEGER DEFAULT 0,
                status_flag INTEGER DEFAULT 0,
                fuel_level REAL,
                mileage REAL,
                engine_status INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def get_vehicle_by_phone(self, terminal_phone: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE terminal_phone = ?", (terminal_phone,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_vehicle_info(self, terminal_phone: str) -> Optional[Dict]:
        """获取车辆信息（别名方法）"""
        return self.get_vehicle_by_phone(terminal_phone)

    def insert_or_update_vehicle(self, terminal_phone: str, vehicle_data: dict):
        """插入或更新车辆信息"""
        existing_vehicle = self.get_vehicle_by_phone(terminal_phone)
        if existing_vehicle:
            # 更新现有车辆信息
            self.update_vehicle(terminal_phone, vehicle_data)
        else:
            # 创建新车辆信息
            self.create_vehicle(
                terminal_phone,
                vehicle_data.get('vehicle_id'),
                vehicle_data.get('plate_number'),
                vehicle_data.get('vehicle_type'),
                vehicle_data.get('manufacturer'),
                vehicle_data.get('model'),
                vehicle_data.get('color')
            )

    def insert_location_data(self, terminal_phone: str, msg_seq: int, location_data: dict):
        """插入定位数据"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO location_data (
                terminal_phone, latitude, longitude, altitude, speed, direction,
                alarm_flag, status_flag, fuel_level, mileage, engine_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            terminal_phone,
            location_data.get('latitude', 0),
            location_data.get('longitude', 0),
            location_data.get('altitude', 0),
            location_data.get('speed', 0),
            location_data.get('direction', 0),
            location_data.get('alarm_flag', 0),
            location_data.get('status', 0),
            location_data.get('fuel_consumption', 0),
            location_data.get('mileage', 0),
            location_data.get('engine_status', 0)
        ))
        self.conn.commit()

    def create_vehicle(self, terminal_phone: str, vehicle_id=None, plate_number=None, vehicle_type=None, manufacturer=None, model=None, color=None) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO vehicles (terminal_phone, vehicle_id, plate_number, vehicle_type, manufacturer, model, color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (terminal_phone, vehicle_id, plate_number, vehicle_type, manufacturer, model, color))
        self.conn.commit()
        return cursor.lastrowid

    def get_vehicles(self, offset=0, limit=20, terminal_phone=None, plate_number=None) -> list:
        cursor = self.conn.cursor()
        sql = "SELECT * FROM vehicles WHERE 1=1"
        params = []
        if terminal_phone:
            sql += " AND terminal_phone = ?"
            params.append(terminal_phone)
        if plate_number:
            sql += " AND plate_number = ?"
            params.append(plate_number)
        sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_vehicles_count(self, terminal_phone=None, plate_number=None) -> int:
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(*) FROM vehicles WHERE 1=1"
        params = []
        if terminal_phone:
            sql += " AND terminal_phone = ?"
            params.append(terminal_phone)
        if plate_number:
            sql += " AND plate_number = ?"
            params.append(plate_number)
        cursor.execute(sql, params)
        return cursor.fetchone()[0]

    def update_vehicle(self, terminal_phone: str, update_data: dict):
        cursor = self.conn.cursor()
        fields = []
        params = []
        for k, v in update_data.items():
            fields.append(f"{k} = ?")
            params.append(v)
        params.append(terminal_phone)
        sql = f"UPDATE vehicles SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE terminal_phone = ?"
        cursor.execute(sql, params)
        self.conn.commit()

    def delete_vehicle(self, terminal_phone: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE terminal_phone = ?", (terminal_phone,))
        self.conn.commit()

    def get_vehicle_changes(self, terminal_phone: str, limit: int = 50) -> list:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM vehicle_change_logs WHERE terminal_phone = ? ORDER BY change_time DESC LIMIT ?
        """, (terminal_phone, limit))
        return [dict(row) for row in cursor.fetchall()]

    def get_vehicle_stats(self) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_vehicles FROM vehicles")
        total_vehicles = cursor.fetchone()[0]
        return {"total_vehicles": total_vehicles}

    def get_location_data(self, terminal_phone: str, start_date: str = None, end_date: str = None, limit: int = 100) -> list:
        cursor = self.conn.cursor()
        sql = "SELECT * FROM location_data WHERE terminal_phone = ?"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_latest_location(self, terminal_phone: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM location_data WHERE terminal_phone = ? ORDER BY timestamp DESC LIMIT 1
        """, (terminal_phone,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_location_stats(self, terminal_phone: str, start_date: str = None, end_date: str = None) -> dict:
        cursor = self.conn.cursor()
        sql = "SELECT COUNT(*) as total_records FROM location_data WHERE terminal_phone = ?"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        cursor.execute(sql, params)
        total_records = cursor.fetchone()[0]
        
        sql = "SELECT AVG(speed) as avg_speed FROM location_data WHERE terminal_phone = ? AND speed > 0"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        cursor.execute(sql, params)
        avg_speed = cursor.fetchone()[0] or 0.0
        
        sql = "SELECT MAX(speed) as max_speed FROM location_data WHERE terminal_phone = ?"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        cursor.execute(sql, params)
        max_speed = cursor.fetchone()[0] or 0
        
        sql = "SELECT SUM(mileage) as total_mileage FROM location_data WHERE terminal_phone = ?"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        cursor.execute(sql, params)
        total_mileage = cursor.fetchone()[0] or 0
        
        sql = "SELECT COUNT(*) as alarm_count FROM location_data WHERE terminal_phone = ? AND alarm_flag > 0"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        cursor.execute(sql, params)
        alarm_count = cursor.fetchone()[0] or 0
        
        date_range = f"{start_date or '开始'} 至 {end_date or '结束'}"
        
        return {
            "terminal_phone": terminal_phone,
            "total_records": total_records,
            "date_range": date_range,
            "avg_speed": float(avg_speed),
            "max_speed": int(max_speed),
            "total_mileage": int(total_mileage),
            "alarm_count": int(alarm_count)
        }

    def get_alarm_data(self, terminal_phone: str, start_date: str = None, end_date: str = None, limit: int = 100) -> list:
        cursor = self.conn.cursor()
        sql = "SELECT * FROM location_data WHERE terminal_phone = ? AND alarm_flag > 0"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_track_data(self, terminal_phone: str, start_date: str = None, end_date: str = None, limit: int = 1000, min_interval: int = 60) -> list:
        cursor = self.conn.cursor()
        sql = "SELECT latitude, longitude, timestamp, speed, direction FROM location_data WHERE terminal_phone = ?"
        params = [terminal_phone]
        if start_date:
            sql += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        sql += " ORDER BY timestamp ASC LIMIT ?"
        params.append(limit)
        cursor.execute(sql, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_location_overview(self) -> dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_records FROM location_data")
        total_records = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT terminal_phone) as active_terminals FROM location_data")
        active_terminals = cursor.fetchone()[0]
        return {
            "total_records": total_records,
            "active_terminals": active_terminals
        }

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """析构函数，确保关闭连接"""
        self.close() 
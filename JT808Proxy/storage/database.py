import sqlite3
from typing import Dict, List, Optional
import logging
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
        cursor.execute("CREATE TABLE IF NOT EXISTS vehicles (id INTEGER PRIMARY KEY AUTOINCREMENT, terminal_phone TEXT UNIQUE NOT NULL, vehicle_id TEXT, plate_number TEXT, vehicle_type TEXT, manufacturer TEXT, model TEXT, color TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("CREATE TABLE IF NOT EXISTS location_data (id INTEGER PRIMARY KEY AUTOINCREMENT, terminal_phone TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL, altitude REAL, speed REAL, direction INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, alarm_flag INTEGER DEFAULT 0, status_flag INTEGER DEFAULT 0, fuel_level REAL, mileage REAL, engine_status INTEGER DEFAULT 0)")
        self.conn.commit()

    def get_vehicle_by_phone(self, terminal_phone: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE terminal_phone = ?", (terminal_phone,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def create_vehicle(self, terminal_phone: str, vehicle_id=None, plate_number=None, vehicle_type=None, manufacturer=None, model=None, color=None) -> int:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO vehicles (terminal_phone, vehicle_id, plate_number, vehicle_type, manufacturer, model, color) VALUES (?, ?, ?, ?, ?, ?, ?)", (terminal_phone, vehicle_id, plate_number, vehicle_type, manufacturer, model, color))
        self.conn.commit()
        return cursor.lastrowid

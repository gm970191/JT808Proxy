"""
数据库功能测试脚本
验证数据库初始化、定位数据存储、车辆信息管理等功能
"""
import sys
import os
import asyncio
import importlib.util
from datetime import date, datetime

# 动态加载模块
database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../jt808proxy/storage/database.py'))
spec = importlib.util.spec_from_file_location("database", database_path)
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
DatabaseManager = database.DatabaseManager

def test_database():
    """测试数据库功能"""
    print("启动数据库功能测试...")
    
    # 创建数据库管理器
    db_manager = DatabaseManager("test_jt808proxy.db")
    
    try:
        # 测试车辆信息管理
        print("\n=== 测试车辆信息管理 ===")
        
        # 插入新车辆信息
        vehicle_data = {
            'vehicle_id': 'TEST001',
            'plate_number': '京A12345',
            'vehicle_type': '测试车辆',
            'manufacturer': '测试制造商',
            'model': '测试型号',
            'color': '白色'
        }
        
        db_manager.insert_or_update_vehicle('13912345678', vehicle_data)
        print("新车辆信息插入成功")
        
        # 查询车辆信息
        vehicle_info = db_manager.get_vehicle_info('13912345678')
        if vehicle_info:
            print(f"查询到车辆信息: {vehicle_info}")
        
        # 更新车辆信息
        updated_vehicle_data = {
            'vehicle_id': 'TEST001',
            'plate_number': '京A54321',  # 变更车牌号
            'vehicle_type': '测试车辆',
            'manufacturer': '测试制造商',
            'model': '测试型号',
            'color': '白色'
        }
        
        db_manager.insert_or_update_vehicle('13912345678', updated_vehicle_data)
        print("车辆信息更新成功")
        
        # 测试定位数据存储
        print("\n=== 测试定位数据存储 ===")
        
        location_data = {
            'alarm_flag': 0,
            'status': 1,
            'latitude': 39.9042,
            'longitude': 116.4074,
            'altitude': 50,
            'speed': 60,
            'direction': 90,
            'time': datetime.now(),
            'mileage': 1000,
            'fuel_consumption': 8,
            'alarm_event_id': 0
        }
        
        db_manager.insert_location_data('13912345678', 1, location_data)
        print("定位数据存储成功")
        
        # 测试定位数据查询
        print("\n=== 测试定位数据查询 ===")
        start_date = date.today()
        end_date = date.today()
        location_records = db_manager.get_location_data('13912345678', start_date, end_date)
        print(f"查询到 {len(location_records)} 条定位记录")
        
        for record in location_records:
            print(f"定位记录: 时间={record['time']}, 位置=({record['latitude']}, {record['longitude']})")
        
        print("\n数据库功能测试完成")
        
    finally:
        # 关闭数据库连接
        db_manager.close()
        
        # 删除测试数据库文件
        if os.path.exists("test_jt808proxy.db"):
            os.remove("test_jt808proxy.db")
            print("测试数据库文件已清理")


if __name__ == "__main__":
    test_database() 
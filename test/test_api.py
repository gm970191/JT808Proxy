"""
API测试
测试Web后端API功能
"""

import pytest
import asyncio
import json
from datetime import date, datetime
from fastapi.testclient import TestClient

# 导入API应用
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.main import app

# 创建测试客户端
client = TestClient(app)

class TestVehicleAPI:
    """车辆API测试"""
    
    def test_create_vehicle(self):
        """测试创建车辆"""
        vehicle_data = {
            "terminal_phone": "13800138001",
            "vehicle_id": "V001",
            "plate_number": "京A12345",
            "vehicle_type": "小型车",
            "manufacturer": "比亚迪",
            "model": "秦",
            "color": "白色"
        }
        
        response = client.post("/api/vehicles/", json=vehicle_data)
        assert response.status_code == 200
        data = response.json()
        assert data["terminal_phone"] == vehicle_data["terminal_phone"]
        assert data["plate_number"] == vehicle_data["plate_number"]
    
    def test_get_vehicles(self):
        """测试获取车辆列表"""
        response = client.get("/api/vehicles/")
        assert response.status_code == 200
        data = response.json()
        assert "vehicles" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    def test_get_vehicle_by_phone(self):
        """测试根据手机号获取车辆"""
        response = client.get("/api/vehicles/13800138001")
        assert response.status_code == 200
        data = response.json()
        assert data["terminal_phone"] == "13800138001"
    
    def test_update_vehicle(self):
        """测试更新车辆信息"""
        update_data = {
            "plate_number": "京A54321",
            "color": "黑色"
        }
        
        response = client.put("/api/vehicles/13800138001", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["plate_number"] == update_data["plate_number"]
        assert data["color"] == update_data["color"]
    
    def test_get_vehicle_changes(self):
        """测试获取车辆变更历史"""
        response = client.get("/api/vehicles/13800138001/changes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_vehicle_stats(self):
        """测试获取车辆统计"""
        response = client.get("/api/vehicles/stats/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_vehicles" in data
    
    def test_delete_vehicle(self):
        """测试删除车辆"""
        response = client.delete("/api/vehicles/13800138001")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "删除成功"

class TestLocationAPI:
    """定位API测试"""
    
    def test_get_location_data(self):
        """测试获取定位数据"""
        # 先创建测试车辆
        vehicle_data = {
            "terminal_phone": "13800138002",
            "vehicle_id": "V002",
            "plate_number": "京B12345"
        }
        client.post("/api/vehicles/", json=vehicle_data)
        
        # 测试获取定位数据
        response = client.get("/api/locations/13800138002?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "locations" in data
        assert "total" in data
        assert data["terminal_phone"] == "13800138002"
    
    def test_get_latest_location(self):
        """测试获取最新定位"""
        response = client.get("/api/locations/13800138002/latest")
        # 可能返回404如果没有数据
        assert response.status_code in [200, 404]
    
    def test_get_location_stats(self):
        """测试获取定位统计"""
        response = client.get("/api/locations/13800138002/stats?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "terminal_phone" in data
        assert "total_records" in data
    
    def test_get_alarm_data(self):
        """测试获取报警数据"""
        response = client.get("/api/locations/13800138002/alarms?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "terminal_phone" in data
        assert "alarms" in data
        assert "total" in data
    
    def test_get_track_data(self):
        """测试获取轨迹数据"""
        response = client.get("/api/locations/13800138002/track?start_date=2024-01-01&end_date=2024-12-31")
        assert response.status_code == 200
        data = response.json()
        assert "terminal_phone" in data
        assert "track_points" in data
        assert "total_points" in data
    
    def test_get_location_overview(self):
        """测试获取定位概览"""
        response = client.get("/api/locations/stats/overview")
        assert response.status_code == 200
        data = response.json()
        assert "total_records" in data

class TestSystemAPI:
    """系统API测试"""
    
    def test_root(self):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self):
        """测试健康检查"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "JT808Proxy API"
    
    def test_system_status(self):
        """测试系统状态"""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data

def test_api_documentation():
    """测试API文档"""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/redoc")
    assert response.status_code == 200

if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"]) 
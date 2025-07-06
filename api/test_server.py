"""
简化的测试API服务器
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

# 创建FastAPI应用
app = FastAPI(
    title="JT808Proxy Test API",
    description="JT808协议代理服务测试API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "JT808Proxy Test API 服务",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "JT808Proxy Test API"
    }

@app.get("/api/vehicles")
async def get_vehicles():
    """获取车辆列表（测试数据）"""
    return {
        "vehicles": [
            {
                "id": 1,
                "terminal_phone": "13800138001",
                "vehicle_id": "V001",
                "plate_number": "京A12345",
                "vehicle_type": "小型车",
                "manufacturer": "大众",
                "model": "帕萨特",
                "color": "黑色",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            },
            {
                "id": 2,
                "terminal_phone": "13800138002",
                "vehicle_id": "V002",
                "plate_number": "京B67890",
                "vehicle_type": "中型车",
                "manufacturer": "丰田",
                "model": "凯美瑞",
                "color": "白色",
                "created_at": "2024-01-02T00:00:00",
                "updated_at": "2024-01-02T00:00:00"
            }
        ],
        "total": 2,
        "page": 1,
        "size": 20
    }

@app.get("/api/locations")
async def get_locations():
    """获取定位数据（测试数据）"""
    return {
        "locations": [
            {
                "id": 1,
                "vehicle_id": "V001",
                "latitude": 39.9042,
                "longitude": 116.4074,
                "altitude": 50,
                "speed": 60,
                "direction": 90,
                "timestamp": "2024-07-06T10:00:00",
                "status": "online"
            }
        ],
        "total": 1,
        "terminal_phone": "13800138001",
        "start_date": "2024-07-06",
        "end_date": "2024-07-06"
    }

@app.get("/api/monitor/connections")
async def get_connections():
    """获取连接信息（测试数据）"""
    return [
        {
            "id": "conn_001",
            "vehicle_id": "V001",
            "client_ip": "192.168.1.100",
            "client_port": 8080,
            "server_ip": "192.168.1.1",
            "server_port": 8080,
            "status": "connected",
            "connect_time": "2024-07-06T09:00:00",
            "last_heartbeat": "2024-07-06T10:00:00",
            "data_count": 100,
            "error_count": 0
        }
    ]

@app.get("/api/monitor/system")
async def get_system_status():
    """获取系统状态（测试数据）"""
    return {
        "cpu_usage": 25.5,
        "memory_usage": 60.2,
        "disk_usage": 45.8,
        "network_in": 1024,
        "network_out": 2048,
        "active_connections": 5,
        "total_connections": 10,
        "uptime": 86400
    }

if __name__ == "__main__":
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=7900,
        reload=True,
        log_level="info"
    ) 
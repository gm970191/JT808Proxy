"""
FastAPI 主应用
JT808Proxy Web API 服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="JT808Proxy API",
    description="JT808协议代理服务API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量存储TCP服务器实例
tcp_server = None

# 导入路由
from api.routers.vehicle import router as vehicle_router
from api.routers.location import router as location_router

# 注册路由
app.include_router(vehicle_router)
app.include_router(location_router)

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("JT808Proxy API 服务启动")
    logger.info(f"启动时间: {datetime.now()}")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("JT808Proxy API 服务关闭")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "JT808Proxy API 服务",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "JT808Proxy API"
    }

@app.get("/api/status")
async def get_system_status():
    """获取系统状态"""
    try:
        if tcp_server:
            stats = tcp_server.get_connection_stats()
            return {
                "status": "running",
                "tcp_server": {
                    "address": stats.get("server_address"),
                    "uptime_seconds": stats.get("uptime_seconds"),
                    "active_connections": stats.get("active_connections"),
                    "total_connections": stats.get("total_connections")
                },
                "monitoring": stats.get("monitoring", {}),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "tcp_server_not_available",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        raise HTTPException(status_code=500, detail="获取系统状态失败")

def set_tcp_server(server_instance):
    """设置TCP服务器实例"""
    global tcp_server
    tcp_server = server_instance
    logger.info("TCP服务器实例已设置到API服务")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7900,
        reload=True,
        log_level="info"
    ) 
"""
API路由包
"""

from api.routers.vehicle import router as vehicle_router
from api.routers.location import router as location_router

__all__ = [
    "vehicle_router",
    "location_router"
] 
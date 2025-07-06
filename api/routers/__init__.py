"""
API路由包
"""

from .vehicle import router as vehicle_router
from .location import router as location_router

__all__ = [
    "vehicle_router",
    "location_router"
] 
"""
配置API路由
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
import logging

from api.models.config import (
    ConfigCreate,
    ConfigUpdate,
    ConfigResponse,
    SystemConfig,
    ConfigCategory
)
from api.services.config_service import ConfigService
from api.routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/config", tags=["配置管理"])

# 依赖注入
def get_config_service():
    """获取配置服务实例"""
    return ConfigService()

@router.get("/", response_model=List[ConfigResponse])
async def get_configs(
    category: Optional[str] = Query(None, description="配置分类"),
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """获取配置列表"""
    try:
        if category:
            configs = config_service.get_configs_by_category(category)
        else:
            configs = config_service.get_all_configs()
        
        return [ConfigResponse(**config) for config in configs]
    except Exception as e:
        logger.error(f"获取配置列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取配置列表失败")

@router.get("/categories", response_model=List[ConfigCategory])
async def get_config_categories(
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """获取配置分类"""
    try:
        categories = [
            {
                "category": "tcp",
                "display_name": "TCP服务配置",
                "description": "TCP服务器相关配置",
                "configs": []
            },
            {
                "category": "web",
                "display_name": "Web服务配置",
                "description": "Web服务器相关配置",
                "configs": []
            },
            {
                "category": "database",
                "display_name": "数据库配置",
                "description": "数据库相关配置",
                "configs": []
            },
            {
                "category": "forward",
                "display_name": "转发配置",
                "description": "数据转发相关配置",
                "configs": []
            },
            {
                "category": "log",
                "display_name": "日志配置",
                "description": "日志相关配置",
                "configs": []
            },
            {
                "category": "monitor",
                "display_name": "监控配置",
                "description": "监控相关配置",
                "configs": []
            },
            {
                "category": "security",
                "display_name": "安全配置",
                "description": "安全相关配置",
                "configs": []
            }
        ]
        
        # 获取每个分类的配置
        for category in categories:
            configs = config_service.get_configs_by_category(category["category"])
            category["configs"] = [ConfigResponse(**config) for config in configs]
        
        return [ConfigCategory(**category) for category in categories]
    except Exception as e:
        logger.error(f"获取配置分类失败: {e}")
        raise HTTPException(status_code=500, detail="获取配置分类失败")

@router.get("/system", response_model=Dict[str, Any])
async def get_system_config(
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """获取系统配置"""
    try:
        return config_service.get_system_config()
    except Exception as e:
        logger.error(f"获取系统配置失败: {e}")
        raise HTTPException(status_code=500, detail="获取系统配置失败")

@router.put("/system")
async def update_system_config(
    config_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """更新系统配置"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        success = config_service.update_system_config(config_data)
        if not success:
            raise HTTPException(status_code=500, detail="更新系统配置失败")
        
        logger.info(f"系统配置更新成功: {list(config_data.keys())}")
        return {"message": "配置更新成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新系统配置失败: {e}")
        raise HTTPException(status_code=500, detail="更新系统配置失败")

@router.post("/", response_model=ConfigResponse)
async def create_config(
    config_data: ConfigCreate,
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """创建配置"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        success = config_service.set_config(
            config_data.key,
            config_data.value,
            config_data.description,
            config_data.category
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="创建配置失败")
        
        # 获取创建的配置
        config = config_service.db_manager.get_config(config_data.key)
        logger.info(f"创建配置成功: {config_data.key}")
        return ConfigResponse(**config)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建配置失败: {e}")
        raise HTTPException(status_code=500, detail="创建配置失败")

@router.put("/{key}", response_model=ConfigResponse)
async def update_config(
    key: str,
    config_update: ConfigUpdate,
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """更新配置"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        success = config_service.set_config(
            key,
            config_update.value,
            config_update.description
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="更新配置失败")
        
        # 获取更新后的配置
        config = config_service.db_manager.get_config(key)
        if not config:
            raise HTTPException(status_code=404, detail="配置不存在")
        
        logger.info(f"更新配置成功: {key}")
        return ConfigResponse(**config)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新配置失败: {e}")
        raise HTTPException(status_code=500, detail="更新配置失败")

@router.delete("/{key}")
async def delete_config(
    key: str,
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """删除配置"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        success = config_service.delete_config(key)
        if not success:
            raise HTTPException(status_code=404, detail="配置不存在")
        
        logger.info(f"删除配置成功: {key}")
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除配置失败: {e}")
        raise HTTPException(status_code=500, detail="删除配置失败")

@router.post("/init")
async def init_default_configs(
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """初始化默认配置"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        config_service.init_default_configs()
        return {"message": "默认配置初始化成功"}
    except Exception as e:
        logger.error(f"初始化默认配置失败: {e}")
        raise HTTPException(status_code=500, detail="初始化默认配置失败")

@router.post("/reload")
async def reload_configs(
    current_user: dict = Depends(get_current_user),
    config_service: ConfigService = Depends(get_config_service)
):
    """重新加载配置"""
    try:
        # 检查权限
        if current_user['role'] != 'admin':
            raise HTTPException(status_code=403, detail="权限不足")
        
        config_service.reload_configs()
        return {"message": "配置重新加载成功"}
    except Exception as e:
        logger.error(f"重新加载配置失败: {e}")
        raise HTTPException(status_code=500, detail="重新加载配置失败") 
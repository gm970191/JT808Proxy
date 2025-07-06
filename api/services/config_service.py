"""
配置服务
"""

import logging
from typing import List, Optional, Dict, Any
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from jt808proxy.storage.database import DatabaseManager

logger = logging.getLogger(__name__)

class ConfigService:
    """配置服务类"""
    
    def __init__(self):
        """初始化配置服务"""
        self.db_manager = DatabaseManager()
        self._cache = {}
    
    def get_config(self, key: str, default: str = None) -> str:
        """获取配置值"""
        try:
            # 先从缓存获取
            if key in self._cache:
                return self._cache[key]
            
            # 从数据库获取
            config = self.db_manager.get_config(key)
            if config:
                value = config['value']
                self._cache[key] = value
                return value
            
            return default
        except Exception as e:
            logger.error(f"获取配置失败: {e}")
            return default
    
    def set_config(self, key: str, value: str, description: str = None, category: str = "system") -> bool:
        """设置配置值"""
        try:
            # 更新数据库
            success = self.db_manager.set_config(key, value, description, category)
            if success:
                # 更新缓存
                self._cache[key] = value
            return success
        except Exception as e:
            logger.error(f"设置配置失败: {e}")
            return False
    
    def get_configs_by_category(self, category: str) -> List[Dict[str, Any]]:
        """根据分类获取配置列表"""
        try:
            return self.db_manager.get_configs_by_category(category)
        except Exception as e:
            logger.error(f"获取配置列表失败: {e}")
            return []
    
    def get_all_configs(self) -> List[Dict[str, Any]]:
        """获取所有配置"""
        try:
            return self.db_manager.get_all_configs()
        except Exception as e:
            logger.error(f"获取所有配置失败: {e}")
            return []
    
    def delete_config(self, key: str) -> bool:
        """删除配置"""
        try:
            success = self.db_manager.delete_config(key)
            if success:
                # 清除缓存
                self._cache.pop(key, None)
            return success
        except Exception as e:
            logger.error(f"删除配置失败: {e}")
            return False
    
    def get_system_config(self) -> Dict[str, Any]:
        """获取系统配置"""
        try:
            configs = self.get_all_configs()
            system_config = {}
            
            for config in configs:
                key = config['key']
                value = config['value']
                
                # 尝试转换为适当的数据类型
                if value.lower() in ('true', 'false'):
                    system_config[key] = value.lower() == 'true'
                elif value.isdigit():
                    system_config[key] = int(value)
                else:
                    system_config[key] = value
            
            return system_config
        except Exception as e:
            logger.error(f"获取系统配置失败: {e}")
            return {}
    
    def update_system_config(self, config_data: Dict[str, Any]) -> bool:
        """更新系统配置"""
        try:
            success = True
            for key, value in config_data.items():
                if not self.set_config(key, str(value)):
                    success = False
            
            return success
        except Exception as e:
            logger.error(f"更新系统配置失败: {e}")
            return False
    
    def init_default_configs(self):
        """初始化默认配置"""
        try:
            default_configs = {
                # TCP服务配置
                'tcp_port': '16900',
                'tcp_max_connections': '1000',
                'tcp_timeout': '30',
                
                # Web服务配置
                'web_port': '7000',
                'web_host': '0.0.0.0',
                
                # 数据库配置
                'db_path': './data/jt808proxy.db',
                'db_backup_enabled': 'true',
                'db_backup_interval': '24',
                
                # 转发配置
                'forward_enabled': 'true',
                'forward_timeout': '30',
                'forward_max_retries': '3',
                'forward_target_server': '192.168.1.100:8080',
                
                # 日志配置
                'log_level': 'INFO',
                'log_file_path': './logs/jt808proxy.log',
                'log_max_size': '100',
                'log_retention_days': '30',
                
                # 监控配置
                'monitor_enabled': 'true',
                'monitor_interval': '10',
                'monitor_connection_timeout': '60',
                'monitor_data_loss_threshold': '100',
                
                # 安全配置
                'jwt_secret_key': 'jt808proxy-secret-key-2024',
                'jwt_expire_minutes': '60',
                'password_min_length': '6',
                
                # 其他配置
                'system_name': 'JT808Proxy',
                'system_version': '1.0.0',
                'admin_email': 'admin@jt808proxy.com'
            }
            
            for key, value in default_configs.items():
                # 检查配置是否已存在
                existing = self.db_manager.get_config(key)
                if not existing:
                    self.set_config(key, value, f"默认{key}配置", "system")
            
            logger.info("默认配置初始化完成")
        except Exception as e:
            logger.error(f"初始化默认配置失败: {e}")
    
    def clear_cache(self):
        """清除配置缓存"""
        self._cache.clear()
    
    def reload_configs(self):
        """重新加载配置"""
        try:
            self.clear_cache()
            # 重新加载所有配置到缓存
            configs = self.get_all_configs()
            for config in configs:
                self._cache[config['key']] = config['value']
            logger.info("配置重新加载完成")
        except Exception as e:
            logger.error(f"重新加载配置失败: {e}") 
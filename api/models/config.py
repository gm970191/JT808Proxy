"""
系统配置数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ConfigBase(BaseModel):
    """配置基础信息"""
    key: str = Field(..., description="配置键")
    value: str = Field(..., description="配置值")
    description: Optional[str] = Field(None, description="配置描述")
    category: str = Field("system", description="配置分类")

class ConfigCreate(ConfigBase):
    """创建配置"""
    pass

class ConfigUpdate(BaseModel):
    """更新配置"""
    value: str = Field(..., description="配置值")
    description: Optional[str] = Field(None, description="配置描述")

class ConfigResponse(ConfigBase):
    """配置响应"""
    id: int = Field(..., description="配置ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

class SystemConfig(BaseModel):
    """系统配置"""
    # TCP服务配置
    tcp_port: int = Field(16900, description="TCP服务端口")
    tcp_max_connections: int = Field(1000, description="最大连接数")
    tcp_timeout: int = Field(30, description="连接超时时间(秒)")
    
    # Web服务配置
    web_port: int = Field(7000, description="Web服务端口")
    web_host: str = Field("0.0.0.0", description="Web服务地址")
    
    # 数据库配置
    db_path: str = Field("./data/jt808proxy.db", description="数据库路径")
    db_backup_enabled: bool = Field(True, description="启用数据库备份")
    db_backup_interval: int = Field(24, description="备份间隔(小时)")
    
    # 转发配置
    forward_enabled: bool = Field(True, description="启用智能转发")
    forward_timeout: int = Field(30, description="转发超时时间(秒)")
    forward_max_retries: int = Field(3, description="最大重试次数")
    forward_target_server: str = Field("192.168.1.100:8080", description="目标服务器")
    
    # 日志配置
    log_level: str = Field("INFO", description="日志级别")
    log_file_path: str = Field("./logs/jt808proxy.log", description="日志文件路径")
    log_max_size: int = Field(100, description="最大日志文件大小(MB)")
    log_retention_days: int = Field(30, description="保留日志天数")
    
    # 监控配置
    monitor_enabled: bool = Field(True, description="启用链路监控")
    monitor_interval: int = Field(10, description="监控间隔(秒)")
    monitor_connection_timeout: int = Field(60, description="连接超时告警(秒)")
    monitor_data_loss_threshold: int = Field(100, description="数据丢失告警阈值")
    
    # 安全配置
    jwt_secret_key: str = Field("jt808proxy-secret-key-2024", description="JWT密钥")
    jwt_expire_minutes: int = Field(60, description="JWT过期时间(分钟)")
    password_min_length: int = Field(6, description="密码最小长度")
    
    # 其他配置
    system_name: str = Field("JT808Proxy", description="系统名称")
    system_version: str = Field("1.0.0", description="系统版本")
    admin_email: str = Field("admin@jt808proxy.com", description="管理员邮箱")

class ConfigCategory(BaseModel):
    """配置分类"""
    category: str = Field(..., description="分类名称")
    display_name: str = Field(..., description="显示名称")
    description: str = Field(..., description="分类描述")
    configs: list[ConfigResponse] = Field(..., description="配置列表") 
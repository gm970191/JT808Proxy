"""
JT808 报文转发模块
支持按终端手机号智能转发，支持一对一/多对一转发模式
"""

import asyncio
import logging
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class TargetServer:
    """目标服务器配置"""
    host: str
    port: int
    name: str
    is_active: bool = True


class ForwardingConfig:
    """转发配置"""
    def __init__(self):
        # 转发模式：'one_to_one' 或 'many_to_one'
        self.mode = 'one_to_one'
        # 默认目标服务器（多对一模式使用）
        self.default_target = TargetServer('127.0.0.1', 7900, 'default_server')
        # 终端到目标服务器的映射（一对一模式使用）
        self.terminal_mapping: Dict[str, TargetServer] = {}
        # 活跃的目标服务器连接
        self.target_connections: Dict[str, asyncio.StreamWriter] = {}


class Forwarder:
    """报文转发器"""
    
    def __init__(self):
        self.config = ForwardingConfig()
        self._connection_lock = asyncio.Lock()
    
    def set_forwarding_mode(self, mode: str):
        """设置转发模式"""
        if mode not in ['one_to_one', 'many_to_one']:
            raise ValueError("转发模式必须是 'one_to_one' 或 'many_to_one'")
        self.config.mode = mode
        logger.info(f"转发模式设置为: {mode}")
    
    def add_terminal_mapping(self, terminal_phone: str, target_host: str, target_port: int, target_name: str = None):
        """添加终端到目标服务器的映射（一对一模式）"""
        target = TargetServer(target_host, target_port, target_name or f"server_{target_host}_{target_port}")
        self.config.terminal_mapping[terminal_phone] = target
        logger.info(f"添加终端映射: {terminal_phone} -> {target.host}:{target.port}")
    
    def set_default_target(self, host: str, port: int, name: str = None):
        """设置默认目标服务器（多对一模式）"""
        self.config.default_target = TargetServer(host, port, name or f"default_{host}_{port}")
        logger.info(f"设置默认目标服务器: {host}:{port}")
    
    async def get_target_connection(self, terminal_phone: str) -> Optional[asyncio.StreamWriter]:
        """获取目标服务器连接"""
        target = self._get_target_server(terminal_phone)
        if not target:
            logger.warning(f"未找到终端 {terminal_phone} 的目标服务器")
            return None
        
        # 检查是否已有连接
        conn_key = f"{target.host}:{target.port}"
        if conn_key in self.config.target_connections:
            writer = self.config.target_connections[conn_key]
            if not writer.is_closing():
                return writer
        
        # 建立新连接
        try:
            reader, writer = await asyncio.open_connection(target.host, target.port)
            async with self._connection_lock:
                self.config.target_connections[conn_key] = writer
            logger.info(f"建立到目标服务器 {target.name} ({target.host}:{target.port}) 的连接")
            return writer
        except Exception as e:
            logger.error(f"连接目标服务器 {target.name} ({target.host}:{target.port}) 失败: {e}")
            return None
    
    def _get_target_server(self, terminal_phone: str) -> Optional[TargetServer]:
        """根据终端手机号获取目标服务器"""
        if self.config.mode == 'one_to_one':
            return self.config.terminal_mapping.get(terminal_phone)
        else:  # many_to_one
            return self.config.default_target
    
    async def forward_packet(self, terminal_phone: str, data: bytes) -> bool:
        """转发数据包"""
        writer = await self.get_target_connection(terminal_phone)
        if not writer:
            return False
        
        try:
            writer.write(data)
            await writer.drain()
            logger.debug(f"成功转发数据包到终端 {terminal_phone}, 数据长度: {len(data)} 字节")
            return True
        except Exception as e:
            logger.error(f"转发数据包到终端 {terminal_phone} 失败: {e}")
            # 移除失效的连接
            await self._remove_invalid_connection(writer)
            return False
    
    async def _remove_invalid_connection(self, writer: asyncio.StreamWriter):
        """移除失效的连接"""
        async with self._connection_lock:
            for conn_key, conn_writer in list(self.config.target_connections.items()):
                if conn_writer == writer:
                    del self.config.target_connections[conn_key]
                    logger.info(f"移除失效连接: {conn_key}")
                    break
    
    def get_forwarding_stats(self) -> Dict:
        """获取转发统计信息"""
        return {
            "mode": self.config.mode,
            "default_target": {
                "host": self.config.default_target.host,
                "port": self.config.default_target.port,
                "name": self.config.default_target.name
            },
            "terminal_mappings": len(self.config.terminal_mapping),
            "active_connections": len(self.config.target_connections),
            "mappings": [
                {
                    "terminal": phone,
                    "target": f"{target.host}:{target.port}",
                    "name": target.name
                }
                for phone, target in self.config.terminal_mapping.items()
            ]
        } 
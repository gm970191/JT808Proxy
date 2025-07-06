"""
TCP Server 增强实现
支持多终端并发连接，完善的链路状态管理，详细日志记录
"""

import asyncio
import logging
import time
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# 导入JT808协议解析器
try:
    from .jt808_parser import JT808Parser
except ImportError:
    import importlib.util
    import os
    jt808_parser_path = os.path.join(os.path.dirname(__file__), 'jt808_parser.py')
    spec = importlib.util.spec_from_file_location("jt808_parser", jt808_parser_path)
    jt808_parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(jt808_parser)
    JT808Parser = jt808_parser.JT808Parser

# 导入转发器
try:
    from .forwarder import Forwarder
except ImportError:
    import importlib.util
    import os
    forwarder_path = os.path.join(os.path.dirname(__file__), 'forwarder.py')
    spec = importlib.util.spec_from_file_location("forwarder", forwarder_path)
    forwarder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(forwarder)
    Forwarder = forwarder.Forwarder

# 导入数据库管理器
try:
    from ..storage.database import DatabaseManager
except ImportError:
    import importlib.util
    import os
    database_path = os.path.join(os.path.dirname(__file__), '../storage/database.py')
    spec = importlib.util.spec_from_file_location("database", database_path)
    database = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(database)
    DatabaseManager = database.DatabaseManager

# 导入监控管理器
try:
    from ..monitor.monitor import MonitorManager, TrafficMetrics
except ImportError:
    import importlib.util
    import os
    monitor_path = os.path.join(os.path.dirname(__file__), '../monitor/monitor.py')
    spec = importlib.util.spec_from_file_location("monitor", monitor_path)
    monitor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(monitor)
    MonitorManager = monitor.MonitorManager
    TrafficMetrics = monitor.TrafficMetrics

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jt808proxy.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """连接状态枚举"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class ConnectionInfo:
    """连接信息"""
    remote_addr: str
    remote_port: int
    connect_time: datetime
    last_activity: datetime
    status: ConnectionStatus = ConnectionStatus.CONNECTED
    bytes_received: int = 0
    bytes_sent: int = 0
    packets_received: int = 0
    packets_sent: int = 0
    disconnect_reason: Optional[str] = None
    
    @property
    def is_active(self) -> bool:
        return self.status == ConnectionStatus.CONNECTED
    
    @property
    def duration(self) -> float:
        """连接持续时间（秒）"""
        if self.is_active:
            return (datetime.now() - self.connect_time).total_seconds()
        return (self.last_activity - self.connect_time).total_seconds()


@dataclass
class ServerStats:
    """服务器统计信息"""
    total_connections: int = 0
    active_connections: int = 0
    total_bytes_received: int = 0
    total_bytes_sent: int = 0
    total_packets_received: int = 0
    total_packets_sent: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def uptime(self) -> float:
        """服务器运行时间（秒）"""
        return (datetime.now() - self.start_time).total_seconds()


class TCPServer:
    """增强的 TCP 服务器实现"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 16900):
        self.host = host
        self.port = port
        self.server: Optional[asyncio.Server] = None
        self.connections: Dict[str, ConnectionInfo] = {}
        self.stats = ServerStats()
        self._connection_lock = asyncio.Lock()
        self.forwarder = Forwarder()
        self.db_manager = DatabaseManager()
        self.monitor_manager = MonitorManager()
        
    async def start(self):
        """启动服务器"""
        try:
            self.server = await asyncio.start_server(
                self.handle_client, self.host, self.port
            )
            logger.info(f"TCP Server 启动成功，监听地址: {self.host}:{self.port}")
            logger.info(f"服务器启动时间: {self.stats.start_time}")
            
            # 启动监控任务
            asyncio.create_task(self._monitor_connections())
            
            # 启动系统监控
            await self.monitor_manager.start()
            
            async with self.server:
                await self.server.serve_forever()
        except Exception as e:
            logger.error(f"TCP Server 启动失败: {e}")
            raise
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理客户端连接"""
        addr = writer.get_extra_info('peername')
        client_id = f"{addr[0]}:{addr[1]}"
        
        # 记录连接信息
        conn_info = ConnectionInfo(
            remote_addr=addr[0],
            remote_port=addr[1],
            connect_time=datetime.now(),
            last_activity=datetime.now()
        )
        
        async with self._connection_lock:
            self.connections[client_id] = conn_info
            self.stats.total_connections += 1
            self.stats.active_connections += 1
        
        logger.info(f"客户端连接: {client_id} (总连接数: {self.stats.total_connections}, 活跃连接: {self.stats.active_connections})")
        
        try:
            while True:
                # 读取数据
                data = await reader.read(1024)
                if not data:
                    break
                
                # 更新连接信息
                async with self._connection_lock:
                    conn_info.last_activity = datetime.now()
                    conn_info.bytes_received += len(data)
                    conn_info.packets_received += 1
                    self.stats.total_bytes_received += len(data)
                    self.stats.total_packets_received += 1
                
                # 记录数据接收日志
                logger.debug(f"收到来自 {client_id} 的数据: {len(data)} 字节")
                
                # JT808协议头解析
                header = JT808Parser.parse_header(data)
                if header:
                    logger.info(f"JT808协议头解析成功 - 终端手机号: {header.phone}, "
                              f"消息ID: 0x{header.msg_id:04X}, 流水号: {header.msg_seq}")
                    if header.pkg_total and header.pkg_index:
                        logger.info(f"分包信息 - 总数: {header.pkg_total}, 序号: {header.pkg_index}")
                    
                    # 根据消息ID处理不同类型的报文
                    await self._process_message(header, data)
                    
                    # 尝试转发数据包
                    forward_success = await self.forwarder.forward_packet(header.phone, data)
                    if forward_success:
                        logger.info(f"数据包转发成功 - 终端: {header.phone}")
                    else:
                        logger.warning(f"数据包转发失败 - 终端: {header.phone}")
                else:
                    logger.warning(f"无法解析JT808协议头，数据长度: {len(data)} 字节")
                
                # 回显数据（基础实现）
                writer.write(data)
                await writer.drain()
                
                # 更新发送统计
                async with self._connection_lock:
                    conn_info.bytes_sent += len(data)
                    conn_info.packets_sent += 1
                    self.stats.total_bytes_sent += len(data)
                    self.stats.total_packets_sent += 1
                
        except Exception as e:
            logger.error(f"处理客户端 {client_id} 数据时出错: {e}")
            conn_info.status = ConnectionStatus.ERROR
            conn_info.disconnect_reason = f"处理错误: {e}"
        finally:
            # 清理连接
            writer.close()
            await writer.wait_closed()
            
            async with self._connection_lock:
                if client_id in self.connections:
                    conn_info.status = ConnectionStatus.DISCONNECTED
                    if not conn_info.disconnect_reason:
                        conn_info.disconnect_reason = "客户端主动断开"
                    self.stats.active_connections -= 1
            
            logger.info(f"客户端断开连接: {client_id} (断开原因: {conn_info.disconnect_reason})")
    
    async def _monitor_connections(self):
        """监控连接状态"""
        while True:
            try:
                await asyncio.sleep(30)  # 每30秒检查一次
                
                current_time = datetime.now()
                idle_connections = []
                
                async with self._connection_lock:
                    for client_id, conn_info in self.connections.items():
                        if conn_info.is_active:
                            idle_time = (current_time - conn_info.last_activity).total_seconds()
                            if idle_time > 600:  # 10分钟空闲
                                idle_connections.append(client_id)
                
                # 记录统计信息
                if self.stats.active_connections > 0:
                    logger.info(f"连接监控 - 活跃连接: {self.stats.active_connections}, "
                              f"总接收: {self.stats.total_bytes_received} 字节, "
                              f"总发送: {self.stats.total_bytes_sent} 字节")
                    
                    # 更新监控指标
                    traffic_metrics = TrafficMetrics(
                        bytes_received=self.stats.total_bytes_received,
                        bytes_sent=self.stats.total_bytes_sent,
                        packets_received=self.stats.total_packets_received,
                        packets_sent=self.stats.total_packets_sent,
                        active_connections=self.stats.active_connections,
                        total_connections=self.stats.total_connections
                    )
                    self.monitor_manager.update_traffic_metrics(traffic_metrics)
                
            except Exception as e:
                logger.error(f"监控连接时出错: {e}")
    
    async def _process_message(self, header, data: bytes):
        """根据消息ID处理不同类型的报文"""
        try:
            if header.msg_id == 0x0200:  # 定位信息
                await self._process_location_message(header, data)
            elif header.msg_id == 0x0100:  # 终端注册
                await self._process_register_message(header, data)
        except Exception as e:
            logger.error(f"处理消息时出错: {e}")
    
    async def _process_location_message(self, header, data: bytes):
        """处理定位信息报文"""
        # 计算消息体偏移量（考虑分包字段）
        body_offset = 12
        if header.pkg_total and header.pkg_index:
            body_offset = 16
        
        # 解析定位数据
        location_data = JT808Parser.parse_location_data(data, body_offset)
        if location_data:
            # 存储到数据库
            self.db_manager.insert_location_data(header.phone, header.msg_seq, location_data)
            logger.info(f"定位数据存储成功 - 终端: {header.phone}, "
                       f"位置: ({location_data['latitude']:.6f}, {location_data['longitude']:.6f})")
    
    async def _process_register_message(self, header, data: bytes):
        """处理终端注册报文"""
        # 计算消息体偏移量
        body_offset = 12
        if header.pkg_total and header.pkg_index:
            body_offset = 16
        
        # 解析注册数据
        register_data = JT808Parser.parse_terminal_register(data, body_offset)
        if register_data:
            # 转换为车辆信息格式
            vehicle_data = {
                'vehicle_id': register_data.get('terminal_id'),
                'plate_number': register_data.get('plate_number'),
                'vehicle_type': 'JT808终端',
                'manufacturer': f"制造商ID:{register_data.get('manufacturer_id')}",
                'model': register_data.get('terminal_model'),
                'color': f"车牌颜色:{register_data.get('plate_color')}"
            }
            
            # 存储或更新车辆信息
            self.db_manager.insert_or_update_vehicle(header.phone, vehicle_data)
            logger.info(f"车辆信息处理成功 - 终端: {header.phone}, 车牌: {vehicle_data.get('plate_number')}")
    
    def get_connection_stats(self) -> Dict:
        """获取连接统计信息"""
        async def _get_stats():
            async with self._connection_lock:
                        return {
            "server_address": f"{self.host}:{self.port}",
            "uptime_seconds": self.stats.uptime,
            "total_connections": self.stats.total_connections,
            "active_connections": self.stats.active_connections,
            "total_bytes_received": self.stats.total_bytes_received,
            "total_bytes_sent": self.stats.total_bytes_sent,
            "total_packets_received": self.stats.total_packets_received,
            "total_packets_sent": self.stats.total_packets_sent,
            "connections": [
                {
                    "client_id": client_id,
                    "remote_addr": conn.remote_addr,
                    "remote_port": conn.remote_port,
                    "connect_time": conn.connect_time.isoformat(),
                    "last_activity": conn.last_activity.isoformat(),
                    "status": conn.status.value,
                    "duration_seconds": conn.duration,
                    "bytes_received": conn.bytes_received,
                    "bytes_sent": conn.bytes_sent,
                    "packets_received": conn.packets_received,
                    "packets_sent": conn.packets_sent,
                    "disconnect_reason": conn.disconnect_reason
                }
                for client_id, conn in self.connections.items()
            ],
            "monitoring": self.monitor_manager.get_monitoring_stats()
        }
        
        # 由于这是同步方法，我们需要在事件循环中运行
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果事件循环正在运行，创建一个任务
                future = asyncio.create_task(_get_stats())
                return future.result()
            else:
                return asyncio.run(_get_stats())
        except RuntimeError:
            # 如果没有事件循环，创建一个新的
            return asyncio.run(_get_stats())


async def main():
    """主函数"""
    server = TCPServer(host='0.0.0.0', port=16900)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main()) 
import psutil
import os
from datetime import datetime
from typing import List, Dict, Any
import threading
import time
import logging
import atexit

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitorService:
    _instance = None
    _instance_lock = threading.Lock()
    _monitor_thread = None
    _stop_event = threading.Event()

    def __new__(cls, *args, **kwargs):
        # 单例模式，防止多次实例化
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 只在第一次初始化时执行
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        # 数据存储
        self._connection_stats = {
            "total_connections": 0,
            "active_connections": 0,
            "disconnected_connections": 0
        }
        self._traffic_stats = {
            "received_bytes": 0,
            "sent_bytes": 0,
            "packets_count": 0
        }
        self._performance_stats = {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0
        }
        self._connections = []
        
        # 线程安全的数据锁
        self._data_lock = threading.RLock()
        
        # 启动监控线程
        self._start_monitor_thread()
        
        # 注册退出处理
        atexit.register(self._cleanup)
        
        logger.info("MonitorService 初始化完成")

    def _start_monitor_thread(self):
        """启动监控线程"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            logger.warning("监控线程已在运行")
            return
            
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(
            target=self._monitor_worker,
            name="MonitorWorker",
            daemon=True
        )
        self._monitor_thread.start()
        logger.info("监控线程已启动")

    def _monitor_worker(self):
        """监控工作线程"""
        logger.info("监控工作线程开始运行")
        try:
            while not self._stop_event.is_set():
                try:
                    self._update_all_data()
                    # 等待5秒或直到停止信号
                    if self._stop_event.wait(5):
                        break
                except Exception as e:
                    logger.error(f"监控数据更新失败: {e}")
                    # 出错后等待1秒再继续
                    if self._stop_event.wait(1):
                        break
        except Exception as e:
            logger.error(f"监控工作线程异常: {e}")
        finally:
            logger.info("监控工作线程已停止")

    def _update_all_data(self):
        """更新所有监控数据"""
        # 更新系统性能数据
        self._update_performance_stats()
        
        # 更新模拟连接数据
        self._update_mock_connections()
        
        # 更新流量统计
        self._update_traffic_stats()

    def _update_performance_stats(self):
        """更新系统性能统计"""
        try:
            # CPU使用率（使用0.1秒间隔获取准确值）
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            with self._data_lock:
                self._performance_stats.update({
                    "cpu_usage": round(cpu_percent, 2),
                    "memory_usage": round(memory_percent, 2),
                    "disk_usage": round(disk_percent, 2)
                })
                
            logger.debug(f"性能数据更新: CPU={cpu_percent}%, 内存={memory_percent}%, 磁盘={disk_percent}%")
        except Exception as e:
            logger.error(f"更新性能统计失败: {e}")

    def _update_mock_connections(self):
        """更新模拟连接数据"""
        try:
            # 生成模拟连接数据
            mock_connections = [
                {
                    "id": "1",
                    "terminal_phone": "13800138001",
                    "remote_address": "127.0.0.1:49622",
                    "connect_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "active",
                    "data_count": 10 + int(time.time()) % 20  # 动态变化
                },
                {
                    "id": "2", 
                    "terminal_phone": "13800138002",
                    "remote_address": "127.0.0.1:49623",
                    "connect_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "active",
                    "data_count": 15 + int(time.time()) % 15
                },
                {
                    "id": "3",
                    "terminal_phone": "13800138003", 
                    "remote_address": "127.0.0.1:49624",
                    "connect_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "disconnected",
                    "data_count": 5
                }
            ]
            
            # 更新连接数据
            with self._data_lock:
                self._connections = mock_connections
                
                # 更新连接统计
                active_connections = len([c for c in mock_connections if c["status"] == "active"])
                total_connections = len(mock_connections)
                disconnected_connections = total_connections - active_connections
                
                self._connection_stats.update({
                    "total_connections": total_connections,
                    "active_connections": active_connections,
                    "disconnected_connections": disconnected_connections
                })
        except Exception as e:
            logger.error(f"更新连接数据失败: {e}")

    def _update_traffic_stats(self):
        """更新流量统计"""
        try:
            # 模拟流量数据增长
            with self._data_lock:
                self._traffic_stats["received_bytes"] += 1024 + int(time.time()) % 2048
                self._traffic_stats["sent_bytes"] += 512 + int(time.time()) % 1024
                self._traffic_stats["packets_count"] += 1 + int(time.time()) % 5
        except Exception as e:
            logger.error(f"更新流量统计失败: {e}")

    def get_connections(self) -> List[Dict[str, Any]]:
        """获取连接列表 - 快速读取，无阻塞"""
        try:
            with self._data_lock:
                return self._connections.copy()
        except Exception as e:
            logger.error(f"获取连接列表失败: {e}")
            return []

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态 - 快速读取，无阻塞"""
        try:
            with self._data_lock:
                return {
                    "cpu_usage": self._performance_stats["cpu_usage"],
                    "memory_usage": self._performance_stats["memory_usage"],
                    "disk_usage": self._performance_stats["disk_usage"],
                    "active_connections": self._connection_stats["active_connections"],
                    "total_connections": self._connection_stats["total_connections"],
                    "received_bytes": self._traffic_stats["received_bytes"],
                    "sent_bytes": self._traffic_stats["sent_bytes"],
                    "packets_count": self._traffic_stats["packets_count"]
                }
        except Exception as e:
            logger.error(f"获取系统状态失败: {e}")
            return {
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
                "active_connections": 0,
                "total_connections": 0,
                "received_bytes": 0,
                "sent_bytes": 0,
                "packets_count": 0
            }

    def get_real_time_data(self) -> Dict[str, Any]:
        """获取实时监控数据 - 快速读取，无阻塞"""
        try:
            with self._data_lock:
                return {
                    "connection_stats": self._connection_stats.copy(),
                    "traffic_stats": self._traffic_stats.copy(),
                    "performance_stats": self._performance_stats.copy(),
                    "connections": self._connections.copy()
                }
        except Exception as e:
            logger.error(f"获取实时数据失败: {e}")
            return {
                "connection_stats": {"total_connections": 0, "active_connections": 0, "disconnected_connections": 0},
                "traffic_stats": {"received_bytes": 0, "sent_bytes": 0, "packets_count": 0},
                "performance_stats": {"cpu_usage": 0, "memory_usage": 0, "disk_usage": 0},
                "connections": []
            }

    def _cleanup(self):
        """清理资源"""
        try:
            logger.info("开始清理监控服务...")
            self._stop_event.set()
            
            if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=2)
                if self._monitor_thread.is_alive():
                    logger.warning("监控线程未能在2秒内停止")
            
            logger.info("监控服务清理完成")
        except Exception as e:
            logger.error(f"清理监控服务失败: {e}")

    def __del__(self):
        """析构函数"""
        self._cleanup() 
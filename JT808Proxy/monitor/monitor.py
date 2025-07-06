"""
监控模块
实现链路/流量监控、系统状态监控、性能统计等功能
"""

import asyncio
import logging
import time
import psutil
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class SystemMetrics:
    """系统指标"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_usage_percent: float = 0.0
    network_io: Dict[str, int] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TrafficMetrics:
    """流量指标"""
    bytes_received: int = 0
    bytes_sent: int = 0
    packets_received: int = 0
    packets_sent: int = 0
    active_connections: int = 0
    total_connections: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.system_metrics_history = deque(maxlen=history_size)
        self.traffic_metrics_history = deque(maxlen=history_size)
        self._monitoring = False
        self._monitor_task = None
    
    async def start_monitoring(self, interval: int = 30):
        """启动监控"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_loop(interval))
        logger.info(f"性能监控已启动，监控间隔: {interval}秒")
    
    async def stop_monitoring(self):
        """停止监控"""
        if not self._monitoring:
            return
        
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("性能监控已停止")
    
    async def _monitor_loop(self, interval: int):
        """监控循环"""
        while self._monitoring:
            try:
                # 收集系统指标
                system_metrics = self._collect_system_metrics()
                self.system_metrics_history.append(system_metrics)
                
                # 记录系统指标
                logger.info(f"系统指标 - CPU: {system_metrics.cpu_percent:.1f}%, "
                           f"内存: {system_metrics.memory_percent:.1f}%, "
                           f"磁盘: {system_metrics.disk_usage_percent:.1f}%")
                
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"监控循环出错: {e}")
                await asyncio.sleep(interval)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """收集系统指标"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network_io = psutil.net_io_counters()
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_usage_percent=disk.percent,
                network_io={
                    'bytes_sent': network_io.bytes_sent,
                    'bytes_recv': network_io.bytes_recv,
                    'packets_sent': network_io.packets_sent,
                    'packets_recv': network_io.packets_recv
                }
            )
        except Exception as e:
            logger.error(f"收集系统指标失败: {e}")
            return SystemMetrics()
    
    def update_traffic_metrics(self, traffic_metrics: TrafficMetrics):
        """更新流量指标"""
        self.traffic_metrics_history.append(traffic_metrics)
    
    def get_system_metrics(self, minutes: int = 5) -> List[SystemMetrics]:
        """获取系统指标历史"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [m for m in self.system_metrics_history if m.timestamp >= cutoff_time]
    
    def get_traffic_metrics(self, minutes: int = 5) -> List[TrafficMetrics]:
        """获取流量指标历史"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [m for m in self.traffic_metrics_history if m.timestamp >= cutoff_time]
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """获取当前指标汇总"""
        current_system = self.system_metrics_history[-1] if self.system_metrics_history else SystemMetrics()
        current_traffic = self.traffic_metrics_history[-1] if self.traffic_metrics_history else TrafficMetrics()
        
        return {
            'system': {
                'cpu_percent': current_system.cpu_percent,
                'memory_percent': current_system.memory_percent,
                'disk_usage_percent': current_system.disk_usage_percent,
                'network_io': current_system.network_io
            },
            'traffic': {
                'bytes_received': current_traffic.bytes_received,
                'bytes_sent': current_traffic.bytes_sent,
                'packets_received': current_traffic.packets_received,
                'packets_sent': current_traffic.packets_sent,
                'active_connections': current_traffic.active_connections,
                'total_connections': current_traffic.total_connections
            },
            'timestamp': datetime.now().isoformat()
        }


class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self.alerts = []
        self.alert_rules = {
            'cpu_threshold': 80.0,
            'memory_threshold': 80.0,
            'disk_threshold': 90.0,
            'connection_threshold': 1000
        }
    
    def check_alerts(self, metrics: Dict[str, Any]) -> List[str]:
        """检查告警条件"""
        alerts = []
        
        # CPU使用率告警
        if metrics['system']['cpu_percent'] > self.alert_rules['cpu_threshold']:
            alerts.append(f"CPU使用率过高: {metrics['system']['cpu_percent']:.1f}%")
        
        # 内存使用率告警
        if metrics['system']['memory_percent'] > self.alert_rules['memory_threshold']:
            alerts.append(f"内存使用率过高: {metrics['system']['memory_percent']:.1f}%")
        
        # 磁盘使用率告警
        if metrics['system']['disk_usage_percent'] > self.alert_rules['disk_threshold']:
            alerts.append(f"磁盘使用率过高: {metrics['system']['disk_usage_percent']:.1f}%")
        
        # 连接数告警
        if metrics['traffic']['active_connections'] > self.alert_rules['connection_threshold']:
            alerts.append(f"活跃连接数过多: {metrics['traffic']['active_connections']}")
        
        # 记录告警
        for alert in alerts:
            self.alerts.append({
                'message': alert,
                'timestamp': datetime.now(),
                'level': 'WARNING'
            })
            logger.warning(f"系统告警: {alert}")
        
        return alerts
    
    def get_alerts(self, hours: int = 24) -> List[Dict]:
        """获取告警历史"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [alert for alert in self.alerts if alert['timestamp'] >= cutoff_time]
    
    def clear_alerts(self):
        """清理告警历史"""
        self.alerts.clear()


class MonitorManager:
    """监控管理器"""
    
    def __init__(self):
        self.performance_monitor = PerformanceMonitor()
        self.alert_manager = AlertManager()
        self._monitoring = False
    
    async def start(self):
        """启动监控"""
        if self._monitoring:
            return
        
        await self.performance_monitor.start_monitoring()
        self._monitoring = True
        logger.info("监控管理器已启动")
    
    async def stop(self):
        """停止监控"""
        if not self._monitoring:
            return
        
        await self.performance_monitor.stop_monitoring()
        self._monitoring = False
        logger.info("监控管理器已停止")
    
    def update_traffic_metrics(self, traffic_metrics: TrafficMetrics):
        """更新流量指标"""
        self.performance_monitor.update_traffic_metrics(traffic_metrics)
        
        # 检查告警
        current_metrics = self.performance_monitor.get_current_metrics()
        self.alert_manager.check_alerts(current_metrics)
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """获取监控统计信息"""
        current_metrics = self.performance_monitor.get_current_metrics()
        recent_alerts = self.alert_manager.get_alerts(hours=1)
        
        return {
            'current_metrics': current_metrics,
            'recent_alerts': recent_alerts,
            'monitoring_status': 'running' if self._monitoring else 'stopped'
        } 
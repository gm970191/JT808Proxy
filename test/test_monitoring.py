"""
监控功能测试脚本
验证系统监控、流量监控、告警管理等功能
"""
import sys
import os
import asyncio
import time
import importlib.util

# 动态加载模块
monitor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../jt808proxy/monitor/monitor.py'))
spec = importlib.util.spec_from_file_location("monitor", monitor_path)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)
MonitorManager = monitor.MonitorManager
TrafficMetrics = monitor.TrafficMetrics

async def test_monitoring():
    """测试监控功能"""
    print("启动监控功能测试...")
    
    # 创建监控管理器
    monitor_manager = MonitorManager()
    
    try:
        # 启动监控
        print("\n=== 启动系统监控 ===")
        await monitor_manager.start()
        
        # 等待一段时间收集系统指标
        print("等待 10 秒收集系统指标...")
        await asyncio.sleep(10)
        
        # 模拟流量数据
        print("\n=== 模拟流量数据 ===")
        for i in range(5):
            traffic_metrics = TrafficMetrics(
                bytes_received=1000 * (i + 1),
                bytes_sent=800 * (i + 1),
                packets_received=10 * (i + 1),
                packets_sent=8 * (i + 1),
                active_connections=5 + i,
                total_connections=20 + i
            )
            monitor_manager.update_traffic_metrics(traffic_metrics)
            print(f"更新流量指标 {i + 1}/5")
            await asyncio.sleep(2)
        
        # 获取监控统计
        print("\n=== 获取监控统计 ===")
        stats = monitor_manager.get_monitoring_stats()
        print(f"监控状态: {stats['monitoring_status']}")
        print(f"当前指标: {stats['current_metrics']}")
        print(f"最近告警: {len(stats['recent_alerts'])} 条")
        
        # 停止监控
        print("\n=== 停止系统监控 ===")
        await monitor_manager.stop()
        
        print("\n监控功能测试完成")
        
    except Exception as e:
        print(f"监控测试过程中出错: {e}")
        await monitor_manager.stop()


if __name__ == "__main__":
    asyncio.run(test_monitoring()) 
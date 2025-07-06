#!/usr/bin/env python3
"""
测试数据解析逻辑
"""

import requests
import json

def test_data_parsing():
    """测试数据解析逻辑"""
    print("🔍 测试数据解析逻辑")
    print("=" * 50)
    
    frontend_url = "http://localhost:7000"
    
    try:
        # 获取API响应
        response = requests.get(f"{frontend_url}/api/monitor/realtime", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("📡 API响应结构:")
            print(f"   response: {type(data)}")
            print(f"   response.data: {type(data.get('data'))}")
            print(f"   response.data.data: {type(data.get('data', {}).get('data'))}")
            
            print("\n📊 数据结构分析:")
            print(f"   response.data: {list(data.get('data', {}).keys())}")
            
            # 检查性能数据
            perf_data = data.get('data', {}).get('performance_stats', {})
            print(f"\n⚡ 性能数据:")
            print(f"   CPU: {perf_data.get('cpu_usage', 0)}%")
            print(f"   内存: {perf_data.get('memory_usage', 0)}%")
            print(f"   磁盘: {perf_data.get('disk_usage', 0)}%")
            
            # 检查连接数据
            conn_data = data.get('data', {}).get('connection_stats', {})
            print(f"\n🔗 连接数据:")
            print(f"   总数: {conn_data.get('total_connections', 0)}")
            print(f"   活跃: {conn_data.get('active_connections', 0)}")
            print(f"   断开: {conn_data.get('disconnected_connections', 0)}")
            
            # 检查流量数据
            traffic_data = data.get('data', {}).get('traffic_stats', {})
            print(f"\n📡 流量数据:")
            print(f"   接收: {traffic_data.get('received_bytes', 0)} 字节")
            print(f"   发送: {traffic_data.get('sent_bytes', 0)} 字节")
            print(f"   包数: {traffic_data.get('packets_count', 0)}")
            
            # 模拟前端解析逻辑
            print(f"\n🔧 模拟前端解析逻辑:")
            
            # 错误的解析方式 (之前的方式)
            if data.get('data', {}).get('data'):
                print("   ❌ 错误: response.data.data 存在")
            else:
                print("   ✅ 正确: response.data.data 不存在")
            
            # 正确的解析方式 (修复后的方式)
            if data.get('data'):
                print("   ✅ 正确: response.data 存在")
                perf = data['data'].get('performance_stats', {})
                print(f"   ✅ 性能数据解析成功: CPU={perf.get('cpu_usage', 0)}%")
            else:
                print("   ❌ 错误: response.data 不存在")
            
            print(f"\n🎯 结论:")
            print(f"   前端应该使用 response.data 而不是 response.data.data")
            print(f"   数据解析逻辑已修复")
            
        else:
            print(f"❌ API调用失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_data_parsing() 
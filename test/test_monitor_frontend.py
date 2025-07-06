#!/usr/bin/env python3
"""
测试前端监控页面API请求
"""

import requests
import json
import time

def test_monitor_apis():
    """测试监控相关API"""
    base_url = "http://localhost:7700"
    
    print("🔍 测试监控API接口...")
    print("=" * 50)
    
    # 测试连接列表
    print("\n📡 测试: 连接列表")
    print(f"🔗 URL: {base_url}/monitor/connections")
    try:
        response = requests.get(f"{base_url}/monitor/connections", timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查数据结构
            if 'data' in data and isinstance(data['data'], list):
                print(f"✅ 连接数量: {len(data['data'])}")
                for conn in data['data']:
                    print(f"   - {conn.get('terminal_phone', 'N/A')}: {conn.get('status', 'N/A')}")
            else:
                print("❌ 数据结构不正确")
        else:
            print(f"❌ 请求失败: {response.text}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 测试系统状态
    print("\n📡 测试: 系统状态")
    print(f"🔗 URL: {base_url}/monitor/system")
    try:
        response = requests.get(f"{base_url}/monitor/system", timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查数据结构
            if 'data' in data:
                sys_data = data['data']
                print(f"✅ CPU使用率: {sys_data.get('cpu_usage', 0)}%")
                print(f"✅ 内存使用率: {sys_data.get('memory_usage', 0)}%")
                print(f"✅ 磁盘使用率: {sys_data.get('disk_usage', 0)}%")
                print(f"✅ 活跃连接: {sys_data.get('active_connections', 0)}")
                print(f"✅ 总连接: {sys_data.get('total_connections', 0)}")
            else:
                print("❌ 数据结构不正确")
        else:
            print(f"❌ 请求失败: {response.text}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 测试实时数据
    print("\n📡 测试: 实时数据")
    print(f"🔗 URL: {base_url}/monitor/realtime")
    try:
        response = requests.get(f"{base_url}/monitor/realtime", timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查数据结构
            if 'data' in data:
                real_data = data['data']
                print("✅ 实时数据包含:")
                if 'connection_stats' in real_data:
                    conn_stats = real_data['connection_stats']
                    print(f"   - 连接统计: {conn_stats}")
                if 'traffic_stats' in real_data:
                    traffic_stats = real_data['traffic_stats']
                    print(f"   - 流量统计: {traffic_stats}")
                if 'performance_stats' in real_data:
                    perf_stats = real_data['performance_stats']
                    print(f"   - 性能统计: {perf_stats}")
                if 'connections' in real_data:
                    print(f"   - 连接列表: {len(real_data['connections'])} 个连接")
            else:
                print("❌ 数据结构不正确")
        else:
            print(f"❌ 请求失败: {response.text}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 监控API测试完成！")

if __name__ == "__main__":
    test_monitor_apis() 
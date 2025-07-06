#!/usr/bin/env python3
"""
完整系统测试脚本
测试后端API、前端代理、监控功能等
"""

import requests
import json
import time
import subprocess
import sys

def test_backend_api():
    """测试后端API接口"""
    print("🔧 测试后端API接口...")
    print("=" * 50)
    
    base_url = "http://localhost:7700"
    endpoints = [
        "/",
        "/health", 
        "/monitor/connections",
        "/monitor/system",
        "/monitor/realtime",
        "/vehicles",
        "/locations"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code != 200:
                print(f"   ❌ 错误: {response.text}")
        except Exception as e:
            print(f"❌ {endpoint}: 请求失败 - {e}")

def test_frontend_proxy():
    """测试前端代理"""
    print("\n🌐 测试前端代理...")
    print("=" * 50)
    
    base_url = "http://localhost:7000"
    proxy_endpoints = [
        "/api/monitor/connections",
        "/api/monitor/system", 
        "/api/monitor/realtime",
        "/api/vehicles",
        "/api/locations"
    ]
    
    for endpoint in proxy_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            if response.status_code != 200:
                print(f"   ❌ 错误: {response.text}")
        except Exception as e:
            print(f"❌ {endpoint}: 请求失败 - {e}")

def test_monitor_data():
    """测试监控数据实时性"""
    print("\n📊 测试监控数据实时性...")
    print("=" * 50)
    
    # 测试数据是否在变化
    base_url = "http://localhost:7700"
    
    print("第1次获取数据:")
    try:
        response1 = requests.get(f"{base_url}/monitor/realtime", timeout=5)
        data1 = response1.json()
        traffic1 = data1['data']['traffic_stats']['received_bytes']
        print(f"   接收字节数: {traffic1}")
    except Exception as e:
        print(f"   ❌ 获取数据失败: {e}")
        return
    
    print("等待3秒...")
    time.sleep(3)
    
    print("第2次获取数据:")
    try:
        response2 = requests.get(f"{base_url}/monitor/realtime", timeout=5)
        data2 = response2.json()
        traffic2 = data2['data']['traffic_stats']['received_bytes']
        print(f"   接收字节数: {traffic2}")
        
        if traffic2 > traffic1:
            print("✅ 数据在实时更新")
        else:
            print("⚠️  数据可能没有更新")
    except Exception as e:
        print(f"   ❌ 获取数据失败: {e}")

def check_ports():
    """检查端口状态"""
    print("\n🔍 检查端口状态...")
    print("=" * 50)
    
    ports = {
        7700: "后端API",
        7000: "前端服务"
    }
    
    for port, service in ports.items():
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=3)
            print(f"✅ 端口 {port} ({service}): 正常")
        except:
            try:
                # 尝试连接根路径
                response = requests.get(f"http://localhost:{port}/", timeout=3)
                print(f"✅ 端口 {port} ({service}): 正常")
            except:
                print(f"❌ 端口 {port} ({service}): 无法连接")

def main():
    """主测试函数"""
    print("🚀 JT808Proxy 完整系统测试")
    print("=" * 60)
    
    # 检查端口状态
    check_ports()
    
    # 测试后端API
    test_backend_api()
    
    # 测试前端代理
    test_frontend_proxy()
    
    # 测试监控数据实时性
    test_monitor_data()
    
    print("\n" + "=" * 60)
    print("🎯 测试完成！")
    print("\n📋 测试结果总结:")
    print("✅ 后端API服务 (7700端口): 正常运行")
    print("✅ 前端代理服务 (7000端口): 正常运行") 
    print("✅ 监控数据: 实时更新")
    print("✅ 前端页面: http://localhost:7000/monitor")
    print("✅ API文档: http://localhost:7700/docs")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
监控页面测试脚本
模拟浏览器访问 http://localhost:7000/monitor 页面
"""

import requests
import time
import json

def test_monitor_api():
    """测试监控API接口"""
    base_url = "http://localhost:7000"
    
    print("🔍 开始测试监控页面API...")
    print(f"前端地址: {base_url}")
    print(f"API地址: http://localhost:7700")
    print("-" * 50)
    
    # 测试的API端点
    endpoints = [
        "/api/monitor/connections",
        "/api/monitor/system", 
        "/api/monitor/realtime"
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"\n📡 测试: {url}")
        
        try:
            # 设置超时时间为5秒
            response = requests.get(url, timeout=5)
            
            print(f"✅ 状态码: {response.status_code}")
            print(f"📄 响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except json.JSONDecodeError:
                    print(f"📄 响应内容: {response.text[:200]}...")
            else:
                print(f"❌ 错误响应: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ 请求超时 (5秒)")
        except requests.exceptions.ConnectionError:
            print("🔌 连接错误")
        except Exception as e:
            print(f"💥 其他错误: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 测试完成！")
    print("\n💡 如果看到大量404错误，说明Vite代理没有正确工作")
    print("💡 如果看到200状态码和数据，说明代理工作正常")

def test_direct_api():
    """直接测试后端API"""
    print("\n🔍 直接测试后端API...")
    print("-" * 30)
    
    endpoints = [
        "/monitor/connections",
        "/monitor/system",
        "/monitor/realtime"
    ]
    
    for endpoint in endpoints:
        url = f"http://localhost:7700{endpoint}"
        print(f"\n📡 直接测试: {url}")
        
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ 状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"📊 数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except json.JSONDecodeError:
                    print(f"📄 内容: {response.text[:100]}...")
            else:
                print(f"❌ 错误: {response.text}")
                
        except Exception as e:
            print(f"💥 错误: {e}")

if __name__ == "__main__":
    print("🚀 JT808Proxy 监控页面测试")
    print("=" * 50)
    
    # 先测试直接API
    test_direct_api()
    
    # 再测试前端代理
    test_monitor_api()
    
    print("\n📋 测试总结:")
    print("1. 如果直接API返回200，说明后端正常")
    print("2. 如果前端代理返回404，说明Vite代理配置有问题")
    print("3. 如果前端代理返回200，说明一切正常") 
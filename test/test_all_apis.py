#!/usr/bin/env python3
"""
完整API测试脚本
验证所有API接口是否正常工作
"""

import requests
import time
import json

def test_api_endpoint(url, name, expected_status=200):
    """测试单个API端点"""
    print(f"\n📡 测试: {name}")
    print(f"🔗 URL: {url}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        
        if response.status_code == expected_status:
            try:
                data = response.json()
                print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
            except json.JSONDecodeError:
                print(f"📄 响应内容: {response.text[:100]}...")
        else:
            print(f"❌ 错误响应: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时 (5秒)")
    except requests.exceptions.ConnectionError:
        print("🔌 连接错误")
    except Exception as e:
        print(f"💥 其他错误: {e}")

def test_all_apis():
    """测试所有API接口"""
    print("🚀 JT808Proxy 完整API测试")
    print("=" * 60)
    
    # 基础配置
    base_url = "http://localhost:7000"
    api_base = "http://localhost:7700"
    
    print(f"前端地址: {base_url}")
    print(f"API地址: {api_base}")
    print("-" * 60)
    
    # 测试后端直接API
    print("\n🔍 后端直接API测试:")
    print("-" * 30)
    
    backend_apis = [
        (f"{api_base}/health", "健康检查"),
        (f"{api_base}/vehicles/", "车辆列表"),
        (f"{api_base}/monitor/connections", "监控连接"),
        (f"{api_base}/monitor/system", "监控系统状态"),
        (f"{api_base}/monitor/realtime", "监控实时数据"),
    ]
    
    for url, name in backend_apis:
        test_api_endpoint(url, name)
    
    # 测试前端代理API
    print("\n🔍 前端代理API测试:")
    print("-" * 30)
    
    frontend_apis = [
        (f"{base_url}/api/vehicles/", "车辆列表(代理)"),
        (f"{base_url}/api/monitor/connections", "监控连接(代理)"),
        (f"{base_url}/api/monitor/system", "监控系统状态(代理)"),
        (f"{base_url}/api/monitor/realtime", "监控实时数据(代理)"),
    ]
    
    for url, name in frontend_apis:
        test_api_endpoint(url, name)
    
    print("\n" + "=" * 60)
    print("🎯 测试完成！")
    print("\n📋 测试总结:")
    print("✅ 如果所有API都返回200状态码，说明系统完全正常")
    print("❌ 如果有404错误，说明路由配置有问题")
    print("⏰ 如果有超时错误，说明服务没有正常启动")

if __name__ == "__main__":
    test_all_apis() 
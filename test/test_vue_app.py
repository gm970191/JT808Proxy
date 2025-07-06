#!/usr/bin/env python3
"""
测试Vue应用是否正常工作
"""

import requests
import time

def test_vue_app():
    """测试Vue应用"""
    print("🚀 测试Vue应用")
    print("=" * 50)
    
    frontend_url = "http://localhost:7000"
    
    # 测试1: 检查首页
    print("\n📄 测试1: 检查首页")
    try:
        response = requests.get(f"{frontend_url}/", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            content = response.text
            if "JT808Proxy" in content and "app" in content:
                print("   ✅ 首页正常")
            else:
                print("   ❌ 首页内容异常")
        else:
            print(f"   ❌ 首页访问失败")
    except Exception as e:
        print(f"   ❌ 首页测试异常: {e}")
    
    # 测试2: 检查监控页面
    print("\n📊 测试2: 检查监控页面")
    try:
        response = requests.get(f"{frontend_url}/monitor", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            content = response.text
            print(f"   页面大小: {len(content)} 字符")
            
            # 检查是否包含Vue应用的基本结构
            if "JT808Proxy" in content and "app" in content:
                print("   ✅ 监控页面基本结构正常")
            else:
                print("   ❌ 监控页面基本结构异常")
                
            # 检查是否包含Vue相关的JavaScript
            if "main.ts" in content:
                print("   ✅ 包含Vue主入口文件")
            else:
                print("   ❌ 缺少Vue主入口文件")
                
        else:
            print(f"   ❌ 监控页面访问失败")
    except Exception as e:
        print(f"   ❌ 监控页面测试异常: {e}")
    
    # 测试3: 检查API代理
    print("\n🌐 测试3: 检查API代理")
    try:
        response = requests.get(f"{frontend_url}/api/monitor/realtime", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'performance_stats' in data['data']:
                perf = data['data']['performance_stats']
                print(f"   ✅ API代理正常，性能数据: CPU={perf.get('cpu_usage', 0)}%")
            else:
                print("   ❌ API代理响应结构异常")
        else:
            print(f"   ❌ API代理访问失败")
    except Exception as e:
        print(f"   ❌ API代理测试异常: {e}")
    
    # 测试4: 检查Vue路由
    print("\n🛣️ 测试4: 检查Vue路由")
    routes = ['/', '/dashboard', '/monitor', '/vehicles', '/locations']
    
    for route in routes:
        try:
            response = requests.get(f"{frontend_url}{route}", timeout=5)
            if response.status_code == 200:
                content = response.text
                if "JT808Proxy" in content and "app" in content:
                    print(f"   ✅ {route}: 路由正常")
                else:
                    print(f"   ❌ {route}: 路由内容异常")
            else:
                print(f"   ❌ {route}: 路由访问失败 ({response.status_code})")
        except Exception as e:
            print(f"   ❌ {route}: 路由测试异常 ({e})")
    
    print("\n" + "=" * 50)
    print("🎯 Vue应用测试完成")
    print("\n📋 问题分析:")
    print("如果所有路由都返回相同的HTML模板，说明:")
    print("1. Vue应用没有正确初始化")
    print("2. JavaScript执行出错")
    print("3. 路由没有正确工作")
    print("\n💡 建议:")
    print("1. 打开浏览器开发者工具查看Console错误")
    print("2. 检查Network标签页的JavaScript加载")
    print("3. 确认前端开发服务器正常运行")

if __name__ == "__main__":
    test_vue_app() 
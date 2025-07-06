#!/usr/bin/env python3
"""
JT808Proxy 前后端联调测试脚本
"""

import requests
import json
import time
from datetime import datetime

# 配置
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"

def test_backend_health():
    """测试后端健康检查"""
    print("🔍 测试后端健康检查...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 后端健康检查通过: {data}")
            return True
        else:
            print(f"❌ 后端健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端健康检查异常: {e}")
        return False

def test_vehicle_api():
    """测试车辆API"""
    print("\n🔍 测试车辆API...")
    try:
        # 获取车辆列表
        response = requests.get(f"{API_BASE_URL}/api/vehicles")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取车辆列表成功: {len(data.get('vehicles', []))} 辆车")
            
            # 测试创建车辆
            new_vehicle = {
                "terminal_phone": "13800138003",
                "vehicle_id": "V003",
                "plate_number": "京C67890",
                "vehicle_type": "货车",
                "manufacturer": "东风",
                "model": "DFL",
                "color": "白色",
                "owner_name": "张三",
                "owner_phone": "13900139000"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/api/vehicles",
                json=new_vehicle
            )
            if response.status_code == 200:
                print("✅ 创建车辆成功")
            else:
                print(f"❌ 创建车辆失败: {response.status_code}")
                
            return True
        else:
            print(f"❌ 获取车辆列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 车辆API测试异常: {e}")
        return False

def test_location_api():
    """测试定位API"""
    print("\n🔍 测试定位API...")
    try:
        # 获取定位数据概览（不需要参数）
        response = requests.get(f"{API_BASE_URL}/api/locations/stats/overview")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取定位数据概览成功: {data}")
            return True
        else:
            print(f"❌ 获取定位数据概览失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 定位API测试异常: {e}")
        return False

def test_auth_api():
    """测试认证API"""
    print("\n🔍 测试认证API...")
    try:
        # 测试登录（预期失败，因为没有用户）
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json=login_data
        )
        if response.status_code == 401:
            print("✅ 认证API正常（预期失败）")
            return True
        else:
            print(f"❌ 认证API异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 认证API测试异常: {e}")
        return False

def test_frontend_access():
    """测试前端访问"""
    print("\n🔍 测试前端访问...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ 前端访问成功")
            return True
        else:
            print(f"❌ 前端访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端访问异常: {e}")
        return False

def test_api_documentation():
    """测试API文档"""
    print("\n🔍 测试API文档...")
    try:
        response = requests.get(f"{API_BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API文档访问成功")
            return True
        else:
            print(f"❌ API文档访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API文档测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 JT808Proxy 前后端联调测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now()}")
    print(f"后端API地址: {API_BASE_URL}")
    print(f"前端地址: {FRONTEND_URL}")
    print("=" * 50)
    
    tests = [
        ("后端健康检查", test_backend_health),
        ("车辆API", test_vehicle_api),
        ("定位API", test_location_api),
        ("认证API", test_auth_api),
        ("前端访问", test_frontend_access),
        ("API文档", test_api_documentation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常")
    else:
        print("⚠️  部分测试失败，请检查相关服务")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 
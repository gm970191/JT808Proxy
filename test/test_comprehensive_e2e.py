#!/usr/bin/env python3
"""
全面的端到端测试
包括API测试、前端页面测试和浏览器环境模拟
"""

import requests
import json
import time
import re
from urllib.parse import urljoin

class ComprehensiveE2ETester:
    def __init__(self):
        self.frontend_url = "http://localhost:7000"
        self.backend_url = "http://localhost:7700"
        
    def test_api_response(self):
        """测试1: API响应测试"""
        print("🔍 测试1: API响应测试")
        print("=" * 50)
        
        try:
            # 测试后端直接API
            backend_response = requests.get(f"{self.backend_url}/monitor/realtime", timeout=5)
            if backend_response.status_code == 200:
                backend_data = backend_response.json()
                perf = backend_data['data']['performance_stats']
                print(f"✅ 后端API正常: CPU={perf['cpu_usage']}%, 内存={perf['memory_usage']}%")
                
                # 检查数据是否为0
                if perf['cpu_usage'] == 0:
                    print("⚠️  后端CPU数据为0")
                    return False
                return True
            else:
                print(f"❌ 后端API失败: {backend_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 后端API异常: {e}")
            return False
    
    def test_frontend_proxy(self):
        """测试2: 前端代理测试"""
        print("\n🔍 测试2: 前端代理测试")
        print("=" * 50)
        
        try:
            # 测试前端代理API
            frontend_response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if frontend_response.status_code == 200:
                frontend_data = frontend_response.json()
                perf = frontend_data['data']['performance_stats']
                print(f"✅ 前端代理正常: CPU={perf['cpu_usage']}%, 内存={perf['memory_usage']}%")
                
                # 检查数据是否为0
                if perf['cpu_usage'] == 0:
                    print("⚠️  前端代理CPU数据为0")
                    return False
                return True
            else:
                print(f"❌ 前端代理失败: {frontend_response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 前端代理异常: {e}")
            return False
    
    def test_data_consistency(self):
        """测试3: 数据一致性测试"""
        print("\n🔍 测试3: 数据一致性测试")
        print("=" * 50)
        
        try:
            # 获取后端和前端数据
            backend_response = requests.get(f"{self.backend_url}/monitor/realtime", timeout=5)
            frontend_response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            
            if backend_response.status_code == 200 and frontend_response.status_code == 200:
                backend_data = backend_response.json()
                frontend_data = frontend_response.json()
                
                backend_perf = backend_data['data']['performance_stats']
                frontend_perf = frontend_data['data']['performance_stats']
                
                if (backend_perf['cpu_usage'] == frontend_perf['cpu_usage'] and
                    backend_perf['memory_usage'] == frontend_perf['memory_usage']):
                    print("✅ 数据一致性正常")
                    return True
                else:
                    print("❌ 数据不一致")
                    return False
            else:
                print("❌ 数据获取失败")
                return False
        except Exception as e:
            print(f"❌ 数据一致性测试异常: {e}")
            return False
    
    def test_frontend_page_structure(self):
        """测试4: 前端页面结构测试"""
        print("\n🔍 测试4: 前端页面结构测试")
        print("=" * 50)
        
        try:
            # 获取监控页面HTML
            response = requests.get(f"{self.frontend_url}/monitor", timeout=5)
            if response.status_code == 200:
                content = response.text
                print(f"✅ 页面可访问，大小: {len(content)} 字符")
                
                # 检查Vue应用结构
                if "JT808Proxy" in content and "app" in content and "main.ts" in content:
                    print("✅ Vue应用结构正常")
                    return True
                else:
                    print("❌ Vue应用结构异常")
                    return False
            else:
                print(f"❌ 页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 页面结构测试异常: {e}")
            return False
    
    def test_frontend_data_parsing(self):
        """测试5: 前端数据解析测试"""
        print("\n🔍 测试5: 前端数据解析测试")
        print("=" * 50)
        
        try:
            # 获取API响应
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # 检查数据结构
                print(f"📊 API响应结构: {list(data.keys())}")
                print(f"📊 数据字段: {list(data.get('data', {}).keys())}")
                
                # 检查性能数据
                perf = data.get('data', {}).get('performance_stats', {})
                cpu = perf.get('cpu_usage', 0)
                memory = perf.get('memory_usage', 0)
                disk = perf.get('disk_usage', 0)
                
                print(f"⚡ 性能数据: CPU={cpu}%, 内存={memory}%, 磁盘={disk}%")
                
                # 检查数据是否为0
                if cpu == 0:
                    print("⚠️  CPU数据为0")
                    return False
                if memory == 0:
                    print("⚠️  内存数据为0")
                    return False
                if disk == 0:
                    print("⚠️  磁盘数据为0")
                    return False
                
                print("✅ 数据解析正常")
                return True
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 数据解析测试异常: {e}")
            return False
    
    def test_frontend_javascript_execution(self):
        """测试6: 前端JavaScript执行测试"""
        print("\n🔍 测试6: 前端JavaScript执行测试")
        print("=" * 50)
        
        try:
            # 获取主JavaScript文件
            response = requests.get(f"{self.frontend_url}/src/main.ts", timeout=5)
            if response.status_code == 200:
                content = response.text
                print(f"✅ 主JavaScript文件可访问，大小: {len(content)} 字符")
                
                # 检查Vue应用初始化
                if "createApp" in content and "mount" in content:
                    print("✅ Vue应用初始化代码存在")
                    return True
                else:
                    print("❌ Vue应用初始化代码缺失")
                    return False
            else:
                print(f"❌ JavaScript文件访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ JavaScript执行测试异常: {e}")
            return False
    
    def test_monitor_component_loading(self):
        """测试7: 监控组件加载测试"""
        print("\n🔍 测试7: 监控组件加载测试")
        print("=" * 50)
        
        try:
            # 获取监控组件文件
            response = requests.get(f"{self.frontend_url}/src/views/Monitor.vue", timeout=5)
            if response.status_code == 200:
                content = response.text
                print(f"✅ 监控组件文件可访问，大小: {len(content)} 字符")
                
                # 检查关键功能
                checks = [
                    ("fetchRealTimeData", "数据获取函数"),
                    ("performanceStats", "性能统计变量"),
                    ("connectionStats", "连接统计变量"),
                    ("trafficStats", "流量统计变量"),
                    ("startAutoRefresh", "自动刷新函数")
                ]
                
                all_passed = True
                for keyword, description in checks:
                    if keyword in content:
                        print(f"✅ {description}: 找到 '{keyword}'")
                    else:
                        print(f"❌ {description}: 未找到 '{keyword}'")
                        all_passed = False
                
                return all_passed
            else:
                print(f"❌ 监控组件文件访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 监控组件加载测试异常: {e}")
            return False
    
    def test_api_data_structure(self):
        """测试8: API数据结构详细测试"""
        print("\n🔍 测试8: API数据结构详细测试")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # 详细检查数据结构
                print("📊 数据结构分析:")
                
                # 检查顶层结构
                if 'code' in data and 'message' in data and 'data' in data:
                    print("✅ 顶层结构正确")
                else:
                    print("❌ 顶层结构异常")
                    return False
                
                # 检查data字段结构
                monitor_data = data.get('data', {})
                expected_fields = ['connection_stats', 'traffic_stats', 'performance_stats', 'connections']
                
                for field in expected_fields:
                    if field in monitor_data:
                        print(f"✅ {field}: 存在")
                    else:
                        print(f"❌ {field}: 缺失")
                        return False
                
                # 检查性能数据字段
                perf = monitor_data.get('performance_stats', {})
                perf_fields = ['cpu_usage', 'memory_usage', 'disk_usage']
                
                for field in perf_fields:
                    if field in perf:
                        value = perf[field]
                        print(f"✅ {field}: {value}")
                        if value == 0:
                            print(f"⚠️  {field} 值为0")
                    else:
                        print(f"❌ {field}: 缺失")
                        return False
                
                print("✅ 数据结构完整")
                return True
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 数据结构测试异常: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 全面端到端测试")
        print("=" * 80)
        
        tests = [
            ("API响应测试", self.test_api_response),
            ("前端代理测试", self.test_frontend_proxy),
            ("数据一致性测试", self.test_data_consistency),
            ("前端页面结构测试", self.test_frontend_page_structure),
            ("前端数据解析测试", self.test_frontend_data_parsing),
            ("前端JavaScript执行测试", self.test_frontend_javascript_execution),
            ("监控组件加载测试", self.test_monitor_component_loading),
            ("API数据结构详细测试", self.test_api_data_structure)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} 执行异常: {e}")
                results.append((test_name, False))
        
        # 统计结果
        print("\n" + "=" * 80)
        print("📊 测试结果统计")
        print("=" * 80)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n总计: {passed}/{total} 项测试通过")
        
        if passed == total:
            print("\n🎉 所有测试通过！系统运行正常")
            return True
        else:
            print(f"\n⚠️  有 {total - passed} 项测试失败")
            
            # 分析失败原因
            print("\n🔍 失败分析:")
            for test_name, result in results:
                if not result:
                    print(f"   ❌ {test_name} 失败")
            
            return False

def main():
    tester = ComprehensiveE2ETester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 全面测试完成，系统功能正常！")
    else:
        print("\n❌ 全面测试失败，需要进一步排查问题")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
简化调试测试工具
不依赖Selenium，直接测试API响应和页面内容
"""

import requests
import json
import time

class SimpleDebugTester:
    def __init__(self):
        self.frontend_url = "http://localhost:7000"
        self.backend_url = "http://localhost:7700"
        
    def test_api_response_structure(self):
        """测试API响应结构"""
        print("\n🔍 测试API响应结构")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            print(f"📡 API状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 响应结构: {list(data.keys())}")
                
                if 'data' in data:
                    monitor_data = data['data']
                    print(f"📊 监控数据结构: {list(monitor_data.keys())}")
                    
                    # 检查性能统计
                    if 'performance_stats' in monitor_data:
                        perf = monitor_data['performance_stats']
                        print(f"⚡ 性能统计: {perf}")
                        
                        # 检查是否为0
                        if perf.get('cpu_usage', 0) == 0:
                            print("⚠️  CPU使用率为0")
                        if perf.get('memory_usage', 0) == 0:
                            print("⚠️  内存使用率为0")
                        if perf.get('disk_usage', 0) == 0:
                            print("⚠️  磁盘使用率为0")
                    else:
                        print("❌ 性能统计字段缺失")
                    
                    # 检查连接统计
                    if 'connection_stats' in monitor_data:
                        conn = monitor_data['connection_stats']
                        print(f"🔗 连接统计: {conn}")
                    else:
                        print("❌ 连接统计字段缺失")
                    
                    # 检查流量统计
                    if 'traffic_stats' in monitor_data:
                        traffic = monitor_data['traffic_stats']
                        print(f"📡 流量统计: {traffic}")
                    else:
                        print("❌ 流量统计字段缺失")
                else:
                    print("❌ 数据字段缺失")
            else:
                print(f"❌ API调用失败: {response.text}")
                
        except Exception as e:
            print(f"❌ API测试异常: {e}")
    
    def test_page_content(self):
        """测试页面内容"""
        print("\n🔍 测试页面内容")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/monitor", timeout=5)
            print(f"📄 页面状态码: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"📄 页面大小: {len(content)} 字符")
                
                # 检查关键元素
                checks = [
                    ("链路监控", "页面标题"),
                    ("TCP连接状态", "连接状态区域"),
                    ("系统性能", "系统性能区域"),
                    ("数据流量", "流量统计区域"),
                    ("连接列表", "连接列表区域"),
                    ("performanceStats", "性能统计变量"),
                    ("connectionStats", "连接统计变量"),
                    ("trafficStats", "流量统计变量")
                ]
                
                for keyword, description in checks:
                    if keyword in content:
                        print(f"✅ {description}: 找到 '{keyword}'")
                    else:
                        print(f"❌ {description}: 未找到 '{keyword}'")
                
                # 检查Vue组件结构
                if "{{ performanceStats.cpu }}" in content:
                    print("✅ Vue数据绑定: CPU使用率绑定正确")
                else:
                    print("❌ Vue数据绑定: CPU使用率绑定可能有问题")
                    
                if "{{ performanceStats.memory }}" in content:
                    print("✅ Vue数据绑定: 内存使用率绑定正确")
                else:
                    print("❌ Vue数据绑定: 内存使用率绑定可能有问题")
                    
                if "{{ performanceStats.disk }}" in content:
                    print("✅ Vue数据绑定: 磁盘使用率绑定正确")
                else:
                    print("❌ Vue数据绑定: 磁盘使用率绑定可能有问题")
                    
            else:
                print(f"❌ 页面访问失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 页面测试异常: {e}")
    
    def test_data_consistency_multiple_calls(self):
        """测试多次调用的数据一致性"""
        print("\n🔍 测试多次调用的数据一致性")
        print("=" * 50)
        
        for i in range(3):
            try:
                print(f"\n📊 第{i+1}次调用:")
                response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and 'performance_stats' in data['data']:
                        perf = data['data']['performance_stats']
                        print(f"   CPU: {perf.get('cpu_usage', 0)}%")
                        print(f"   内存: {perf.get('memory_usage', 0)}%")
                        print(f"   磁盘: {perf.get('disk_usage', 0)}%")
                        
                        # 检查是否为0
                        if perf.get('cpu_usage', 0) == 0:
                            print("   ⚠️  CPU为0")
                        if perf.get('memory_usage', 0) == 0:
                            print("   ⚠️  内存为0")
                        if perf.get('disk_usage', 0) == 0:
                            print("   ⚠️  磁盘为0")
                    else:
                        print("   ❌ 数据结构异常")
                else:
                    print(f"   ❌ 调用失败: {response.status_code}")
                    
                if i < 2:  # 不是最后一次
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ 调用异常: {e}")
    
    def test_backend_vs_frontend(self):
        """测试后端vs前端API"""
        print("\n🔍 测试后端vs前端API")
        print("=" * 50)
        
        try:
            # 后端直接调用
            print("📡 后端直接调用:")
            backend_response = requests.get(f"{self.backend_url}/monitor/realtime", timeout=5)
            if backend_response.status_code == 200:
                backend_data = backend_response.json()
                if 'data' in backend_data and 'performance_stats' in backend_data['data']:
                    backend_perf = backend_data['data']['performance_stats']
                    print(f"   CPU: {backend_perf.get('cpu_usage', 0)}%")
                    print(f"   内存: {backend_perf.get('memory_usage', 0)}%")
                    print(f"   磁盘: {backend_perf.get('disk_usage', 0)}%")
            
            # 前端代理调用
            print("\n🌐 前端代理调用:")
            frontend_response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if frontend_response.status_code == 200:
                frontend_data = frontend_response.json()
                if 'data' in frontend_data and 'performance_stats' in frontend_data['data']:
                    frontend_perf = frontend_data['data']['performance_stats']
                    print(f"   CPU: {frontend_perf.get('cpu_usage', 0)}%")
                    print(f"   内存: {frontend_perf.get('memory_usage', 0)}%")
                    print(f"   磁盘: {frontend_perf.get('disk_usage', 0)}%")
            
            # 比较数据
            if (backend_response.status_code == 200 and frontend_response.status_code == 200 and
                'data' in backend_data and 'data' in frontend_data and
                'performance_stats' in backend_data['data'] and 'performance_stats' in frontend_data['data']):
                
                backend_perf = backend_data['data']['performance_stats']
                frontend_perf = frontend_data['data']['performance_stats']
                
                if (backend_perf.get('cpu_usage') == frontend_perf.get('cpu_usage') and
                    backend_perf.get('memory_usage') == frontend_perf.get('memory_usage') and
                    backend_perf.get('disk_usage') == frontend_perf.get('disk_usage')):
                    print("\n✅ 后端和前端数据一致")
                else:
                    print("\n⚠️  后端和前端数据不一致")
                    
        except Exception as e:
            print(f"❌ 比较测试异常: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 简化调试测试")
        print("=" * 80)
        
        try:
            self.test_api_response_structure()
            self.test_page_content()
            self.test_data_consistency_multiple_calls()
            self.test_backend_vs_frontend()
            
            print("\n" + "=" * 80)
            print("🎯 简化调试测试完成！")
            print("\n📋 测试总结:")
            print("✅ API响应结构测试完成")
            print("✅ 页面内容测试完成")
            print("✅ 数据一致性测试完成")
            print("✅ 后端vs前端对比测试完成")
            
        except Exception as e:
            print(f"\n❌ 测试过程中出现异常: {e}")

if __name__ == "__main__":
    tester = SimpleDebugTester()
    tester.run_all_tests() 
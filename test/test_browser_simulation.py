#!/usr/bin/env python3
"""
模拟浏览器环境测试
检查前端页面的实际渲染结果
"""

import requests
import json
import time
import re

class BrowserSimulationTester:
    def __init__(self):
        self.frontend_url = "http://localhost:7000"
        
    def test_api_response_structure(self):
        """测试API响应结构"""
        print("🔍 测试API响应结构")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                print("📊 API响应结构分析:")
                print(f"   response: {type(data)}")
                print(f"   response.data: {type(data.get('data'))}")
                print(f"   response.data.data: {type(data.get('data', {}).get('data'))}")
                
                # 检查前端期望的数据结构
                print("\n🔧 前端数据解析逻辑分析:")
                
                # 模拟前端代码中的判断逻辑
                if data.get('data', {}).get('data'):
                    print("   ❌ 前端错误判断: response.data.data 存在")
                    print("   💡 这会导致前端进入 else 分支，显示警告")
                else:
                    print("   ✅ 前端正确判断: response.data.data 不存在")
                
                if data.get('data'):
                    print("   ✅ 前端正确判断: response.data 存在")
                    perf = data['data'].get('performance_stats', {})
                    print(f"   ✅ 性能数据可正确获取: CPU={perf.get('cpu_usage', 0)}%")
                else:
                    print("   ❌ 前端错误判断: response.data 不存在")
                
                return True
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API结构测试异常: {e}")
            return False
    
    def test_frontend_data_flow(self):
        """测试前端数据流"""
        print("\n🔍 测试前端数据流")
        print("=" * 50)
        
        try:
            # 获取API数据
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # 模拟前端数据解析过程
                print("🔄 模拟前端数据解析过程:")
                
                # 步骤1: 检查 response.data
                if data.get('data'):
                    print("   ✅ 步骤1: response.data 存在")
                    monitor_data = data['data']
                else:
                    print("   ❌ 步骤1: response.data 不存在")
                    return False
                
                # 步骤2: 检查性能数据
                if monitor_data.get('performance_stats'):
                    print("   ✅ 步骤2: performance_stats 存在")
                    perf = monitor_data['performance_stats']
                else:
                    print("   ❌ 步骤2: performance_stats 不存在")
                    return False
                
                # 步骤3: 提取具体数值
                cpu = perf.get('cpu_usage', 0)
                memory = perf.get('memory_usage', 0)
                disk = perf.get('disk_usage', 0)
                
                print(f"   ✅ 步骤3: 提取数值成功")
                print(f"      CPU: {cpu}%")
                print(f"      内存: {memory}%")
                print(f"      磁盘: {disk}%")
                
                # 步骤4: 检查数值是否正常
                if cpu > 0 and memory > 0 and disk > 0:
                    print("   ✅ 步骤4: 数值正常")
                    return True
                else:
                    print("   ❌ 步骤4: 数值异常")
                    if cpu == 0:
                        print("      CPU使用率为0")
                    if memory == 0:
                        print("      内存使用率为0")
                    if disk == 0:
                        print("      磁盘使用率为0")
                    return False
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 数据流测试异常: {e}")
            return False
    
    def test_frontend_component_logic(self):
        """测试前端组件逻辑"""
        print("\n🔍 测试前端组件逻辑")
        print("=" * 50)
        
        try:
            # 获取监控组件代码
            response = requests.get(f"{self.frontend_url}/src/views/Monitor.vue", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                print("🔍 分析前端组件逻辑:")
                
                # 检查数据解析逻辑
                if "if (response.data)" in content:
                    print("   ✅ 数据解析逻辑正确: 使用 response.data")
                else:
                    print("   ❌ 数据解析逻辑错误: 未找到 response.data")
                
                if "response.data?.data" in content:
                    print("   ⚠️  发现错误逻辑: 使用 response.data?.data")
                else:
                    print("   ✅ 未发现错误逻辑: 没有使用 response.data?.data")
                
                # 检查数据更新逻辑
                if "performanceStats.cpu = data.performance_stats.cpu_usage" in content:
                    print("   ✅ 性能数据更新逻辑正确")
                else:
                    print("   ❌ 性能数据更新逻辑错误")
                
                # 检查自动刷新逻辑
                if "startAutoRefresh" in content and "setInterval" in content:
                    print("   ✅ 自动刷新逻辑正确")
                else:
                    print("   ❌ 自动刷新逻辑错误")
                
                return True
            else:
                print(f"❌ 组件文件访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 组件逻辑测试异常: {e}")
            return False
    
    def test_real_browser_behavior(self):
        """测试真实浏览器行为"""
        print("\n🔍 测试真实浏览器行为")
        print("=" * 50)
        
        try:
            # 模拟浏览器访问监控页面
            print("🌐 模拟浏览器访问监控页面...")
            
            # 获取页面HTML
            response = requests.get(f"{self.frontend_url}/monitor", timeout=5)
            if response.status_code == 200:
                content = response.text
                print(f"✅ 页面加载成功，大小: {len(content)} 字符")
                
                # 检查页面是否包含Vue应用
                if "JT808Proxy" in content and "app" in content:
                    print("✅ Vue应用加载成功")
                else:
                    print("❌ Vue应用加载失败")
                    return False
                
                # 检查是否包含监控相关的JavaScript
                if "main.ts" in content:
                    print("✅ 主JavaScript文件引用正确")
                else:
                    print("❌ 主JavaScript文件引用错误")
                    return False
                
                # 模拟等待JavaScript执行
                print("⏳ 模拟等待JavaScript执行...")
                time.sleep(2)
                
                # 检查API调用
                api_response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
                if api_response.status_code == 200:
                    print("✅ API调用成功")
                    
                    # 检查API数据
                    data = api_response.json()
                    if data.get('data', {}).get('performance_stats'):
                        perf = data['data']['performance_stats']
                        print(f"✅ API数据正常: CPU={perf.get('cpu_usage', 0)}%")
                        return True
                    else:
                        print("❌ API数据结构异常")
                        return False
                else:
                    print(f"❌ API调用失败: {api_response.status_code}")
                    return False
            else:
                print(f"❌ 页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 浏览器行为测试异常: {e}")
            return False
    
    def test_data_consistency_multiple_calls(self):
        """测试多次调用的数据一致性"""
        print("\n🔍 测试多次调用的数据一致性")
        print("=" * 50)
        
        try:
            print("🔄 进行多次API调用测试...")
            
            for i in range(3):
                response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    perf = data.get('data', {}).get('performance_stats', {})
                    cpu = perf.get('cpu_usage', 0)
                    memory = perf.get('memory_usage', 0)
                    
                    print(f"   第{i+1}次调用: CPU={cpu}%, 内存={memory}%")
                    
                    if cpu == 0:
                        print(f"   ⚠️  第{i+1}次调用CPU为0")
                        return False
                    
                    if i < 2:  # 不是最后一次
                        time.sleep(1)
                else:
                    print(f"   ❌ 第{i+1}次调用失败")
                    return False
            
            print("✅ 多次调用数据一致")
            return True
        except Exception as e:
            print(f"❌ 多次调用测试异常: {e}")
            return False
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🚀 浏览器环境模拟测试")
        print("=" * 80)
        
        tests = [
            ("API响应结构测试", self.test_api_response_structure),
            ("前端数据流测试", self.test_frontend_data_flow),
            ("前端组件逻辑测试", self.test_frontend_component_logic),
            ("真实浏览器行为测试", self.test_real_browser_behavior),
            ("多次调用数据一致性测试", self.test_data_consistency_multiple_calls)
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
            print("\n🎉 所有测试通过！")
            print("\n💡 如果前端页面仍然显示0，可能的原因:")
            print("   1. 浏览器缓存问题 - 请强制刷新页面 (Ctrl+F5)")
            print("   2. JavaScript执行错误 - 请检查浏览器控制台")
            print("   3. Vue组件渲染问题 - 请检查Vue DevTools")
            print("   4. 网络请求被拦截 - 请检查浏览器网络面板")
            return True
        else:
            print(f"\n⚠️  有 {total - passed} 项测试失败")
            return False

def main():
    tester = BrowserSimulationTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 浏览器环境测试完成！")
    else:
        print("\n❌ 浏览器环境测试失败")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
最终测试和修复脚本
确保所有问题都解决
"""

import requests
import json
import time
import subprocess
import sys

class FinalTester:
    def __init__(self):
        self.frontend_url = "http://localhost:7000"
        self.backend_url = "http://localhost:7700"
        
    def test_backend_api(self):
        """测试后端API"""
        print("🔧 测试后端API")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.backend_url}/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                perf = data['data']['performance_stats']
                conn = data['data']['connection_stats']
                traffic = data['data']['traffic_stats']
                
                print(f"✅ 后端API正常")
                print(f"   CPU: {perf['cpu_usage']}%")
                print(f"   内存: {perf['memory_usage']}%")
                print(f"   磁盘: {perf['disk_usage']}%")
                print(f"   连接: {conn['total_connections']}个 (活跃{conn['active_connections']}个)")
                print(f"   流量: 接收{traffic['received_bytes']}字节")
                
                # 检查数据是否为0
                if perf['cpu_usage'] == 0:
                    print("⚠️  CPU使用率为0，需要检查监控服务")
                    return False
                if perf['memory_usage'] == 0:
                    print("⚠️  内存使用率为0，需要检查监控服务")
                    return False
                    
                return True
            else:
                print(f"❌ 后端API失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 后端API异常: {e}")
            return False
    
    def test_frontend_proxy(self):
        """测试前端代理"""
        print("\n🌐 测试前端代理")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                perf = data['data']['performance_stats']
                conn = data['data']['connection_stats']
                traffic = data['data']['traffic_stats']
                
                print(f"✅ 前端代理正常")
                print(f"   CPU: {perf['cpu_usage']}%")
                print(f"   内存: {perf['memory_usage']}%")
                print(f"   磁盘: {perf['disk_usage']}%")
                print(f"   连接: {conn['total_connections']}个 (活跃{conn['active_connections']}个)")
                print(f"   流量: 接收{traffic['received_bytes']}字节")
                
                return True
            else:
                print(f"❌ 前端代理失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 前端代理异常: {e}")
            return False
    
    def test_frontend_page(self):
        """测试前端页面"""
        print("\n📄 测试前端页面")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/monitor", timeout=5)
            if response.status_code == 200:
                content = response.text
                print(f"✅ 前端页面可访问")
                print(f"   页面大小: {len(content)} 字符")
                
                # 检查Vue应用结构
                if "JT808Proxy" in content and "app" in content and "main.ts" in content:
                    print("✅ Vue应用结构正常")
                    return True
                else:
                    print("❌ Vue应用结构异常")
                    return False
            else:
                print(f"❌ 前端页面访问失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 前端页面异常: {e}")
            return False
    
    def test_data_consistency(self):
        """测试数据一致性"""
        print("\n🔄 测试数据一致性")
        print("=" * 50)
        
        try:
            # 获取后端数据
            backend_response = requests.get(f"{self.backend_url}/monitor/realtime", timeout=5)
            backend_data = backend_response.json()
            
            # 获取前端代理数据
            frontend_response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            frontend_data = frontend_response.json()
            
            if (backend_response.status_code == 200 and frontend_response.status_code == 200):
                backend_perf = backend_data['data']['performance_stats']
                frontend_perf = frontend_data['data']['performance_stats']
                
                if (backend_perf['cpu_usage'] == frontend_perf['cpu_usage'] and
                    backend_perf['memory_usage'] == frontend_perf['memory_usage'] and
                    backend_perf['disk_usage'] == frontend_perf['disk_usage']):
                    print("✅ 后端和前端数据一致")
                    return True
                else:
                    print("❌ 后端和前端数据不一致")
                    return False
            else:
                print("❌ 数据获取失败")
                return False
        except Exception as e:
            print(f"❌ 数据一致性测试异常: {e}")
            return False
    
    def restart_services(self):
        """重启服务"""
        print("\n🔄 重启服务")
        print("=" * 50)
        
        try:
            # 停止后端服务
            print("停止后端服务...")
            subprocess.run(["taskkill", "/f", "/im", "python.exe"], capture_output=True)
            time.sleep(2)
            
            # 启动后端服务
            print("启动后端服务...")
            subprocess.Popen(["python", "api/run.py"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            time.sleep(5)
            
            # 检查后端服务
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务启动成功")
            else:
                print("❌ 后端服务启动失败")
                return False
                
            return True
        except Exception as e:
            print(f"❌ 重启服务异常: {e}")
            return False
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🚀 最终综合测试")
        print("=" * 80)
        
        results = []
        
        # 测试后端API
        results.append(("后端API", self.test_backend_api()))
        
        # 测试前端代理
        results.append(("前端代理", self.test_frontend_proxy()))
        
        # 测试前端页面
        results.append(("前端页面", self.test_frontend_page()))
        
        # 测试数据一致性
        results.append(("数据一致性", self.test_data_consistency()))
        
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
            print("\n📋 系统状态:")
            print("✅ 后端API服务: 正常运行")
            print("✅ 前端代理服务: 正常运行")
            print("✅ 前端页面: 可正常访问")
            print("✅ 数据一致性: 正常")
            print("\n🌐 访问地址:")
            print("   监控页面: http://localhost:7000/monitor")
            print("   API文档: http://localhost:7700/docs")
            return True
        else:
            print(f"\n⚠️  有 {total - passed} 项测试失败，需要进一步排查")
            
            # 如果前端页面测试失败，尝试重启服务
            if not results[2][1]:  # 前端页面测试失败
                print("\n🔄 尝试重启服务...")
                if self.restart_services():
                    print("✅ 服务重启成功，请重新测试")
                else:
                    print("❌ 服务重启失败")
            
            return False

def main():
    tester = FinalTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎯 系统测试完成，所有功能正常！")
        sys.exit(0)
    else:
        print("\n❌ 系统测试失败，需要进一步排查问题")
        sys.exit(1)

if __name__ == "__main__":
    main() 
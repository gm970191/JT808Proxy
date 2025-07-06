#!/usr/bin/env python3
"""
前端数据绑定调试工具
模拟浏览器环境，测试前端页面的数据绑定和渲染
"""

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FrontendDebugTester:
    def __init__(self):
        self.frontend_url = "http://localhost:7000"
        self.backend_url = "http://localhost:7700"
        self.driver = None
        
    def setup_driver(self):
        """设置Chrome驱动"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 无头模式
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome驱动初始化成功")
            return True
        except Exception as e:
            print(f"❌ Chrome驱动初始化失败: {e}")
            return False
    
    def test_api_direct(self):
        """测试1: 直接API调用"""
        print("\n🔍 测试1: 直接API调用")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.frontend_url}/api/monitor/realtime", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ API调用成功")
                
                # 检查数据结构
                if 'data' in data and 'performance_stats' in data['data']:
                    perf = data['data']['performance_stats']
                    print(f"📊 性能数据: CPU={perf.get('cpu_usage', 0)}%, "
                          f"内存={perf.get('memory_usage', 0)}%, "
                          f"磁盘={perf.get('disk_usage', 0)}%")
                    
                    # 检查数据是否为0
                    if perf.get('cpu_usage', 0) == 0:
                        print("⚠️  CPU使用率为0")
                    if perf.get('memory_usage', 0) == 0:
                        print("⚠️  内存使用率为0")
                    if perf.get('disk_usage', 0) == 0:
                        print("⚠️  磁盘使用率为0")
                else:
                    print("❌ 数据结构异常")
            else:
                print(f"❌ API调用失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ API测试异常: {e}")
    
    def test_page_rendering(self):
        """测试2: 页面渲染测试"""
        print("\n🔍 测试2: 页面渲染测试")
        print("=" * 50)
        
        if not self.driver:
            print("❌ 浏览器驱动未初始化")
            return
        
        try:
            # 访问监控页面
            print(f"🌐 访问页面: {self.frontend_url}/monitor")
            self.driver.get(f"{self.frontend_url}/monitor")
            
            # 等待页面加载
            wait = WebDriverWait(self.driver, 10)
            
            # 检查页面标题
            try:
                title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
                if "链路监控" in title.text:
                    print("✅ 页面标题正确")
                else:
                    print(f"⚠️  页面标题异常: {title.text}")
            except:
                print("❌ 页面标题未找到")
            
            # 等待数据加载
            time.sleep(3)
            
            # 检查性能数据区域
            try:
                perf_elements = self.driver.find_elements(By.CLASS_NAME, "perf-item")
                print(f"📊 找到 {len(perf_elements)} 个性能数据元素")
                
                for element in perf_elements:
                    text = element.text
                    print(f"   - {text}")
                    
                    # 检查是否为0
                    if "0%" in text:
                        print(f"   ⚠️  发现0值: {text}")
                        
            except Exception as e:
                print(f"❌ 性能数据元素查找失败: {e}")
            
            # 检查连接数据区域
            try:
                conn_elements = self.driver.find_elements(By.CLASS_NAME, "status-item")
                print(f"🔗 找到 {len(conn_elements)} 个连接数据元素")
                
                for element in conn_elements:
                    text = element.text
                    print(f"   - {text}")
                    
            except Exception as e:
                print(f"❌ 连接数据元素查找失败: {e}")
            
            # 检查流量数据区域
            try:
                traffic_elements = self.driver.find_elements(By.CLASS_NAME, "traffic-item")
                print(f"📡 找到 {len(traffic_elements)} 个流量数据元素")
                
                for element in traffic_elements:
                    text = element.text
                    print(f"   - {text}")
                    
            except Exception as e:
                print(f"❌ 流量数据元素查找失败: {e}")
                
        except Exception as e:
            print(f"❌ 页面渲染测试异常: {e}")
    
    def test_console_logs(self):
        """测试3: 控制台日志测试"""
        print("\n🔍 测试3: 控制台日志测试")
        print("=" * 50)
        
        if not self.driver:
            print("❌ 浏览器驱动未初始化")
            return
        
        try:
            # 访问页面并等待
            self.driver.get(f"{self.frontend_url}/monitor")
            time.sleep(5)
            
            # 获取控制台日志
            logs = self.driver.get_log('browser')
            print(f"📝 找到 {len(logs)} 条控制台日志")
            
            for log in logs:
                message = log.get('message', '')
                if 'error' in message.lower():
                    print(f"❌ 错误日志: {message}")
                elif 'warning' in message.lower():
                    print(f"⚠️  警告日志: {message}")
                else:
                    print(f"ℹ️  信息日志: {message}")
                    
        except Exception as e:
            print(f"❌ 控制台日志测试异常: {e}")
    
    def test_network_requests(self):
        """测试4: 网络请求测试"""
        print("\n🔍 测试4: 网络请求测试")
        print("=" * 50)
        
        if not self.driver:
            print("❌ 浏览器驱动未初始化")
            return
        
        try:
            # 启用网络日志
            self.driver.execute_cdp_cmd('Network.enable', {})
            
            # 访问页面
            self.driver.get(f"{self.frontend_url}/monitor")
            time.sleep(5)
            
            # 获取网络请求
            performance_logs = self.driver.execute_script("""
                var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {};
                var network = performance.getEntries() || {};
                return network;
            """)
            
            print(f"🌐 找到 {len(performance_logs)} 个网络请求")
            
            # 查找API请求
            api_requests = [req for req in performance_logs if 'monitor' in req.get('name', '')]
            print(f"📡 找到 {len(api_requests)} 个监控API请求")
            
            for req in api_requests:
                name = req.get('name', '')
                duration = req.get('duration', 0)
                print(f"   - {name} (耗时: {duration:.2f}ms)")
                
        except Exception as e:
            print(f"❌ 网络请求测试异常: {e}")
    
    def test_data_refresh(self):
        """测试5: 数据刷新测试"""
        print("\n🔍 测试5: 数据刷新测试")
        print("=" * 50)
        
        if not self.driver:
            print("❌ 浏览器驱动未初始化")
            return
        
        try:
            # 访问页面
            self.driver.get(f"{self.frontend_url}/monitor")
            time.sleep(3)
            
            # 获取初始数据
            print("📊 获取初始数据...")
            initial_perf = self.driver.find_elements(By.CLASS_NAME, "perf-item")
            initial_values = []
            for element in initial_perf:
                initial_values.append(element.text)
            
            print(f"   初始值: {initial_values}")
            
            # 等待5秒（模拟自动刷新）
            print("⏳ 等待5秒...")
            time.sleep(5)
            
            # 获取刷新后数据
            print("📊 获取刷新后数据...")
            refreshed_perf = self.driver.find_elements(By.CLASS_NAME, "perf-item")
            refreshed_values = []
            for element in refreshed_perf:
                refreshed_values.append(element.text)
            
            print(f"   刷新后值: {refreshed_values}")
            
            # 比较数据
            if initial_values == refreshed_values:
                print("⚠️  数据没有变化，可能自动刷新未工作")
            else:
                print("✅ 数据已刷新")
                
        except Exception as e:
            print(f"❌ 数据刷新测试异常: {e}")
    
    def cleanup(self):
        """清理资源"""
        if self.driver:
            self.driver.quit()
            print("🧹 浏览器驱动已清理")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 前端数据绑定调试测试")
        print("=" * 80)
        
        try:
            # 设置浏览器驱动
            if not self.setup_driver():
                return
            
            # 运行测试
            self.test_api_direct()
            self.test_page_rendering()
            self.test_console_logs()
            self.test_network_requests()
            self.test_data_refresh()
            
            print("\n" + "=" * 80)
            print("🎯 前端调试测试完成！")
            
        except Exception as e:
            print(f"\n❌ 测试过程中出现异常: {e}")
        finally:
            self.cleanup()

if __name__ == "__main__":
    tester = FrontendDebugTester()
    tester.run_all_tests() 
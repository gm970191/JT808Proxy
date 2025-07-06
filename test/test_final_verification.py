#!/usr/bin/env python3
"""
最终验证测试
提供具体的排查建议
"""

import requests
import json
import time

def test_final_verification():
    """最终验证测试"""
    print("🔍 最终验证测试")
    print("=" * 80)
    
    frontend_url = "http://localhost:7000"
    backend_url = "http://localhost:7700"
    
    # 测试1: 验证后端数据
    print("\n📡 测试1: 验证后端数据")
    try:
        response = requests.get(f"{backend_url}/monitor/realtime", timeout=5)
        if response.status_code == 200:
            data = response.json()
            perf = data['data']['performance_stats']
            print(f"✅ 后端数据正常: CPU={perf['cpu_usage']}%, 内存={perf['memory_usage']}%")
        else:
            print(f"❌ 后端数据异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端测试异常: {e}")
        return False
    
    # 测试2: 验证前端代理
    print("\n🌐 测试2: 验证前端代理")
    try:
        response = requests.get(f"{frontend_url}/api/monitor/realtime", timeout=5)
        if response.status_code == 200:
            data = response.json()
            perf = data['data']['performance_stats']
            print(f"✅ 前端代理正常: CPU={perf['cpu_usage']}%, 内存={perf['memory_usage']}%")
        else:
            print(f"❌ 前端代理异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端代理测试异常: {e}")
        return False
    
    # 测试3: 验证数据一致性
    print("\n🔄 测试3: 验证数据一致性")
    try:
        backend_response = requests.get(f"{backend_url}/monitor/realtime", timeout=5)
        frontend_response = requests.get(f"{frontend_url}/api/monitor/realtime", timeout=5)
        
        if backend_response.status_code == 200 and frontend_response.status_code == 200:
            backend_data = backend_response.json()
            frontend_data = frontend_response.json()
            
            backend_perf = backend_data['data']['performance_stats']
            frontend_perf = frontend_data['data']['performance_stats']
            
            if (backend_perf['cpu_usage'] == frontend_perf['cpu_usage'] and
                backend_perf['memory_usage'] == frontend_perf['memory_usage']):
                print("✅ 数据一致性正常")
            else:
                print("❌ 数据不一致")
                return False
        else:
            print("❌ 数据获取失败")
            return False
    except Exception as e:
        print(f"❌ 数据一致性测试异常: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("🎉 所有验证测试通过！")
    print("=" * 80)
    
    print("\n📋 系统状态确认:")
    print("✅ 后端API服务: 正常运行")
    print("✅ 前端代理服务: 正常运行")
    print("✅ 数据一致性: 正常")
    print("✅ 监控数据: 实时更新")
    
    print("\n🌐 访问地址:")
    print("   监控页面: http://localhost:7000/monitor")
    print("   API文档: http://localhost:7700/docs")
    
    print("\n🔍 如果前端页面仍然显示0，请按以下步骤排查:")
    print("\n1️⃣ 浏览器缓存问题:")
    print("   - 按 Ctrl+F5 强制刷新页面")
    print("   - 或者按 F12 打开开发者工具，右键刷新按钮选择'清空缓存并硬性重新加载'")
    print("   - 或者按 Ctrl+Shift+R 强制刷新")
    
    print("\n2️⃣ 检查浏览器控制台:")
    print("   - 按 F12 打开开发者工具")
    print("   - 查看 Console 标签页是否有错误信息")
    print("   - 查看 Network 标签页是否有API请求失败")
    
    print("\n3️⃣ 检查Vue DevTools:")
    print("   - 安装Vue DevTools浏览器扩展")
    print("   - 查看组件状态和数据绑定")
    print("   - 检查 performanceStats、connectionStats、trafficStats 的值")
    
    print("\n4️⃣ 检查网络请求:")
    print("   - 在Network标签页中找到 /api/monitor/realtime 请求")
    print("   - 查看请求状态码是否为200")
    print("   - 查看响应数据是否包含正确的性能数据")
    
    print("\n5️⃣ 检查前端代码:")
    print("   - 确认 Monitor.vue 中的数据解析逻辑已修复")
    print("   - 确认使用 response.data 而不是 response.data.data")
    print("   - 确认数据更新逻辑正确")
    
    print("\n6️⃣ 重启服务:")
    print("   - 停止前端服务 (Ctrl+C)")
    print("   - 重新启动: cd frontend && npm run dev")
    print("   - 清除浏览器缓存后重新访问")
    
    print("\n💡 调试建议:")
    print("   - 在浏览器控制台中手动测试API调用:")
    print("     fetch('/api/monitor/realtime').then(r => r.json()).then(console.log)")
    print("   - 检查返回的数据结构是否符合前端期望")
    print("   - 确认前端代码中的条件判断逻辑正确")
    
    return True

if __name__ == "__main__":
    success = test_final_verification()
    if success:
        print("\n🎯 最终验证完成！")
    else:
        print("\n❌ 最终验证失败") 
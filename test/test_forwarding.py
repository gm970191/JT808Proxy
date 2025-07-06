"""
转发功能测试脚本
验证一对一/多对一转发模式和终端映射功能
"""
import sys
import os
import asyncio
import socket
import time
import importlib.util

# 动态加载模块
forwarder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../jt808proxy/core/forwarder.py'))
spec = importlib.util.spec_from_file_location("forwarder", forwarder_path)
forwarder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(forwarder)
Forwarder = forwarder.Forwarder

async def test_forwarding():
    """测试转发功能"""
    print("启动转发功能测试...")
    
    # 创建转发器实例
    forwarder = Forwarder()
    
    # 测试一对一模式
    print("\n=== 测试一对一转发模式 ===")
    forwarder.set_forwarding_mode('one_to_one')
    
    # 添加终端映射
    forwarder.add_terminal_mapping('13912345678', '127.0.0.1', 7901, 'server_1')
    forwarder.add_terminal_mapping('13987654321', '127.0.0.1', 7902, 'server_2')
    
    # 获取转发统计
    stats = forwarder.get_forwarding_stats()
    print(f"转发统计: {stats}")
    
    # 测试多对一模式
    print("\n=== 测试多对一转发模式 ===")
    forwarder.set_forwarding_mode('many_to_one')
    forwarder.set_default_target('127.0.0.1', 7900, 'default_server')
    
    # 获取转发统计
    stats = forwarder.get_forwarding_stats()
    print(f"转发统计: {stats}")
    
    # 测试数据包转发（模拟）
    print("\n=== 测试数据包转发 ===")
    test_data = b'test_packet_data'
    
    # 测试一对一模式下的转发
    forwarder.set_forwarding_mode('one_to_one')
    success = await forwarder.forward_packet('13912345678', test_data)
    print(f"一对一模式转发结果: {'成功' if success else '失败'}")
    
    # 测试多对一模式下的转发
    forwarder.set_forwarding_mode('many_to_one')
    success = await forwarder.forward_packet('13912345678', test_data)
    print(f"多对一模式转发结果: {'成功' if success else '失败'}")
    
    print("\n转发功能测试完成")


if __name__ == "__main__":
    asyncio.run(test_forwarding()) 
"""
TCP Server 增强测试脚本
用于验证服务器链路管理、统计信息和日志功能
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import socket
import time
import json
try:
    from jt808proxy.core.tcp_server import TCPServer
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("tcp_server", os.path.join(os.path.dirname(__file__), '../jt808proxy/core/tcp_server.py'))
    tcp_server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tcp_server)
    TCPServer = tcp_server.TCPServer


async def test_server():
    """测试服务器功能"""
    print("启动 TCP Server 增强测试...")
    
    # 创建服务器实例
    server = TCPServer(host='127.0.0.1', port=16900)
    
    # 启动服务器（在后台运行）
    server_task = asyncio.create_task(server.start())
    
    # 等待服务器启动
    await asyncio.sleep(1)
    
    print("服务器已启动，开始测试客户端连接...")
    
    # 测试多个客户端连接
    clients = []
    for i in range(3):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 16900))
            clients.append(client)
            print(f"客户端 {i+1} 连接成功")
            
            # 发送测试数据
            test_data = f"Test data from client {i+1}".encode()
            client.send(test_data)
            print(f"客户端 {i+1} 发送数据: {test_data}")
            
            # 接收响应
            response = client.recv(1024)
            print(f"客户端 {i+1} 收到响应: {response}")
            
            # 等待一段时间，让服务器处理
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"客户端 {i+1} 连接失败: {e}")
    
    # 检查连接统计
    print("\n=== 连接统计信息 ===")
    stats = server.get_connection_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # 等待一段时间，观察监控日志
    print("\n等待 5 秒观察监控日志...")
    await asyncio.sleep(5)
    
    # 关闭部分客户端连接
    for i, client in enumerate(clients[:2]):
        client.close()
        print(f"客户端 {i+1} 已关闭")
    
    # 等待一段时间
    await asyncio.sleep(2)
    
    # 再次检查统计
    print("\n=== 关闭部分连接后的统计信息 ===")
    stats = server.get_connection_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # 关闭剩余客户端连接
    for i, client in enumerate(clients[2:]):
        client.close()
        print(f"客户端 {i+3} 已关闭")
    
    # 等待一段时间后再次检查统计
    await asyncio.sleep(2)
    print("\n=== 所有连接关闭后的统计信息 ===")
    stats = server.get_connection_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    # 取消服务器任务
    server_task.cancel()
    print("\n测试完成")


if __name__ == "__main__":
    asyncio.run(test_server()) 
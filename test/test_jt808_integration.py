"""
JT808协议解析与TCP服务集成测试
"""
import sys
import os
import asyncio
import socket
import time
import importlib.util

# 动态加载模块
tcp_server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../jt808proxy/core/tcp_server.py'))
spec = importlib.util.spec_from_file_location("tcp_server", tcp_server_path)
tcp_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tcp_server)
TCPServer = tcp_server.TCPServer

async def test_jt808_integration():
    """测试JT808协议解析与TCP服务集成"""
    print("启动 JT808 协议解析集成测试...")
    
    # 创建服务器实例
    server = TCPServer(host='127.0.0.1', port=16900)
    
    # 启动服务器（在后台运行）
    server_task = asyncio.create_task(server.start())
    
    # 等待服务器启动
    await asyncio.sleep(1)
    
    print("服务器已启动，开始测试JT808协议解析...")
    
    # 构造JT808协议数据包
    # 消息ID: 0x0200 (位置信息), 消息体属性: 0x0040, 手机号: 13912345678, 流水号: 1
    jt808_data = bytes.fromhex('02 00 00 40 01 39 12 34 56 78 00 01')
    
    try:
        # 连接服务器
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 16900))
        print("客户端连接成功")
        
        # 发送JT808数据包
        client.send(jt808_data)
        print(f"发送JT808数据包: {jt808_data.hex()}")
        
        # 接收响应
        response = client.recv(1024)
        print(f"收到响应: {response.hex()}")
        
        # 等待一段时间，让服务器处理日志
        await asyncio.sleep(2)
        
        # 检查连接统计
        stats = server.get_connection_stats()
        print(f"连接统计: 活跃连接数 {stats['active_connections']}, "
              f"总接收字节 {stats['total_bytes_received']}")
        
        client.close()
        print("客户端已关闭")
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
    
    # 取消服务器任务
    server_task.cancel()
    print("集成测试完成")


if __name__ == "__main__":
    asyncio.run(test_jt808_integration()) 
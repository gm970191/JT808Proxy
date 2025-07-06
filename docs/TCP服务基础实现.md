# TCP 服务基础实现

## 实现概述

本阶段实现了基础的 TCP Server，具备以下功能：
- 支持多终端并发连接
- 链路状态管理
- 基础日志输出
- 连接统计信息

## 核心组件

### 1. ConnectionInfo 数据类
- 记录连接的详细信息：远程地址、端口、连接时间、最后活动时间、活跃状态
- 用于链路状态管理和监控

### 2. TCPServer 类
- 异步 TCP 服务器实现
- 支持多客户端并发连接
- 自动管理连接生命周期
- 提供连接统计功能

## 主要功能

### 连接管理
- 自动记录新连接信息
- 实时更新最后活动时间
- 连接断开时自动清理资源

### 数据处理
- 接收客户端数据（最大 1024 字节）
- 基础回显功能（用于测试）
- 数据以十六进制格式记录到日志

### 日志记录
- 连接建立/断开日志
- 数据接收日志
- 错误处理日志

## 测试方法

### 1. 启动服务器
```bash
cd JT808Proxy
python -m jt808proxy.core.tcp_server
```

### 2. 使用 telnet 测试
```bash
telnet localhost 8080
```

### 3. 使用 Python 客户端测试
```python
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
client.send(b'Hello JT808Proxy')
response = client.recv(1024)
print(f"收到响应: {response}")
client.close()
```

## 下一步计划

1. 实现 JT808 协议解析
2. 添加报文转发功能
3. 实现智能路由机制

## 注意事项

- 当前为基础实现，仅支持数据回显
- 后续将集成 JT808 协议解析
- 建议在生产环境中添加更多错误处理和监控 
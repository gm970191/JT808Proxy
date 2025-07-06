#!/usr/bin/env python3
"""
JT808终端模拟器
模拟终端连接TCP服务并发送数据
"""

import asyncio
import socket
import struct
import time
import random
from datetime import datetime

class JT808Simulator:
    def __init__(self, host='localhost', port=16900):
        self.host = host
        self.port = port
        self.terminal_phone = "13800138001"  # 模拟终端手机号
        self.msg_seq = 1  # 消息流水号
        
    def create_jt808_header(self, msg_id, msg_body=b""):
        """创建JT808协议头"""
        # 消息ID (2字节)
        # 消息体属性 (2字节) - 包含消息体长度
        msg_body_len = len(msg_body)
        msg_attr = msg_body_len
        
        # 终端手机号 (6字节) - BCD编码
        # 将手机号转换为BCD格式（每两位数字占一个字节）
        phone_bcd = b''
        for i in range(0, len(self.terminal_phone), 2):
            if i + 1 < len(self.terminal_phone):
                # 两个数字组成一个字节
                high = int(self.terminal_phone[i])
                low = int(self.terminal_phone[i + 1])
                phone_bcd += bytes([high * 16 + low])
            else:
                # 最后一个数字，高位补0
                low = int(self.terminal_phone[i])
                phone_bcd += bytes([low])
        
        # 确保长度为6字节，不足补0
        while len(phone_bcd) < 6:
            phone_bcd += b'\x00'
        
        # 消息流水号 (2字节)
        msg_seq_bytes = struct.pack('>H', self.msg_seq)
        
        # 组装协议头
        header = struct.pack('>HH', msg_id, msg_attr) + phone_bcd + msg_seq_bytes
        
        # 计算校验码
        checksum = 0
        for byte in header + msg_body:
            checksum ^= byte
        
        # 添加校验码和标识位
        packet = b'\x7e' + header + msg_body + struct.pack('B', checksum) + b'\x7e'
        
        self.msg_seq += 1
        return packet
    
    def create_location_data(self, lat, lng, altitude=100, speed=60):
        """创建定位信息数据"""
        # 简化的定位信息结构
        # 报警标志 (4字节)
        alarm_flag = struct.pack('>I', 0)
        
        # 状态 (4字节)
        status = struct.pack('>I', 0)
        
        # 纬度 (4字节) - 以度为单位的浮点数 * 10^6
        latitude = int(lat * 1000000)
        lat_bytes = struct.pack('>I', latitude)
        
        # 经度 (4字节) - 以度为单位的浮点数 * 10^6
        longitude = int(lng * 1000000)
        lng_bytes = struct.pack('>I', longitude)
        
        # 高程 (2字节) - 海拔高度，单位为米
        altitude_bytes = struct.pack('>H', altitude)
        
        # 速度 (2字节) - 1/10km/h
        speed_bytes = struct.pack('>H', speed * 10)
        
        # 方向 (2字节) - 0-359，正北为0，顺时针
        direction = random.randint(0, 359)
        direction_bytes = struct.pack('>H', direction)
        
        # 时间 (6字节) - BCD编码
        now = datetime.now()
        time_str = now.strftime('%y%m%d%H%M%S')
        time_bytes = bytes.fromhex(time_str)
        
        # 组装定位信息
        location_data = (alarm_flag + status + lat_bytes + lng_bytes + 
                        altitude_bytes + speed_bytes + direction_bytes + time_bytes)
        
        return location_data
    
    def create_register_data(self):
        """创建终端注册数据"""
        # 省域ID (2字节)
        province_id = struct.pack('>H', 11)  # 北京市
        
        # 市县域ID (2字节)
        city_id = struct.pack('>H', 1)
        
        # 制造商ID (5字节) - ASCII编码
        manufacturer_id = b'TEST1'
        
        # 终端型号 (20字节) - ASCII编码，不足补0
        terminal_model = b'JT808-SIMULATOR' + b'\x00' * 5
        
        # 终端ID (7字节) - ASCII编码
        terminal_id = b'TEST001'
        
        # 车牌颜色 (1字节)
        plate_color = struct.pack('B', 1)  # 蓝色
        
        # 车牌号码 (12字节) - ASCII编码
        plate_number = b'JINGA12345' + b'\x00' * 2
        
        # 组装注册信息
        register_data = (province_id + city_id + manufacturer_id + terminal_model + 
                        terminal_id + plate_color + plate_number)
        
        return register_data
    
    async def simulate_terminal(self):
        """模拟终端连接和数据发送"""
        try:
            # 创建TCP连接
            reader, writer = await asyncio.open_connection(self.host, self.port)
            print(f"✅ 终端 {self.terminal_phone} 已连接到TCP服务 {self.host}:{self.port}")
            
            # 发送终端注册消息
            register_data = self.create_register_data()
            register_packet = self.create_jt808_header(0x0100, register_data)
            writer.write(register_packet)
            await writer.drain()
            print(f"📤 发送终端注册消息 (消息ID: 0x0100)")
            
            # 等待注册响应
            await asyncio.sleep(1)
            
            # 模拟发送定位信息
            base_lat, base_lng = 39.9042, 116.4074  # 北京天安门坐标
            for i in range(10):
                # 随机偏移坐标
                lat = base_lat + random.uniform(-0.01, 0.01)
                lng = base_lng + random.uniform(-0.01, 0.01)
                
                # 创建定位数据
                location_data = self.create_location_data(lat, lng)
                location_packet = self.create_jt808_header(0x0200, location_data)
                
                # 发送定位信息
                writer.write(location_packet)
                await writer.drain()
                print(f"📍 发送定位信息 {i+1}/10 - 位置: ({lat:.6f}, {lng:.6f})")
                
                # 等待响应
                try:
                    response = await asyncio.wait_for(reader.read(1024), timeout=2.0)
                    if response:
                        print(f"📥 收到响应: {len(response)} 字节")
                except asyncio.TimeoutError:
                    print("⏰ 响应超时")
                
                await asyncio.sleep(3)  # 每3秒发送一次定位
            
            # 关闭连接
            writer.close()
            await writer.wait_closed()
            print(f"🔌 终端 {self.terminal_phone} 断开连接")
            
        except Exception as e:
            print(f"❌ 模拟终端出错: {e}")

async def main():
    """主函数"""
    print("🚀 启动JT808终端模拟器...")
    
    # 创建多个模拟终端
    simulators = []
    for i in range(3):  # 创建3个模拟终端
        phone = f"1380013800{i+1}"
        simulator = JT808Simulator()
        simulator.terminal_phone = phone
        simulators.append(simulator)
    
    # 并发运行所有模拟终端
    tasks = [simulator.simulate_terminal() for simulator in simulators]
    await asyncio.gather(*tasks)
    
    print("✅ 所有模拟终端运行完成")

if __name__ == "__main__":
    asyncio.run(main()) 
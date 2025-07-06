"""
JT808 协议头解析模块
"""
from typing import Optional, Dict, Any
import struct

class JT808Header:
    """JT808协议头数据结构"""
    def __init__(self, msg_id: int, body_props: int, phone: str, msg_seq: int, pkg_total: Optional[int]=None, pkg_index: Optional[int]=None):
        self.msg_id = msg_id
        self.body_props = body_props
        self.phone = phone
        self.msg_seq = msg_seq
        self.pkg_total = pkg_total
        self.pkg_index = pkg_index

    def to_dict(self) -> Dict:
        return {
            'msg_id': self.msg_id,
            'body_props': self.body_props,
            'phone': self.phone,
            'msg_seq': self.msg_seq,
            'pkg_total': self.pkg_total,
            'pkg_index': self.pkg_index
        }

class JT808Parser:
    """JT808协议头解析器"""
    @staticmethod
    def parse_header(data: bytes) -> Optional[JT808Header]:
        """
        解析JT808协议头，返回JT808Header对象
        JT808标准头部格式：
        0      1      2      3      4      5      6      7      8      9      10     11     12     13
        |----消息ID----|--消息体属性--|----终端手机号BCD----|--消息流水号--|[分包总数][分包序号]
        """
        if len(data) < 12:
            return None
        msg_id = int.from_bytes(data[0:2], 'big')
        body_props = int.from_bytes(data[2:4], 'big')
        phone_bcd = data[4:10]
        phone = ''.join(f"{(b>>4)&0xF}{b&0xF}" for b in phone_bcd).lstrip('0')
        msg_seq = int.from_bytes(data[10:12], 'big')
        # 判断是否分包
        is_subpkg = (body_props & 0x2000) != 0
        pkg_total = pkg_index = None
        if is_subpkg and len(data) >= 16:
            pkg_total = int.from_bytes(data[12:14], 'big')
            pkg_index = int.from_bytes(data[14:16], 'big')
        return JT808Header(msg_id, body_props, phone, msg_seq, pkg_total, pkg_index)

    @staticmethod
    def parse_location_data(data: bytes, header_offset: int = 0) -> Optional[Dict[str, Any]]:
        """
        解析0x0200定位信息报文
        定位信息格式（简化版）：
        0      1      2      3      4      5      6      7      8      9      10     11     12     13     14     15
        |----报警标志----|----状态----|----纬度----|----经度----|----高程----|----速度----|----方向----|----时间----|
        """
        if len(data) < header_offset + 28:  # 最小长度检查
            return None
        
        offset = header_offset
        alarm_flag = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        status = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        
        # 纬度（度*10^6）
        latitude_raw = int.from_bytes(data[offset:offset+4], 'big')
        latitude = latitude_raw / 1000000.0
        offset += 4
        
        # 经度（度*10^6）
        longitude_raw = int.from_bytes(data[offset:offset+4], 'big')
        longitude = longitude_raw / 1000000.0
        offset += 4
        
        # 高程（米）
        altitude = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        
        # 速度（0.1km/h）
        speed = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        
        # 方向（0-359，正北为0，顺时针）
        direction = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        
        # 时间（BCD码，YY-MM-DD-hh-mm-ss）
        time_bytes = data[offset:offset+6]
        time_str = ''.join(f"{b>>4}{b&0xF:02d}" for b in time_bytes)
        time_str = f"20{time_str[:2]}-{time_str[2:4]}-{time_str[4:6]} {time_str[6:8]}:{time_str[8:10]}:{time_str[10:12]}"
        
        return {
            'alarm_flag': alarm_flag,
            'status': status,
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'speed': speed,
            'direction': direction,
            'time': time_str
        }

    @staticmethod
    def parse_terminal_register(data: bytes, header_offset: int = 0) -> Optional[Dict[str, Any]]:
        """
        解析0x0100终端注册信息报文
        终端注册信息格式（简化版）：
        0      1      2      3      4      5      6      7      8      9      10     11     12     13     14     15
        |----省域ID----|----市县域ID----|----制造商ID----|----终端型号----|----终端ID----|----车牌颜色----|----车牌号码----|
        """
        if len(data) < header_offset + 37:  # 最小长度检查
            return None
        
        offset = header_offset
        province_id = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        city_id = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        manufacturer_id = int.from_bytes(data[offset:offset+5], 'big')
        offset += 5
        terminal_model = data[offset:offset+20].decode('gbk', errors='ignore').rstrip('\x00')
        offset += 20
        terminal_id = data[offset:offset+7].decode('ascii', errors='ignore').rstrip('\x00')
        offset += 7
        plate_color = data[offset]
        offset += 1
        plate_number = data[offset:offset+len(data)-offset].decode('gbk', errors='ignore').rstrip('\x00')
        
        return {
            'province_id': province_id,
            'city_id': city_id,
            'manufacturer_id': manufacturer_id,
            'terminal_model': terminal_model,
            'terminal_id': terminal_id,
            'plate_color': plate_color,
            'plate_number': plate_number
        } 
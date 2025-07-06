"""
JT808协议头解析单元测试
"""
import sys
import os
import unittest
import importlib.util

# 动态加载jt808_parser模块
jt808_parser_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../jt808proxy/core/jt808_parser.py'))
spec = importlib.util.spec_from_file_location("jt808_parser", jt808_parser_path)
jt808_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jt808_parser)
JT808Parser = jt808_parser.JT808Parser

class TestJT808Parser(unittest.TestCase):
    def test_parse_header_normal(self):
        # 构造一个标准JT808协议头（无分包）
        # 消息ID: 0x0200, 消息体属性: 0x0040, 手机号: 013912345678, 流水号: 0x0001
        # 手机号BCD: 0x01 0x39 0x12 0x34 0x56 0x78
        data = bytes.fromhex('02 00 00 40 01 39 12 34 56 78 00 01')
        header = JT808Parser.parse_header(data)
        self.assertIsNotNone(header)
        self.assertEqual(header.msg_id, 0x0200)
        self.assertEqual(header.body_props, 0x0040)
        self.assertEqual(header.phone, '13912345678')
        self.assertEqual(header.msg_seq, 1)
        self.assertIsNone(header.pkg_total)
        self.assertIsNone(header.pkg_index)

    def test_parse_header_subpackage(self):
        # 构造一个带分包的协议头
        # 消息体属性: 0x2040 (分包标志位)
        data = bytes.fromhex('02 00 20 40 01 39 12 34 56 78 00 01 00 03 00 02')
        header = JT808Parser.parse_header(data)
        self.assertIsNotNone(header)
        self.assertEqual(header.body_props, 0x2040)
        self.assertEqual(header.pkg_total, 3)
        self.assertEqual(header.pkg_index, 2)

    def test_parse_header_invalid(self):
        # 长度不足
        data = bytes.fromhex('02 00 00 40 01 39 12')
        header = JT808Parser.parse_header(data)
        self.assertIsNone(header)

if __name__ == '__main__':
    unittest.main() 
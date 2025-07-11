# JT808Proxy

**版本：V0.2**

## 版本历史
- **V0.2**（2024-12-19）：
  - 统一主程序目录为小写 jt808proxy
  - 端口规范：TCP服务16900，前端7000，API 7700
  - 文档与代码全面适配小写目录
  - 修复数据库与测试兼容性问题
  - 完善技术问题排查指南和开发经验总结
- **V0.1**：项目初始化，基础功能实现

## 简介
JT808Proxy是一个基于JT/T 808协议的车辆通信代理服务系统，包含TCP Proxy服务、Web前台和Web后台服务，支持双向TCP通信、协议解析、定位数据和车辆信息存储、智能转发、链路监控和日志、前端管理界面和后端REST API。

## 目录结构
```
jt808proxy/           # 主程序包，包含 TCP Proxy 服务的核心代码
├── core/             # JT808 协议解析、转发等核心逻辑
├── storage/          # 数据存储、每日分表等相关实现
├── monitor/          # 链路监控、日志等功能模块
├── docs/             # 项目文档
frontend/             # 前端 Vue3 项目
api/                  # FastAPI 后端
...
```

## 端口规范
- TCP服务端口：16900
- Web前端端口：7000
- API服务端口：7700

## 主要功能
- ✅ TCP服务基础实现
- ✅ JT808协议解析
- ✅ 监控与运行日志
- ✅ Web后端API开发（基础架构）
- ✅ 车辆管理基础API
- ✅ 系统健康检查
- ✅ 完整的技术文档

## 技术架构

```
jt808proxy/
├── api/                    # Web后端API
│   ├── main.py            # FastAPI主应用
│   ├── models/            # 数据模型
│   ├── routers/           # API路由
│   └── services/          # 业务逻辑层
├── jt808proxy/            # 核心模块
│   ├── core/              # 核心功能
│   ├── monitor/           # 监控模块
│   └── storage/           # 数据存储
├── docs/                  # 项目文档
├── test/                  # 测试文件
└── requirements.txt       # 依赖管理
```

## 技术栈

- **Web框架**: FastAPI 0.104.1
- **数据验证**: Pydantic 2.6.1
- **数据库**: SQLite
- **测试框架**: pytest 8.0.0
- **协议**: JT/T 808
- **通信**: TCP Socket

## 快速开始

### 环境要求

- Python 3.8+
- Git

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/gm970191/JT808Proxy.git
   cd JT808Proxy
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行Web API服务**
   ```bash
   cd api
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **访问API文档**
   ```
   http://localhost:8000/docs
   ```

### API端点

#### 车辆管理API
```
GET    /api/vehicles/                    # 获取车辆列表
POST   /api/vehicles/                    # 创建车辆
GET    /api/vehicles/{terminal_phone}    # 获取单个车辆
PUT    /api/vehicles/{terminal_phone}    # 更新车辆
DELETE /api/vehicles/{terminal_phone}    # 删除车辆
GET    /api/vehicles/{terminal_phone}/changes  # 变更历史
GET    /api/vehicles/stats/summary       # 统计信息
```

#### 定位数据API
```
GET    /api/locations/{terminal_phone}           # 定位数据
GET    /api/locations/{terminal_phone}/latest    # 最新定位
GET    /api/locations/{terminal_phone}/stats     # 定位统计
GET    /api/locations/{terminal_phone}/alarms    # 报警数据
GET    /api/locations/{terminal_phone}/track     # 轨迹数据
GET    /api/locations/stats/overview             # 定位概览
```

#### 系统API
```
GET    /health                    # 健康检查
GET    /api/system/status         # 系统状态
GET    /docs                      # API文档
```

## 测试

运行测试套件：
```bash
python -m pytest test/ -v
```

当前测试状态：
- 车辆API测试：2/7 通过 (28.6%)
- 定位API测试：0/6 通过 (0%)
- 系统API测试：3/3 通过 (100%)
- 总体通过率：5/16 (31.25%)

## 项目文档

详细文档请查看 `docs/` 目录：

- [项目进度总结](docs/项目进度总结.md)
- [V0.2开发经验总结](docs/V0.2开发经验总结.md)
- [Web后端API开发最佳实践](docs/Web后端API开发最佳实践.md)
- [技术问题排查指南](docs/技术问题排查指南.md)
- [需求分析](docs/需求分析.md)
- [开发环境搭建](docs/开发环境搭建.md)
- [JT808协议解析与转发](docs/JT808协议解析与转发.md)

## 开发计划

### 当前阶段 (第六阶段)
- [x] FastAPI应用架构搭建
- [x] 数据库连接和表结构设计
- [x] 车辆管理基础API
- [x] 系统健康检查API
- [ ] 车辆管理完整API
- [ ] 定位数据管理API
- [ ] 数据验证和错误处理完善

### 下一阶段 (第七阶段)
- [ ] 数据存储与每日分表
- [ ] 性能优化
- [ ] 缓存机制

### 后续阶段
- [ ] 前端管理界面开发
- [ ] 系统集成与部署
- [ ] 生产环境优化

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目链接: https://github.com/gm970191/JT808Proxy
- 作者: 星辰大海

## 更新日志

### V0.2 (2024-12-19)
- 🔧 端口配置规范化：TCP服务16900，前端7000，API 7700
- 📁 目录结构统一：主程序目录统一为小写jt808proxy
- 🐛 测试修复：修复数据库测试中的重复定义和字段名错误
- 📚 文档完善：更新项目结构说明、技术问题排查指南等文档
- 🏷️ 版本管理：成功发布V0.2版本并推送到GitHub
- 📖 经验总结：创建V0.2开发经验总结文档

### V0.1 (2024-12-19)
- 🎉 项目初始化
- ✅ FastAPI应用架构搭建
- ✅ 车辆管理基础API实现
- ✅ 数据库连接和表结构设计
- ✅ 系统健康检查API
- ✅ 完整的技术文档和最佳实践
- 📊 测试通过率: 31.25% (5/16)

---

**注意**: 本项目仍在积极开发中，API接口可能会发生变化。请查看最新文档获取详细信息。

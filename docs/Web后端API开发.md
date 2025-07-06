# Web后端API开发

## 概述

本文档记录JT808Proxy项目第六阶段Web后端API的开发过程，包括API设计、实现、测试和文档。

## 技术栈

- **Web框架**: FastAPI
- **数据验证**: Pydantic
- **服务器**: Uvicorn（端口：7700）
- **测试**: pytest + TestClient

## 项目结构

```
api/
├── main.py                 # FastAPI主应用
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── vehicle.py         # 车辆信息模型
│   └── location.py        # 定位数据模型
├── routers/               # API路由
│   ├── __init__.py
│   ├── vehicle.py         # 车辆管理路由
│   └── location.py        # 定位数据路由
└── services/              # 业务服务层
    ├── __init__.py
    ├── vehicle_service.py # 车辆服务
    └── location_service.py # 定位服务
```

## API设计

### 1. 车辆管理API

#### 1.1 创建车辆
- **路径**: `POST /api/vehicles/`
- **功能**: 创建新的车辆信息
- **请求体**: VehicleCreate模型
- **响应**: VehicleResponse模型

#### 1.2 获取车辆列表
- **路径**: `GET /api/vehicles/`
- **功能**: 分页获取车辆列表
- **查询参数**: 
  - page: 页码
  - size: 页大小
  - terminal_phone: 终端手机号过滤
  - plate_number: 车牌号过滤
- **响应**: VehicleListResponse模型

#### 1.3 获取单个车辆
- **路径**: `GET /api/vehicles/{terminal_phone}`
- **功能**: 根据终端手机号获取车辆信息
- **响应**: VehicleResponse模型

#### 1.4 更新车辆信息
- **路径**: `PUT /api/vehicles/{terminal_phone}`
- **功能**: 更新车辆信息
- **请求体**: VehicleUpdate模型
- **响应**: VehicleResponse模型

#### 1.5 删除车辆
- **路径**: `DELETE /api/vehicles/{terminal_phone}`
- **功能**: 删除车辆信息
- **响应**: 成功消息

#### 1.6 获取变更历史
- **路径**: `GET /api/vehicles/{terminal_phone}/changes`
- **功能**: 获取车辆信息变更历史
- **查询参数**: limit - 限制条数
- **响应**: VehicleChangeLog列表

#### 1.7 获取统计信息
- **路径**: `GET /api/vehicles/stats/summary`
- **功能**: 获取车辆统计概览
- **响应**: 统计信息

### 2. 定位数据API

#### 2.1 获取定位数据
- **路径**: `GET /api/locations/{terminal_phone}`
- **功能**: 获取指定时间范围的定位数据
- **查询参数**:
  - start_date: 开始日期
  - end_date: 结束日期
  - limit: 限制条数
- **响应**: LocationResponse模型

#### 2.2 获取最新定位
- **路径**: `GET /api/locations/{terminal_phone}/latest`
- **功能**: 获取最新定位数据
- **响应**: LocationData模型

#### 2.3 获取定位统计
- **路径**: `GET /api/locations/{terminal_phone}/stats`
- **功能**: 获取定位数据统计信息
- **查询参数**:
  - start_date: 开始日期
  - end_date: 结束日期
- **响应**: LocationStats模型

#### 2.4 获取报警数据
- **路径**: `GET /api/locations/{terminal_phone}/alarms`
- **功能**: 获取报警数据
- **查询参数**:
  - start_date: 开始日期
  - end_date: 结束日期
  - limit: 限制条数
- **响应**: 报警数据列表

#### 2.5 获取轨迹数据
- **路径**: `GET /api/locations/{terminal_phone}/track`
- **功能**: 获取轨迹数据
- **查询参数**:
  - start_date: 开始日期
  - end_date: 结束日期
  - min_interval: 最小时间间隔
- **响应**: 轨迹点列表

#### 2.6 获取定位概览
- **路径**: `GET /api/locations/stats/overview`
- **功能**: 获取定位数据概览
- **响应**: 概览统计信息

### 3. 系统API

#### 3.1 根路径
- **路径**: `GET /`
- **功能**: API服务信息
- **响应**: 服务基本信息

#### 3.2 健康检查
- **路径**: `GET /health`
- **功能**: 服务健康检查
- **响应**: 健康状态

#### 3.3 系统状态
- **路径**: `GET /api/status`
- **功能**: 获取系统运行状态
- **响应**: 系统状态信息

## 数据模型

### 车辆信息模型

```python
class VehicleBase(BaseModel):
    terminal_phone: str
    vehicle_id: Optional[str]
    plate_number: Optional[str]
    vehicle_type: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    color: Optional[str]

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    vehicle_id: Optional[str]
    plate_number: Optional[str]
    vehicle_type: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    color: Optional[str]

class VehicleResponse(VehicleBase):
    id: int
    created_at: datetime
    updated_at: datetime

class VehicleChangeLog(BaseModel):
    id: int
    terminal_phone: str
    field_name: str
    old_value: Optional[str]
    new_value: Optional[str]
    change_time: datetime

class VehicleListResponse(BaseModel):
    vehicles: list[VehicleResponse]
    total: int
    page: int
    size: int
```

### 定位数据模型

```python
class LocationData(BaseModel):
    id: int
    terminal_phone: str
    msg_seq: int
    alarm_flag: int
    status: int
    latitude: float
    longitude: float
    altitude: int
    speed: int
    direction: int
    time: datetime
    mileage: int
    fuel_consumption: int
    alarm_event_id: int
    created_at: datetime

class LocationQuery(BaseModel):
    terminal_phone: str
    start_date: date
    end_date: date
    limit: Optional[int]

class LocationResponse(BaseModel):
    locations: List[LocationData]
    total: int
    terminal_phone: str
    start_date: date
    end_date: date

class LocationStats(BaseModel):
    terminal_phone: str
    total_records: int
    date_range: str
    avg_speed: float
    max_speed: int
    total_mileage: int
    alarm_count: int
```

## 服务层设计

### 车辆服务 (VehicleService)

```python
class VehicleService:
    def create_vehicle(self, vehicle: VehicleCreate) -> VehicleResponse
    def get_vehicles(self, page: int, size: int, ...) -> VehicleListResponse
    def get_vehicle_by_phone(self, terminal_phone: str) -> Optional[VehicleResponse]
    def update_vehicle(self, terminal_phone: str, vehicle_update: VehicleUpdate) -> Optional[VehicleResponse]
    def delete_vehicle(self, terminal_phone: str) -> bool
    def get_vehicle_changes(self, terminal_phone: str, limit: int) -> List[VehicleChangeLog]
    def get_vehicle_stats(self) -> Dict[str, Any]
```

### 定位服务 (LocationService)

```python
class LocationService:
    def get_location_data(self, terminal_phone: str, start_date: date, end_date: date, limit: int) -> LocationResponse
    def get_latest_location(self, terminal_phone: str) -> Optional[LocationData]
    def get_location_stats(self, terminal_phone: str, start_date: date, end_date: date) -> LocationStats
    def get_alarm_data(self, terminal_phone: str, start_date: date, end_date: date, limit: int) -> List[Dict[str, Any]]
    def get_track_data(self, terminal_phone: str, start_date: date, end_date: date, min_interval: int) -> List[Dict[str, Any]]
    def get_location_overview(self) -> Dict[str, Any]
```

## 错误处理

### HTTP状态码

- **200**: 成功
- **400**: 请求参数错误
- **404**: 资源不存在
- **500**: 服务器内部错误

### 错误响应格式

```json
{
    "detail": "错误描述信息"
}
```

## 中间件配置

### CORS配置

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 测试

### 测试覆盖

- 车辆管理API测试
- 定位数据API测试
- 系统API测试
- API文档测试

### 测试运行

```bash
# 运行API测试
python -m pytest test/test_api.py -v

# 运行所有测试
python -m pytest test/ -v
```

## 启动服务

### 开发模式

```bash
# 启动API服务
cd api
python main.py
```

### 生产模式

```bash
# 使用uvicorn启动
uvicorn api.main:app --host 0.0.0.0 --port 7900 --workers 4
```

## API文档

### 自动生成文档

- **Swagger UI**: http://localhost:7900/docs
- **ReDoc**: http://localhost:7900/redoc

### 文档特性

- 自动生成API文档
- 交互式测试界面
- 请求/响应示例
- 数据模型说明

## 性能优化

### 数据库查询优化

- 使用索引优化查询性能
- 分页查询减少数据传输
- 缓存常用数据

### 响应优化

- 异步处理提高并发性能
- 数据压缩减少传输量
- 合理的缓存策略

## 安全考虑

### 输入验证

- 使用Pydantic进行数据验证
- 参数类型和范围检查
- SQL注入防护

### 访问控制

- 生产环境需要添加认证授权
- API访问频率限制
- 敏感数据保护

## 部署配置

### 环境变量

```bash
# API服务配置
API_HOST=0.0.0.0
API_PORT=7900
API_WORKERS=4

# 数据库配置
DB_PATH=./data/jt808proxy.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=./logs/api.log
```

### Docker部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7900

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7900"]
```

## 监控和日志

### 日志记录

- 请求日志记录
- 错误日志记录
- 性能监控日志

### 健康检查

- 服务健康状态检查
- 数据库连接检查
- 系统资源监控

## 总结

第六阶段成功实现了完整的Web后端API系统，包括：

1. **完整的API设计**: 车辆管理和定位数据两大核心功能模块
2. **分层架构**: 模型层、路由层、服务层清晰分离
3. **数据验证**: 使用Pydantic确保数据完整性
4. **错误处理**: 统一的错误处理和响应格式
5. **自动文档**: Swagger和ReDoc自动生成API文档
6. **全面测试**: 覆盖所有API接口的测试用例
7. **性能优化**: 异步处理和数据库查询优化

API服务运行在7900端口，为前端应用提供完整的数据接口支持。下一阶段将开发Web前端界面，与API服务进行集成。 
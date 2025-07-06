import request from './index'

export interface ConnectionInfo {
  id: string
  vehicle_id: string
  client_ip: string
  client_port: number
  server_ip: string
  server_port: number
  status: 'connected' | 'disconnected' | 'error'
  connect_time: string
  last_heartbeat: string
  data_count: number
  error_count: number
}

export interface SystemStatus {
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  network_in: number
  network_out: number
  active_connections: number
  total_connections: number
  uptime: number
}

export interface LogEntry {
  id: number
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR'
  message: string
  timestamp: string
  source: string
  details?: string
}

export interface MonitorQuery {
  level?: string
  start_time?: string
  end_time?: string
  page?: number
  size?: number
}

// 获取连接信息列表
export const getConnections = () => {
  return request.get<ConnectionInfo[]>('/monitor/connections')
}

// 获取连接详情
export const getConnection = (id: string) => {
  return request.get<ConnectionInfo>(`/monitor/connections/${id}`)
}

// 断开连接
export const disconnectConnection = (id: string) => {
  return request.delete(`/monitor/connections/${id}`)
}

// 获取系统状态
export const getSystemStatus = () => {
  return request.get<SystemStatus>('/monitor/system')
}

// 获取系统状态历史
export const getSystemStatusHistory = (hours: number = 24) => {
  return request.get<SystemStatus[]>('/monitor/system/history', {
    params: { hours }
  })
}

// 获取日志列表
export const getLogs = (params: MonitorQuery) => {
  return request.get<LogEntry[]>('/monitor/logs', { params })
}

// 获取日志详情
export const getLog = (id: number) => {
  return request.get<LogEntry>(`/monitor/logs/${id}`)
}

// 清除日志
export const clearLogs = (before?: string) => {
  return request.delete('/monitor/logs', {
    params: { before }
  })
}

// 获取实时监控数据
export const getRealTimeData = () => {
  return request.get('/monitor/realtime')
}

// 获取性能统计
export const getPerformanceStats = (period: 'hour' | 'day' | 'week' = 'day') => {
  return request.get('/monitor/performance', {
    params: { period }
  })
}

// 获取告警列表
export const getAlerts = (params: MonitorQuery) => {
  return request.get('/monitor/alerts', { params })
}

// 确认告警
export const acknowledgeAlert = (id: number) => {
  return request.put(`/monitor/alerts/${id}/acknowledge`)
}

// 获取监控配置
export const getMonitorConfig = () => {
  return request.get('/monitor/config')
}

// 更新监控配置
export const updateMonitorConfig = (config: any) => {
  return request.put('/monitor/config', config)
} 
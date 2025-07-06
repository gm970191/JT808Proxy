import request from './index'

export interface ConfigItem {
  id: number
  key: string
  value: string
  description?: string
  category: string
  created_at: string
  updated_at: string
}

export interface ConfigCategory {
  category: string
  display_name: string
  description: string
  configs: ConfigItem[]
}

export interface ConfigCreate {
  key: string
  value: string
  description?: string
  category: string
}

export interface ConfigUpdate {
  value: string
  description?: string
}

export interface SystemConfig {
  [key: string]: any
}

// 获取配置列表
export const getConfigs = (params?: { category?: string }) => {
  return request.get<ConfigItem[]>('/api/config', { params })
}

// 获取配置分类
export const getConfigCategories = () => {
  return request.get<ConfigCategory[]>('/api/config/categories')
}

// 获取系统配置
export const getSystemConfig = () => {
  return request.get<SystemConfig>('/api/config/system')
}

// 更新系统配置
export const updateSystemConfig = (config: SystemConfig) => {
  return request.put('/api/config/system', config)
}

// 创建配置
export const createConfig = (data: ConfigCreate) => {
  return request.post<ConfigItem>('/api/config', data)
}

// 更新配置
export const updateConfig = (key: string, data: ConfigUpdate) => {
  return request.put<ConfigItem>(`/api/config/${key}`, data)
}

// 删除配置
export const deleteConfig = (key: string) => {
  return request.delete(`/api/config/${key}`)
}

// 初始化默认配置
export const initDefaultConfigs = () => {
  return request.post('/api/config/init')
}

// 重新加载配置
export const reloadConfigs = () => {
  return request.post('/api/config/reload')
} 
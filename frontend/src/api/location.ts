import request from './index'

export interface LocationData {
  id?: number
  vehicle_id: string
  latitude: number
  longitude: number
  altitude: number
  speed: number
  direction: number
  timestamp: string
  status: string
  created_at?: string
  updated_at?: string
}

export interface LocationQuery {
  vehicle_id?: string
  start_time?: string
  end_time?: string
  page?: number
  size?: number
}

export interface LocationStats {
  total_count: number
  today_count: number
  online_vehicles: number
  offline_vehicles: number
}

// 获取定位数据列表
export const getLocations = (params: LocationQuery) => {
  return request.get<LocationData[]>('/locations', { params })
}

// 获取定位数据详情
export const getLocation = (id: number) => {
  return request.get<LocationData>(`/locations/${id}`)
}

// 创建定位数据
export const createLocation = (data: LocationData) => {
  return request.post<LocationData>('/locations', data)
}

// 更新定位数据
export const updateLocation = (id: number, data: Partial<LocationData>) => {
  return request.put<LocationData>(`/locations/${id}`, data)
}

// 删除定位数据
export const deleteLocation = (id: number) => {
  return request.delete(`/locations/${id}`)
}

// 获取定位统计信息
export const getLocationStats = () => {
  return request.get<LocationStats>('/locations/stats')
}

// 获取车辆最新定位
export const getVehicleLatestLocation = (vehicleId: string) => {
  return request.get<LocationData>(`/locations/vehicle/${vehicleId}/latest`)
}

// 获取车辆历史轨迹
export const getVehicleTrack = (vehicleId: string, startTime: string, endTime: string) => {
  return request.get<LocationData[]>(`/locations/vehicle/${vehicleId}/track`, {
    params: { start_time: startTime, end_time: endTime }
  })
}

// 批量删除定位数据
export const batchDeleteLocations = (ids: number[]) => {
  return request.delete('/locations/batch', { data: { ids } })
}

// 导出定位数据
export const exportLocations = (params: LocationQuery) => {
  return request.get('/locations/export', { 
    params,
    responseType: 'blob'
  })
} 
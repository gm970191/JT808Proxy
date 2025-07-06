import api from './index'

export interface Vehicle {
  id: number
  terminal_phone: string
  vehicle_id?: string
  plate_number?: string
  vehicle_type?: string
  manufacturer?: string
  model?: string
  color?: string
  created_at: string
  updated_at: string
}

export interface VehicleCreate {
  terminal_phone: string
  vehicle_id?: string
  plate_number?: string
  vehicle_type?: string
  manufacturer?: string
  model?: string
  color?: string
}

export interface VehicleUpdate {
  vehicle_id?: string
  plate_number?: string
  vehicle_type?: string
  manufacturer?: string
  model?: string
  color?: string
}

export interface VehicleListResponse {
  vehicles: Vehicle[]
  total: number
  page: number
  size: number
}

// 车辆管理API
export const vehicleApi = {
  // 获取车辆列表
  getVehicles(params: {
    page?: number
    size?: number
    terminal_phone?: string
    plate_number?: string
  }) {
    return api.get<VehicleListResponse>('/vehicles/', { params })
  },

  // 创建车辆
  createVehicle(data: VehicleCreate) {
    return api.post<Vehicle>('/vehicles/', data)
  },

  // 获取单个车辆
  getVehicle(terminal_phone: string) {
    return api.get<Vehicle>(`/vehicles/${terminal_phone}`)
  },

  // 更新车辆
  updateVehicle(terminal_phone: string, data: VehicleUpdate) {
    return api.put<Vehicle>(`/vehicles/${terminal_phone}`, data)
  },

  // 删除车辆
  deleteVehicle(terminal_phone: string) {
    return api.delete(`/vehicles/${terminal_phone}`)
  },

  // 获取车辆变更历史
  getVehicleChanges(terminal_phone: string, limit?: number) {
    return api.get(`/vehicles/${terminal_phone}/changes`, { params: { limit } })
  },

  // 获取车辆统计
  getVehicleStats() {
    return api.get('/vehicles/stats/summary')
  }
} 
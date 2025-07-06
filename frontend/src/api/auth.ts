import request from './index'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: {
    id: number
    username: string
    email?: string
    role: string
    created_at: string
    updated_at: string
    last_login?: string
  }
}

export interface UserInfo {
  id: number
  username: string
  email?: string
  role: string
  created_at: string
  updated_at: string
  last_login?: string
}

export interface UserCreate {
  username: string
  password: string
  email?: string
  role: string
}

export interface UserUpdate {
  email?: string
  role?: string
  password?: string
}

// 用户登录
export const login = (data: LoginRequest) => {
  return request.post<LoginResponse>('/api/auth/login', data)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<UserInfo>('/api/auth/me')
}

// 创建用户
export const createUser = (data: UserCreate) => {
  return request.post<UserInfo>('/api/auth/users', data)
}

// 获取用户列表
export const getUsers = (params?: { page?: number; size?: number }) => {
  return request.get<UserInfo[]>('/api/auth/users', { params })
}

// 更新用户信息
export const updateUser = (userId: number, data: UserUpdate) => {
  return request.put<UserInfo>(`/api/auth/users/${userId}`, data)
}

// 删除用户
export const deleteUser = (userId: number) => {
  return request.delete(`/api/auth/users/${userId}`)
} 
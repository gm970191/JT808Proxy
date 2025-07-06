import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserInfo {
  id: number
  username: string
  email: string
  role: string
  avatar?: string
  lastLogin?: string
}

export const useUserStore = defineStore('user', () => {
  // 状态
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string>('')
  const isLoggedIn = ref(false)

  // 计算属性
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const displayName = computed(() => userInfo.value?.username || '未登录')

  // 登录
  const login = async (username: string, password: string) => {
    try {
      // 模拟登录API调用
      if (username === 'admin' && password === 'admin') {
        const user: UserInfo = {
          id: 1,
          username: 'admin',
          email: 'admin@jt808proxy.com',
          role: 'admin',
          lastLogin: new Date().toISOString()
        }
        
        userInfo.value = user
        token.value = 'mock-token-' + Date.now()
        isLoggedIn.value = true
        
        // 保存到本地存储
        localStorage.setItem('userInfo', JSON.stringify(user))
        localStorage.setItem('token', token.value)
        
        return { success: true }
      } else {
        return { success: false, message: '用户名或密码错误' }
      }
    } catch (error) {
      return { success: false, message: '登录失败' }
    }
  }

  // 登出
  const logout = () => {
    userInfo.value = null
    token.value = ''
    isLoggedIn.value = false
    
    // 清除本地存储
    localStorage.removeItem('userInfo')
    localStorage.removeItem('token')
  }

  // 初始化用户信息
  const initUserInfo = () => {
    const savedUserInfo = localStorage.getItem('userInfo')
    const savedToken = localStorage.getItem('token')
    
    if (savedUserInfo && savedToken) {
      try {
        userInfo.value = JSON.parse(savedUserInfo)
        token.value = savedToken
        isLoggedIn.value = true
      } catch (error) {
        console.error('Failed to parse saved user info:', error)
        logout()
      }
    }
  }

  // 更新用户信息
  const updateUserInfo = (info: Partial<UserInfo>) => {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...info }
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
    }
  }

  return {
    // 状态
    userInfo,
    token,
    isLoggedIn,
    
    // 计算属性
    isAdmin,
    displayName,
    
    // 方法
    login,
    logout,
    initUserInfo,
    updateUserInfo
  }
}) 
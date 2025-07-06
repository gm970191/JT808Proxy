// 格式化时间
export const formatTime = (time: string | Date, format: string = 'YYYY-MM-DD HH:mm:ss'): string => {
  const date = new Date(time)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

// 格式化文件大小
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化速度
export const formatSpeed = (speed: number): string => {
  if (speed < 1) return '0 km/h'
  return `${speed.toFixed(1)} km/h`
}

// 格式化距离
export const formatDistance = (distance: number): string => {
  if (distance < 1000) return `${distance.toFixed(0)} m`
  return `${(distance / 1000).toFixed(2)} km`
}

// 计算两点间距离（米）
export const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
  const R = 6371000 // 地球半径（米）
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

// 防抖函数
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// 节流函数
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// 深拷贝
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as unknown as T
  if (typeof obj === 'object') {
    const clonedObj = {} as T
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        clonedObj[key] = deepClone(obj[key])
      }
    }
    return clonedObj
  }
  return obj
}

// 生成UUID
export const generateUUID = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

// 验证车牌号
export const validatePlateNumber = (plateNumber: string): boolean => {
  const pattern = /^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-Z0-9]{5}$/
  return pattern.test(plateNumber)
}

// 验证手机号
export const validatePhone = (phone: string): boolean => {
  const pattern = /^1[3-9]\d{9}$/
  return pattern.test(phone)
}

// 验证IP地址
export const validateIP = (ip: string): boolean => {
  const pattern = /^(\d{1,3}\.){3}\d{1,3}$/
  if (!pattern.test(ip)) return false
  
  const parts = ip.split('.')
  return parts.every(part => {
    const num = parseInt(part)
    return num >= 0 && num <= 255
  })
}

// 获取状态颜色
export const getStatusColor = (status: string): string => {
  const statusColors: Record<string, string> = {
    'online': '#67C23A',
    'offline': '#F56C6C',
    'connected': '#67C23A',
    'disconnected': '#F56C6C',
    'error': '#E6A23C',
    'warning': '#E6A23C',
    'info': '#909399'
  }
  return statusColors[status] || '#909399'
}

// 获取状态文本
export const getStatusText = (status: string): string => {
  const statusTexts: Record<string, string> = {
    'online': '在线',
    'offline': '离线',
    'connected': '已连接',
    'disconnected': '已断开',
    'error': '错误',
    'warning': '警告',
    'info': '信息'
  }
  return statusTexts[status] || status
} 
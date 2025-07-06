<template>
  <div class="monitor-container">
    <h2>链路监控</h2>
    
    <!-- 连接状态 -->
    <el-row :gutter="20" class="status-row">
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>TCP连接状态</span>
          </template>
          <div class="connection-status">
            <div class="status-item">
              <span class="label">总连接数:</span>
              <span class="value">{{ connectionStats.total }}</span>
            </div>
            <div class="status-item">
              <span class="label">活跃连接:</span>
              <span class="value success">{{ connectionStats.active }}</span>
            </div>
            <div class="status-item">
              <span class="label">断开连接:</span>
              <span class="value warning">{{ connectionStats.disconnected }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>数据流量</span>
          </template>
          <div class="traffic-stats">
            <div class="traffic-item">
              <span class="label">接收数据:</span>
              <span class="value">{{ trafficStats.received }} KB</span>
            </div>
            <div class="traffic-item">
              <span class="label">发送数据:</span>
              <span class="value">{{ trafficStats.sent }} KB</span>
            </div>
            <div class="traffic-item">
              <span class="label">数据包数:</span>
              <span class="value">{{ trafficStats.packets }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>系统性能</span>
          </template>
          <div class="performance-stats">
            <div class="perf-item">
              <span class="label">CPU使用率:</span>
              <span class="value">{{ performanceStats.cpu }}%</span>
            </div>
            <div class="perf-item">
              <span class="label">内存使用率:</span>
              <span class="value">{{ performanceStats.memory }}%</span>
            </div>
            <div class="perf-item">
              <span class="label">磁盘使用率:</span>
              <span class="value">{{ performanceStats.disk }}%</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 连接列表 -->
    <el-card class="connection-list">
      <template #header>
        <span>连接列表</span>
        <el-button style="float: right; padding: 3px 0" link @click="refreshConnections">
          刷新
        </el-button>
      </template>
      <el-table :data="connections" v-loading="loading" stripe>
        <el-table-column prop="terminal_phone" label="终端手机号" width="150" />
        <el-table-column prop="remote_address" label="远程地址" width="150" />
        <el-table-column prop="connect_time" label="连接时间" width="180" />
        <el-table-column prop="last_activity" label="最后活动" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '活跃' : '断开' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="data_count" label="数据包数" width="100" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleViewDetails(row)">详情</el-button>
            <el-button size="small" type="danger" @click="handleDisconnect(row)">断开</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { getConnections, getSystemStatus, getRealTimeData, disconnectConnection } from '@/api/monitor'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const loading = ref(false)
const connections = ref<any[]>([])

// 连接统计
const connectionStats = reactive({
  total: 0,
  active: 0,
  disconnected: 0
})

// 流量统计
const trafficStats = reactive({
  received: 0,
  sent: 0,
  packets: 0
})

// 性能统计
const performanceStats = reactive({
  cpu: 0,
  memory: 0,
  disk: 0
})

// 定时器
let refreshTimer: number | null = null

// 获取连接列表
const fetchConnections = async () => {
  loading.value = true
  try {
    const response: any = await getConnections()
    if (response.data) {
      connections.value = response.data
      // 更新连接统计
      connectionStats.total = response.data.length
      connectionStats.active = response.data.filter((conn: any) => conn.status === 'active').length
      connectionStats.disconnected = response.data.filter((conn: any) => conn.status === 'disconnected').length
    }
  } catch (error) {
    console.error('获取连接列表失败:', error)
    ElMessage.error('获取连接列表失败')
  } finally {
    loading.value = false
  }
}

// 获取系统状态
const fetchSystemStatus = async () => {
  try {
    const response: any = await getSystemStatus()
    if (response.data) {
      const data = response.data
      performanceStats.cpu = data.cpu_usage || 0
      performanceStats.memory = data.memory_usage || 0
      performanceStats.disk = data.disk_usage || 0
      
      // 更新流量统计
      trafficStats.received = Math.round((data.received_bytes || 0) / 1024) // 转换为KB
      trafficStats.sent = Math.round((data.sent_bytes || 0) / 1024) // 转换为KB
      trafficStats.packets = data.packets_count || 0
      
      // 更新连接统计
      connectionStats.total = data.total_connections || 0
      connectionStats.active = data.active_connections || 0
      connectionStats.disconnected = data.disconnected_connections || 0
    }
  } catch (error) {
    console.error('获取系统状态失败:', error)
  }
}

// 获取实时数据
const fetchRealTimeData = async () => {
  try {
    console.log('🔄 开始获取实时数据...')
    const response: any = await getRealTimeData()
    console.log('📡 API响应:', response)
    
    if (response.data) {
      const data = response.data
      console.log('📊 解析的数据:', data)
      
      // 更新连接统计
      if (data.connection_stats) {
        connectionStats.total = data.connection_stats.total_connections || 0
        connectionStats.active = data.connection_stats.active_connections || 0
        connectionStats.disconnected = data.connection_stats.disconnected_connections || 0
        console.log('🔗 更新连接统计:', connectionStats)
      }
      
      // 更新流量统计
      if (data.traffic_stats) {
        trafficStats.received = Math.round((data.traffic_stats.received_bytes || 0) / 1024)
        trafficStats.sent = Math.round((data.traffic_stats.sent_bytes || 0) / 1024)
        trafficStats.packets = data.traffic_stats.packets_count || 0
        console.log('📡 更新流量统计:', trafficStats)
      }
      
      // 更新性能统计
      if (data.performance_stats) {
        performanceStats.cpu = data.performance_stats.cpu_usage || 0
        performanceStats.memory = data.performance_stats.memory_usage || 0
        performanceStats.disk = data.performance_stats.disk_usage || 0
        console.log('⚡ 更新性能统计:', performanceStats)
      }
      
      // 更新连接列表
      if (data.connections) {
        connections.value = data.connections
        console.log('📋 更新连接列表:', connections.value.length, '个连接')
      }
      
      console.log('✅ 实时数据更新完成')
    } else {
      console.warn('⚠️ API响应数据结构异常:', response)
    }
  } catch (error) {
    console.error('❌ 获取实时数据失败:', error)
  }
}

// 刷新连接
const refreshConnections = () => {
  fetchRealTimeData()
}

// 查看详情
const handleViewDetails = (row: any) => {
  console.log('查看详情:', row)
  ElMessage.info(`查看终端 ${row.terminal_phone} 的详细信息`)
}

// 断开连接
const handleDisconnect = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要断开终端 ${row.terminal_phone} 的连接吗？`,
      '确认断开',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const response: any = await disconnectConnection(row.id)
    if (response.data?.code === 200) {
      ElMessage.success('断开连接成功')
      refreshConnections()
    } else {
      ElMessage.error('断开连接失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('断开连接失败:', error)
      ElMessage.error('断开连接失败')
    }
  }
}

// 启动定时刷新
const startAutoRefresh = () => {
  refreshTimer = setInterval(() => {
    fetchRealTimeData()
  }, 5000) // 每5秒刷新一次
}

// 停止定时刷新
const stopAutoRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

onMounted(() => {
  console.log('🚀 监控页面初始化...')
  console.log('📊 初始数据状态:')
  console.log('  连接统计:', connectionStats)
  console.log('  流量统计:', trafficStats)
  console.log('  性能统计:', performanceStats)
  
  // 初始化时获取所有数据
  fetchRealTimeData()
  startAutoRefresh()
  
  console.log('✅ 监控页面初始化完成')
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.monitor-container {
  padding: 20px;
}

.status-row {
  margin-bottom: 20px;
}

.connection-status,
.traffic-stats,
.performance-stats {
  padding: 10px 0;
}

.status-item,
.traffic-item,
.perf-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.label {
  color: #606266;
}

.value {
  font-weight: bold;
  color: #303133;
}

.value.success {
  color: #67c23a;
}

.value.warning {
  color: #e6a23c;
}

.connection-list {
  margin-bottom: 20px;
}
</style> 
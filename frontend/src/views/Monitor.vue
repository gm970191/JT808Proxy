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
        <el-button style="float: right; padding: 3px 0" type="text" @click="refreshConnections">
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
import { ref, reactive, onMounted } from 'vue'

// 响应式数据
const loading = ref(false)
const connections = ref([])

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

// 获取连接列表
const fetchConnections = async () => {
  loading.value = true
  try {
    // 这里应该调用后端API
    connections.value = []
    connectionStats.total = 0
    connectionStats.active = 0
    connectionStats.disconnected = 0
  } catch (error) {
    console.error('获取连接列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 刷新连接
const refreshConnections = () => {
  fetchConnections()
}

// 查看详情
const handleViewDetails = (row: any) => {
  console.log('查看详情:', row)
}

// 断开连接
const handleDisconnect = (row: any) => {
  console.log('断开连接:', row)
}

onMounted(() => {
  fetchConnections()
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
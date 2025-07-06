<template>
  <div class="dashboard-container">
    <h2>系统仪表盘</h2>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon">
              <el-icon><Van /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.totalVehicles }}</div>
              <div class="stats-label">车辆总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon">
              <el-icon><Location /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.totalLocations }}</div>
              <div class="stats-label">定位记录</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.activeConnections }}</div>
              <div class="stats-label">活跃连接</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ stats.alarmCount }}</div>
              <div class="stats-label">报警数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统状态 -->
    <el-row :gutter="20" class="status-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统状态</span>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="服务状态">
              <el-tag type="success">运行中</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="数据库状态">
              <el-tag type="success">正常</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="TCP服务">
              <el-tag type="success">正常</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="API服务">
              <el-tag type="success">正常</el-tag>
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>最近活动</span>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(activity, index) in recentActivities"
              :key="index"
              :timestamp="activity.time"
              :type="activity.type"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 统计数据
const stats = ref({
  totalVehicles: 0,
  totalLocations: 0,
  activeConnections: 0,
  alarmCount: 0
})

// 最近活动
const recentActivities = ref([
  {
    time: '2024-12-19 10:30:00',
    content: '系统启动完成',
    type: 'success'
  },
  {
    time: '2024-12-19 10:25:00',
    content: '数据库连接成功',
    type: 'success'
  },
  {
    time: '2024-12-19 10:20:00',
    content: 'TCP服务启动',
    type: 'primary'
  }
])

// 获取统计数据
const fetchStats = async () => {
  // 这里应该调用后端API获取真实数据
  stats.value = {
    totalVehicles: 25,
    totalLocations: 1250,
    activeConnections: 8,
    alarmCount: 3
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  height: 120px;
}

.stats-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stats-icon {
  font-size: 48px;
  color: #409EFF;
  margin-right: 20px;
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
}

.stats-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.status-row {
  margin-bottom: 20px;
}
</style> 
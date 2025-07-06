<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <span>系统设置</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 基本设置 -->
        <el-tab-pane label="基本设置" name="basic">
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" />
            </el-form-item>
            <el-form-item label="TCP服务端口">
              <el-input-number v-model="basicSettings.tcpPort" :min="1024" :max="65535" />
            </el-form-item>
            <el-form-item label="Web服务端口">
              <el-input-number v-model="basicSettings.webPort" :min="1024" :max="65535" />
            </el-form-item>
            <el-form-item label="数据库路径">
              <el-input v-model="basicSettings.dbPath" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 转发设置 -->
        <el-tab-pane label="转发设置" name="forward">
          <el-form :model="forwardSettings" label-width="120px">
            <el-form-item label="启用智能转发">
              <el-switch v-model="forwardSettings.enableSmartForward" />
            </el-form-item>
            <el-form-item label="转发超时时间(秒)">
              <el-input-number v-model="forwardSettings.timeout" :min="1" :max="60" />
            </el-form-item>
            <el-form-item label="最大重试次数">
              <el-input-number v-model="forwardSettings.maxRetries" :min="0" :max="10" />
            </el-form-item>
            <el-form-item label="目标服务器">
              <el-input v-model="forwardSettings.targetServer" placeholder="例如: 192.168.1.100:8080" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveForwardSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 日志设置 -->
        <el-tab-pane label="日志设置" name="log">
          <el-form :model="logSettings" label-width="120px">
            <el-form-item label="日志级别">
              <el-select v-model="logSettings.level">
                <el-option label="DEBUG" value="DEBUG" />
                <el-option label="INFO" value="INFO" />
                <el-option label="WARNING" value="WARNING" />
                <el-option label="ERROR" value="ERROR" />
              </el-select>
            </el-form-item>
            <el-form-item label="日志文件路径">
              <el-input v-model="logSettings.filePath" />
            </el-form-item>
            <el-form-item label="最大日志文件大小(MB)">
              <el-input-number v-model="logSettings.maxSize" :min="1" :max="1000" />
            </el-form-item>
            <el-form-item label="保留日志天数">
              <el-input-number v-model="logSettings.retentionDays" :min="1" :max="365" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveLogSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 监控设置 -->
        <el-tab-pane label="监控设置" name="monitor">
          <el-form :model="monitorSettings" label-width="120px">
            <el-form-item label="启用链路监控">
              <el-switch v-model="monitorSettings.enableMonitoring" />
            </el-form-item>
            <el-form-item label="监控间隔(秒)">
              <el-input-number v-model="monitorSettings.interval" :min="1" :max="60" />
            </el-form-item>
            <el-form-item label="连接超时告警(秒)">
              <el-input-number v-model="monitorSettings.connectionTimeout" :min="5" :max="300" />
            </el-form-item>
            <el-form-item label="数据丢失告警阈值">
              <el-input-number v-model="monitorSettings.dataLossThreshold" :min="1" :max="1000" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveMonitorSettings">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('basic')

// 基本设置
const basicSettings = reactive({
  systemName: 'JT808Proxy',
  tcpPort: 16900,
  webPort: 7000,
  dbPath: './data/jt808proxy.db'
})

// 转发设置
const forwardSettings = reactive({
  enableSmartForward: true,
  timeout: 30,
  maxRetries: 3,
  targetServer: '192.168.1.100:8080'
})

// 日志设置
const logSettings = reactive({
  level: 'INFO',
  filePath: './logs/jt808proxy.log',
  maxSize: 100,
  retentionDays: 30
})

// 监控设置
const monitorSettings = reactive({
  enableMonitoring: true,
  interval: 10,
  connectionTimeout: 60,
  dataLossThreshold: 100
})

const saveBasicSettings = () => {
  ElMessage.success('基本设置保存成功')
}

const saveForwardSettings = () => {
  ElMessage.success('转发设置保存成功')
}

const saveLogSettings = () => {
  ElMessage.success('日志设置保存成功')
}

const saveMonitorSettings = () => {
  ElMessage.success('监控设置保存成功')
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-form {
  max-width: 600px;
}
</style> 
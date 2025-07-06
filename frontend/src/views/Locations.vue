<template>
  <div class="locations-container">
    <h2>定位数据管理</h2>
    
    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="终端手机号">
          <el-input v-model="searchForm.terminal_phone" placeholder="请输入终端手机号" clearable />
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 定位数据列表 -->
    <el-card class="table-card">
      <el-table :data="locations" v-loading="loading" stripe>
        <el-table-column prop="terminal_phone" label="终端手机号" width="150" />
        <el-table-column prop="latitude" label="纬度" width="120" />
        <el-table-column prop="longitude" label="经度" width="120" />
        <el-table-column prop="speed" label="速度(km/h)" width="100" />
        <el-table-column prop="direction" label="方向" width="80" />
        <el-table-column prop="altitude" label="海拔" width="80" />
        <el-table-column prop="timestamp" label="时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleViewDetails(row)">详情</el-button>
            <el-button size="small" type="info" @click="handleViewTrack(row)">轨迹</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

// 响应式数据
const loading = ref(false)
const locations = ref([])

// 搜索表单
const searchForm = reactive({
  terminal_phone: '',
  dateRange: []
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 获取定位数据
const fetchLocations = async () => {
  loading.value = true
  try {
    // 这里应该调用后端API
    locations.value = []
    pagination.total = 0
  } catch (error) {
    console.error('获取定位数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchLocations()
}

// 重置搜索
const handleReset = () => {
  searchForm.terminal_phone = ''
  searchForm.dateRange = []
  pagination.page = 1
  fetchLocations()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  fetchLocations()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchLocations()
}

// 查看详情
const handleViewDetails = (row: any) => {
  console.log('查看详情:', row)
}

// 查看轨迹
const handleViewTrack = (row: any) => {
  console.log('查看轨迹:', row)
}

onMounted(() => {
  fetchLocations()
})
</script>

<style scoped>
.locations-container {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style> 
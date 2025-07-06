<template>
  <div class="vehicles-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>车辆管理</h2>
      <el-button type="primary" @click="showCreateDialog = true">
        <el-icon><Plus /></el-icon>
        添加车辆
      </el-button>
    </div>

    <!-- 搜索栏 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="终端手机号">
          <el-input v-model="searchForm.terminal_phone" placeholder="请输入终端手机号" clearable />
        </el-form-item>
        <el-form-item label="车牌号">
          <el-input v-model="searchForm.plate_number" placeholder="请输入车牌号" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 车辆列表 -->
    <el-card class="table-card">
      <el-table :data="vehicles" v-loading="loading" stripe>
        <el-table-column prop="terminal_phone" label="终端手机号" width="150" />
        <el-table-column prop="vehicle_id" label="车辆ID" width="120" />
        <el-table-column prop="plate_number" label="车牌号" width="120" />
        <el-table-column prop="vehicle_type" label="车辆类型" width="100" />
        <el-table-column prop="manufacturer" label="制造商" width="120" />
        <el-table-column prop="model" label="型号" width="120" />
        <el-table-column prop="color" label="颜色" width="80" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
            <el-button size="small" type="info" @click="handleViewChanges(row)">变更历史</el-button>
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

    <!-- 创建/编辑车辆对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="isEdit ? '编辑车辆' : '添加车辆'"
      width="500px"
    >
      <el-form :model="vehicleForm" :rules="rules" ref="vehicleFormRef" label-width="100px">
        <el-form-item label="终端手机号" prop="terminal_phone">
          <el-input v-model="vehicleForm.terminal_phone" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="车辆ID" prop="vehicle_id">
          <el-input v-model="vehicleForm.vehicle_id" />
        </el-form-item>
        <el-form-item label="车牌号" prop="plate_number">
          <el-input v-model="vehicleForm.plate_number" />
        </el-form-item>
        <el-form-item label="车辆类型" prop="vehicle_type">
          <el-input v-model="vehicleForm.vehicle_type" />
        </el-form-item>
        <el-form-item label="制造商" prop="manufacturer">
          <el-input v-model="vehicleForm.manufacturer" />
        </el-form-item>
        <el-form-item label="型号" prop="model">
          <el-input v-model="vehicleForm.model" />
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-input v-model="vehicleForm.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 变更历史对话框 -->
    <el-dialog v-model="showChangesDialog" title="变更历史" width="600px">
      <el-table :data="changes" stripe>
        <el-table-column prop="field_name" label="字段名" width="120" />
        <el-table-column prop="old_value" label="原值" width="150" />
        <el-table-column prop="new_value" label="新值" width="150" />
        <el-table-column prop="change_time" label="变更时间" width="180" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { vehicleApi, type Vehicle, type VehicleCreate, type VehicleUpdate } from '@/api/vehicle'

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const vehicles = ref<Vehicle[]>([])
const changes = ref([])
const showCreateDialog = ref(false)
const showChangesDialog = ref(false)
const isEdit = ref(false)
const vehicleFormRef = ref()

// 搜索表单
const searchForm = reactive({
  terminal_phone: '',
  plate_number: ''
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 车辆表单
const vehicleForm = reactive<VehicleCreate>({
  terminal_phone: '',
  vehicle_id: '',
  plate_number: '',
  vehicle_type: '',
  manufacturer: '',
  model: '',
  color: ''
})

// 表单验证规则
const rules = {
  terminal_phone: [
    { required: true, message: '请输入终端手机号', trigger: 'blur' }
  ]
}

// 获取车辆列表
const fetchVehicles = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      ...searchForm
    }
    const response = await vehicleApi.getVehicles(params)
    vehicles.value = response.vehicles
    pagination.total = response.total
  } catch (error) {
    ElMessage.error('获取车辆列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchVehicles()
}

// 重置搜索
const handleReset = () => {
  searchForm.terminal_phone = ''
  searchForm.plate_number = ''
  pagination.page = 1
  fetchVehicles()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.page = 1
  fetchVehicles()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchVehicles()
}

// 编辑车辆
const handleEdit = (row: Vehicle) => {
  isEdit.value = true
  Object.assign(vehicleForm, row)
  showCreateDialog.value = true
}

// 删除车辆
const handleDelete = async (row: Vehicle) => {
  try {
    await ElMessageBox.confirm('确定要删除该车辆吗？', '提示', {
      type: 'warning'
    })
    await vehicleApi.deleteVehicle(row.terminal_phone)
    ElMessage.success('删除成功')
    fetchVehicles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 查看变更历史
const handleViewChanges = async (row: Vehicle) => {
  try {
    const response = await vehicleApi.getVehicleChanges(row.terminal_phone)
    changes.value = response
    showChangesDialog.value = true
  } catch (error) {
    ElMessage.error('获取变更历史失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!vehicleFormRef.value) return
  
  try {
    await vehicleFormRef.value.validate()
    submitting.value = true
    
    if (isEdit.value) {
      const { terminal_phone, ...updateData } = vehicleForm
      await vehicleApi.updateVehicle(terminal_phone, updateData)
      ElMessage.success('更新成功')
    } else {
      await vehicleApi.createVehicle(vehicleForm)
      ElMessage.success('创建成功')
    }
    
    showCreateDialog.value = false
    fetchVehicles()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}

// 初始化
onMounted(() => {
  fetchVehicles()
})
</script>

<style scoped>
.vehicles-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
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
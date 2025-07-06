<template>
  <div class="data-table">
    <!-- 工具栏 -->
    <div class="table-toolbar" v-if="showToolbar">
      <div class="toolbar-left">
        <slot name="toolbar-left">
          <el-button type="primary" @click="$emit('add')" v-if="showAdd">
            <el-icon><Plus /></el-icon>
            新增
          </el-button>
          <el-button type="danger" @click="handleBatchDelete" v-if="showBatchDelete && selectedRows.length > 0">
            <el-icon><Delete /></el-icon>
            批量删除
          </el-button>
        </slot>
      </div>
      
      <div class="toolbar-right">
        <slot name="toolbar-right">
          <el-input
            v-model="searchKeyword"
            placeholder="请输入搜索关键词"
            style="width: 200px; margin-right: 10px"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-button @click="handleRefresh">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
          
          <el-button @click="handleExport" v-if="showExport">
            <el-icon><Download /></el-icon>
            导出
          </el-button>
        </slot>
      </div>
    </div>

    <!-- 表格 -->
    <el-table
      :data="tableData"
      :height="height"
      :stripe="stripe"
      :border="border"
      :show-header="showHeader"
      @selection-change="handleSelectionChange"
    >
      <!-- 选择列 -->
      <el-table-column
        v-if="showSelection"
        type="selection"
        width="55"
        align="center"
      />
      
      <!-- 序号列 -->
      <el-table-column
        v-if="showIndex"
        type="index"
        label="序号"
        width="60"
        align="center"
      />
      
      <!-- 动态列 -->
      <slot />
      
      <!-- 操作列 -->
      <el-table-column
        v-if="showActions"
        label="操作"
        :width="actionsWidth"
        align="center"
      >
        <template #default="scope">
          <slot name="actions" :row="scope.row" :$index="scope.$index">
            <el-button
              v-if="showEdit"
              type="primary"
              size="small"
              @click="$emit('edit', scope.row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="showDelete"
              type="danger"
              size="small"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </slot>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="table-pagination" v-if="showPagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pageSizes"
        :total="total"
        :layout="layout"
        @size-change="handleSizeChange"
        @current-change="handleCurrentPageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, Search, Refresh, Download } from '@element-plus/icons-vue'

interface Props {
  data: any[]
  height?: string | number
  stripe?: boolean
  border?: boolean
  showHeader?: boolean
  
  // 自定义属性
  showToolbar?: boolean
  showAdd?: boolean
  showBatchDelete?: boolean
  showExport?: boolean
  showSelection?: boolean
  showIndex?: boolean
  showActions?: boolean
  showEdit?: boolean
  showDelete?: boolean
  actionsWidth?: string | number
  showPagination?: boolean
  total?: number
  pageSizes?: number[]
  layout?: string
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
  stripe: true,
  border: true,
  showHeader: true,
  
  showToolbar: true,
  showAdd: true,
  showBatchDelete: true,
  showExport: true,
  showSelection: false,
  showIndex: true,
  showActions: true,
  showEdit: true,
  showDelete: true,
  actionsWidth: 150,
  showPagination: true,
  total: 0,
  pageSizes: () => [10, 20, 50, 100],
  layout: 'total, sizes, prev, pager, next, jumper'
})

const emit = defineEmits<{
  add: []
  edit: [row: any]
  delete: [row: any]
  batchDelete: [rows: any[]]
  export: []
  refresh: []
  search: [keyword: string]
  selectionChange: [selection: any[]]
  sizeChange: [size: number]
  currentPageChange: [page: number]
}>()

// 响应式数据
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const selectedRows = ref<any[]>([])

// 计算属性
const tableData = computed(() => {
  if (!searchKeyword.value) return props.data
  return props.data.filter(item => {
    return Object.values(item).some(value => 
      String(value).toLowerCase().includes(searchKeyword.value.toLowerCase())
    )
  })
})

// 方法
const handleSearch = () => {
  emit('search', searchKeyword.value)
}

const handleRefresh = () => {
  emit('refresh')
}

const handleExport = () => {
  emit('export')
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    emit('delete', row)
  } catch {
    // 用户取消删除
  }
}

const handleBatchDelete = async () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的记录')
    return
  }
  
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedRows.value.length} 条记录吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    emit('batchDelete', selectedRows.value)
  } catch {
    // 用户取消删除
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
  emit('selectionChange', selection)
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  emit('sizeChange', size)
}

const handleCurrentPageChange = (page: number) => {
  currentPage.value = page
  emit('currentPageChange', page)
}
</script>

<style scoped>
.data-table {
  background: #fff;
  border-radius: 4px;
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.table-pagination {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  border-top: 1px solid #ebeef5;
}

:deep(.el-table) {
  border-radius: 0;
}

:deep(.el-table th) {
  background-color: #fafafa;
}
</style> 
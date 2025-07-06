<template>
  <el-tag
    :type="tagType"
    :color="customColor"
    :effect="effect"
    size="small"
  >
    {{ displayText }}
  </el-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getStatusColor, getStatusText } from '@/utils'

interface Props {
  status: string
  effect?: 'dark' | 'light' | 'plain'
  customColor?: string
}

const props = withDefaults(defineProps<Props>(), {
  effect: 'light',
  customColor: ''
})

const tagType = computed(() => {
  const typeMap: Record<string, string> = {
    'online': 'success',
    'connected': 'success',
    'offline': 'danger',
    'disconnected': 'danger',
    'error': 'danger',
    'warning': 'warning',
    'info': 'info'
  }
  return typeMap[props.status] || 'info'
})

const displayText = computed(() => {
  return getStatusText(props.status)
})

const customColor = computed(() => {
  return props.customColor || getStatusColor(props.status)
})
</script>

<style scoped>
.el-tag {
  border-radius: 4px;
}
</style> 
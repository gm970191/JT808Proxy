<template>
  <div class="map-container">
    <div ref="mapContainer" class="map-content"></div>
    
    <!-- 地图控制面板 -->
    <div class="map-controls" v-if="showControls">
      <el-button-group>
        <el-button size="small" @click="zoomIn">
          <el-icon><ZoomIn /></el-icon>
        </el-button>
        <el-button size="small" @click="zoomOut">
          <el-icon><ZoomOut /></el-icon>
        </el-button>
        <el-button size="small" @click="resetView">
          <el-icon><Refresh /></el-icon>
        </el-button>
      </el-button-group>
    </div>
    
    <!-- 图例 -->
    <div class="map-legend" v-if="showLegend">
      <div class="legend-title">图例</div>
      <div class="legend-item">
        <div class="legend-color online"></div>
        <span>在线车辆</span>
      </div>
      <div class="legend-item">
        <div class="legend-color offline"></div>
        <span>离线车辆</span>
      </div>
      <div class="legend-item">
        <div class="legend-color error"></div>
        <span>异常车辆</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ZoomIn, ZoomOut, Refresh } from '@element-plus/icons-vue'

interface Vehicle {
  id: string
  plate_number: string
  latitude: number
  longitude: number
  status: 'online' | 'offline' | 'error'
  speed?: number
  direction?: number
  last_update?: string
}

interface Props {
  vehicles: Vehicle[]
  center?: [number, number]
  zoom?: number
  showControls?: boolean
  showLegend?: boolean
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  vehicles: () => [],
  center: () => [39.9042, 116.4074], // 北京
  zoom: 10,
  showControls: true,
  showLegend: true,
  height: '400px'
})

const emit = defineEmits<{
  vehicleClick: [vehicle: Vehicle]
  mapClick: [lat: number, lng: number]
}>()

const mapContainer = ref<HTMLElement>()
let map: any = null
let markers: any[] = []

// 初始化地图
const initMap = () => {
  if (!mapContainer.value) return
  
  // 这里使用高德地图API，需要先引入
  // 实际项目中需要配置高德地图的API Key
  console.log('初始化地图...')
  
  // 模拟地图初始化
  mapContainer.value.innerHTML = `
    <div style="
      width: 100%; 
      height: 100%; 
      background: linear-gradient(45deg, #f0f0f0 25%, transparent 25%), 
                  linear-gradient(-45deg, #f0f0f0 25%, transparent 25%), 
                  linear-gradient(45deg, transparent 75%, #f0f0f0 75%), 
                  linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
      background-size: 20px 20px;
      background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #666;
      font-size: 14px;
    ">
      <div style="text-align: center;">
        <div style="font-size: 24px; margin-bottom: 10px;">🗺️</div>
        <div>地图组件</div>
        <div style="font-size: 12px; margin-top: 5px;">需要配置地图API</div>
      </div>
    </div>
  `
}

// 更新车辆标记
const updateMarkers = () => {
  // 清除现有标记
  markers.forEach(marker => {
    if (marker && marker.remove) {
      marker.remove()
    }
  })
  markers = []
  
  // 添加新标记
  props.vehicles.forEach(vehicle => {
    const marker = createMarker(vehicle)
    if (marker) {
      markers.push(marker)
    }
  })
}

// 创建标记
const createMarker = (vehicle: Vehicle) => {
  // 模拟创建标记
  const markerElement = document.createElement('div')
  markerElement.className = `vehicle-marker ${vehicle.status}`
  markerElement.innerHTML = `
    <div class="marker-icon">🚗</div>
    <div class="marker-label">${vehicle.plate_number}</div>
  `
  
  markerElement.addEventListener('click', () => {
    emit('vehicleClick', vehicle)
  })
  
  return {
    element: markerElement,
    remove: () => {
      markerElement.remove()
    }
  }
}

// 地图控制方法
const zoomIn = () => {
  console.log('放大')
}

const zoomOut = () => {
  console.log('缩小')
}

const resetView = () => {
  console.log('重置视图')
}

// 监听车辆数据变化
watch(() => props.vehicles, () => {
  updateMarkers()
}, { deep: true })

// 生命周期
onMounted(() => {
  initMap()
  updateMarkers()
})

onUnmounted(() => {
  // 清理地图资源
  markers.forEach(marker => {
    if (marker && marker.remove) {
      marker.remove()
    }
  })
})
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: v-bind(height);
  border-radius: 4px;
  overflow: hidden;
}

.map-content {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
}

.map-legend {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.legend-title {
  font-weight: bold;
  margin-bottom: 8px;
  font-size: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  font-size: 12px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 6px;
}

.legend-color.online {
  background-color: #67C23A;
}

.legend-color.offline {
  background-color: #F56C6C;
}

.legend-color.error {
  background-color: #E6A23C;
}

.vehicle-marker {
  position: absolute;
  cursor: pointer;
  text-align: center;
}

.marker-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.marker-label {
  font-size: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 4px;
  border-radius: 2px;
  white-space: nowrap;
}

.vehicle-marker.online .marker-icon {
  color: #67C23A;
}

.vehicle-marker.offline .marker-icon {
  color: #F56C6C;
}

.vehicle-marker.error .marker-icon {
  color: #E6A23C;
}
</style> 
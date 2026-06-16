<template>
  <section class="panel full-panel">
    <div class="panel-title">
      <h2>配送任务</h2>
      <span>{{ deliveries.length }} 条任务</span>
    </div>

    <div v-if="loading" class="loading">配送数据加载中...</div>
    <div v-else class="delivery-list">
      <article v-for="task in deliveries" :key="task.id" class="delivery-card">
        <div>
          <strong>订单 #{{ task.order }}</strong>
          <p>{{ task.order_detail.student_name }} · {{ task.order_detail.delivery_address }}</p>
          <small>预计 {{ formatTime(task.estimated_arrival) }}</small>
        </div>
        <div class="delivery-meta">
          <span>{{ task.courier_name || '待分配' }}</span>
          <select :value="task.status" @change="changeStatus(task, $event.target.value)">
            <option value="waiting">待分配</option>
            <option value="assigned">已分配</option>
            <option value="picked">已取餐</option>
            <option value="delivered">已送达</option>
            <option value="failed">异常</option>
          </select>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { fetchDeliveries, updateDelivery } from '../api/canteen'

const props = defineProps({
  reloadKey: {
    type: Number,
    default: 0,
  },
})

const deliveries = ref([])
const loading = ref(false)

async function loadDeliveries() {
  loading.value = true
  try {
    deliveries.value = await fetchDeliveries()
  } finally {
    loading.value = false
  }
}

async function changeStatus(task, status) {
  const payload = { status }
  if (status === 'delivered') {
    payload.delivered_at = new Date().toISOString()
  }
  const updated = await updateDelivery(task.id, payload)
  Object.assign(task, updated)
}

function formatTime(value) {
  if (!value) return '待确认'
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

onMounted(loadDeliveries)
watch(() => props.reloadKey, loadDeliveries)
</script>

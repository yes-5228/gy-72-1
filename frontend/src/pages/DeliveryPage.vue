<template>
  <section class="panel full-panel">
    <div class="panel-title">
      <h2>配送任务</h2>
      <span>{{ deliveries.length }} 条任务</span>
    </div>

    <div v-if="loading" class="loading">配送数据加载中...</div>
    <div v-else class="delivery-list">
      <article v-for="task in deliveries" :key="task.id" :class="['delivery-card', { locked: task.is_locked }]">
        <div>
          <strong>订单 #{{ task.order }}</strong>
          <p>{{ task.order_detail.student_name }} · {{ task.order_detail.delivery_address }}</p>
          <small>预计 {{ formatTime(task.estimated_arrival) }}</small>
        </div>
        <div class="delivery-meta">
          <span>{{ task.courier_name || '待分配' }}</span>
          <select
            :value="task.status"
            :disabled="task.is_locked"
            @change="changeStatus(task, $event.target.value)"
          >
            <option value="waiting">待分配</option>
            <option value="assigned">已分配</option>
            <option value="picked">已取餐</option>
            <option value="delivered">已送达</option>
            <option value="failed">异常</option>
          </select>
        </div>
        <small v-if="task.is_locked" class="lock-hint">🔒 {{ task.lock_reason }}</small>
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
  if (task.is_locked) {
    alert(task.lock_reason || '该配送任务已锁定，无法修改状态')
    return
  }
  const payload = { status }
  if (status === 'delivered') {
    payload.delivered_at = new Date().toISOString()
  }
  try {
    const updated = await updateDelivery(task.id, payload)
    Object.assign(task, updated)
  } catch (error) {
    alert(error.message)
  }
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

<style scoped>
.delivery-card.locked {
  opacity: 0.65;
  background: #fff8f6;
}

.lock-hint {
  grid-column: 1 / -1;
  margin-top: 8px;
  color: #d4380d;
  font-size: 12px;
}

select:disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}
</style>

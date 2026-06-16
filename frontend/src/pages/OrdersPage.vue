<template>
  <div class="content-grid">
    <section class="menu-area full-area">
      <div class="panel full-panel">
        <div class="panel-title">
          <h2>我的订单</h2>
          <span v-if="currentStudent">{{ orders.length }} 条订单</span>
        </div>

        <div v-if="!currentStudent" class="student-login">
          <label>
            请输入学号查看您的订单
            <input v-model="studentNoInput" placeholder="如：S2026008" @keyup.enter="loadMyOrders" />
          </label>
          <button class="primary-button" type="button" @click="loadMyOrders">查询订单</button>
        </div>

        <div v-else>
          <div class="student-info-bar">
            <span>当前学号：<strong>{{ currentStudent }}</strong></span>
            <button class="ghost-button" type="button" @click="switchStudent">切换学号</button>
          </div>

          <div v-if="loading" class="loading">订单加载中...</div>
          <div v-else-if="orders.length === 0" class="empty-state">暂无订单记录</div>
          <div v-else class="order-list">
            <article v-for="order in orders" :key="order.id" class="order-card">
              <header class="order-header">
                <div>
                  <strong>订单 #{{ order.id }}</strong>
                  <small>{{ formatTime(order.created_at) }}</small>
                </div>
                <div class="order-status-row">
                  <span :class="['status-tag', `status-${order.status}`]">{{ getStatusLabel(order.status) }}</span>
                  <button
                    v-if="order.can_cancel"
                    class="danger-button"
                    type="button"
                    :disabled="order.cancelling"
                    @click="cancelOrder(order)"
                  >
                    {{ order.cancelling ? '取消中...' : '取消订单' }}
                  </button>
                </div>
              </header>

              <div class="order-info">
                <p><span>收货人：</span>{{ order.student_name }} · {{ order.phone }}</p>
                <p><span>配送地址：</span>{{ order.delivery_address }}</p>
                <p><span>预约送达：</span>{{ formatTime(order.pickup_time) }}</p>
                <p v-if="order.note"><span>备注：</span>{{ order.note }}</p>
              </div>

              <ul class="order-items">
                <li v-for="item in order.items" :key="item.id">
                  <span>{{ item.dish_detail.name }}</span>
                  <span>× {{ item.quantity }}</span>
                  <span>￥{{ (Number(item.unit_price) * item.quantity).toFixed(2) }}</span>
                </li>
              </ul>

              <footer class="order-footer">
                <span>合计：<strong>￥{{ Number(order.total_amount).toFixed(2) }}</strong></span>
                <small v-if="!order.can_cancel && order.status !== 'cancelled'" class="cancel-hint">{{ order.cancel_reason }}</small>
              </footer>
            </article>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { cancelOrder, fetchOrders } from '../api/canteen'

const props = defineProps({
  reloadKey: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['orderCancelled'])

const STUDENT_KEY = 'canteen_current_student_no'

const currentStudent = ref(localStorage.getItem(STUDENT_KEY) || '')
const studentNoInput = ref(currentStudent.value)
const orders = ref([])
const loading = ref(false)

const STATUS_LABELS = {
  pending: '待确认',
  confirmed: '已确认',
  preparing: '备餐中',
  delivering: '配送中',
  completed: '已完成',
  cancelled: '已取消',
}

function getStatusLabel(status) {
  return STATUS_LABELS[status] || status
}

function formatTime(value) {
  if (!value) return '待确认'
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

async function loadMyOrders() {
  const studentNo = studentNoInput.value.trim()
  if (!studentNo) return
  localStorage.setItem(STUDENT_KEY, studentNo)
  currentStudent.value = studentNo
  loading.value = true
  try {
    orders.value = await fetchOrders({ student_no: studentNo, ordering: '-created_at' })
  } catch (error) {
    alert(`加载订单失败：${error.message}`)
  } finally {
    loading.value = false
  }
}

function switchStudent() {
  currentStudent.value = ''
  studentNoInput.value = ''
  orders.value = []
  localStorage.removeItem(STUDENT_KEY)
}

async function cancelOrder(order) {
  if (!confirm(`确定要取消订单 #${order.id} 吗？菜品库存将自动恢复。`)) return
  order.cancelling = true
  try {
    await cancelOrder(order.id, { operator_student_no: currentStudent.value })
    order.status = 'cancelled'
    order.can_cancel = false
    order.cancel_reason = '订单已取消'
    emit('orderCancelled', order)
  } catch (error) {
    alert(`取消失败：${error.message}`)
  } finally {
    order.cancelling = false
  }
}

onMounted(() => {
  if (currentStudent.value) {
    studentNoInput.value = currentStudent.value
    loadMyOrders()
  }
})
watch(() => props.reloadKey, () => {
  if (currentStudent.value) loadMyOrders()
})
</script>

<style scoped>
.student-login {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 32px;
  max-width: 360px;
}

.student-login label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  color: #666;
}

.student-login input {
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
}

.student-info-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.full-area {
  grid-column: 1 / -1;
}

.order-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  padding: 16px;
  background: #fff;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.order-header strong {
  font-size: 16px;
  display: block;
}

.order-header small {
  color: #999;
  font-size: 12px;
}

.order-status-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-tag {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-pending { background: #fff4e5; color: #d48806; }
.status-confirmed { background: #e6f7ff; color: #1890ff; }
.status-preparing { background: #f9f0ff; color: #722ed1; }
.status-delivering { background: #e6fffb; color: #13c2c2; }
.status-completed { background: #f6ffed; color: #52c41a; }
.status-cancelled { background: #fff1f0; color: #ff4d4f; }

.danger-button {
  padding: 6px 12px;
  background: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.danger-button:disabled {
  background: #ffccc7;
  cursor: not-allowed;
}

.danger-button:hover:not(:disabled) {
  background: #ff7875;
}

.order-info {
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 12px;
}

.order-info p {
  margin: 4px 0;
  font-size: 13px;
  color: #555;
}

.order-info span {
  color: #999;
}

.order-items {
  list-style: none;
  padding: 0;
  margin: 0 0 12px 0;
  border-top: 1px dashed #eee;
}

.order-items li {
  display: grid;
  grid-template-columns: 1fr 80px 100px;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed #eee;
  font-size: 14px;
}

.order-items li:last-child {
  border-bottom: none;
}

.order-items li span:nth-child(2),
.order-items li span:nth-child(3) {
  text-align: right;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.order-footer strong {
  color: #ff4d4f;
  font-size: 16px;
}

.cancel-hint {
  color: #999;
  font-size: 12px;
}
</style>

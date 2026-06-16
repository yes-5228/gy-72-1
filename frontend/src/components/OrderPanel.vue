<template>
  <section class="panel order-panel">
    <div class="panel-title">
      <h2>当前餐盘</h2>
      <span>{{ cart.length }} 类菜品</span>
    </div>

    <div v-if="cart.length === 0" class="empty-state">从菜品列表选择餐品后可提交提前订餐。</div>
    <div v-else class="cart-list">
      <div v-for="item in cart" :key="item.dish.id" class="cart-item">
        <div>
          <strong>{{ item.dish.name }}</strong>
          <small>￥{{ item.dish.price }} / 份</small>
        </div>
        <div class="stepper">
          <button type="button" @click="$emit('decrease', item.dish.id)">-</button>
          <span>{{ item.quantity }}</span>
          <button type="button" @click="$emit('increase', item.dish)">+</button>
        </div>
      </div>
    </div>

    <form class="order-form" @submit.prevent="submitOrder">
      <label>
        学生姓名
        <input v-model="form.student_name" required placeholder="如：张同学" />
      </label>
      <label>
        学号
        <input v-model="form.student_no" required placeholder="如：S2026008" />
      </label>
      <label>
        联系电话
        <input v-model="form.phone" required placeholder="用于配送联系" />
      </label>
      <label>
        配送地址
        <input v-model="form.delivery_address" required placeholder="教学楼 / 宿舍 / 班级" />
      </label>
      <label>
        预约送达
        <input v-model="form.pickup_time" required type="datetime-local" />
      </label>
      <label>
        备注
        <textarea v-model="form.note" rows="3" placeholder="少辣、不要香菜等"></textarea>
      </label>

      <div class="total-row">
        <span>合计</span>
        <strong>￥{{ totalAmount }}</strong>
      </div>
      <button class="primary-button" type="submit" :disabled="submitting || cart.length === 0">
        {{ submitting ? '提交中...' : '提交订单' }}
      </button>
      <p v-if="message" class="form-message">{{ message }}</p>
    </form>
  </section>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { createOrder } from '../api/canteen'

const props = defineProps({
  cart: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['created', 'increase', 'decrease'])
const submitting = ref(false)
const message = ref('')

const plusHours = new Date(Date.now() + 2 * 60 * 60 * 1000)
const form = reactive({
  student_name: '',
  student_no: '',
  phone: '',
  delivery_address: '',
  pickup_time: plusHours.toISOString().slice(0, 16),
  note: '',
})

const totalAmount = computed(() =>
  props.cart.reduce((sum, item) => sum + Number(item.dish.price) * item.quantity, 0).toFixed(2),
)

async function submitOrder() {
  submitting.value = true
  message.value = ''
  try {
    const payload = {
      ...form,
      pickup_time: new Date(form.pickup_time).toISOString(),
      items: props.cart.map((item) => ({ dish: item.dish.id, quantity: item.quantity })),
    }
    const order = await createOrder(payload)
    message.value = `订单 #${order.id} 已提交，金额 ￥${order.total_amount}`
    emit('created', order)
  } catch (error) {
    message.value = error.message
  } finally {
    submitting.value = false
  }
}
</script>

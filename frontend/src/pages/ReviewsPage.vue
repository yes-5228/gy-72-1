<template>
  <div class="reviews-layout">
    <section class="panel">
      <div class="panel-title">
        <h2>提交评价</h2>
      </div>
      <form class="order-form" @submit.prevent="submitReview">
        <label>
          菜品
          <select v-model="form.dish" required>
            <option value="">请选择菜品</option>
            <option v-for="dish in dishes" :key="dish.id" :value="dish.id">{{ dish.name }}</option>
          </select>
        </label>
        <label>
          姓名
          <input v-model="form.student_name" required placeholder="评价人" />
        </label>
        <label>
          评分
          <input v-model.number="form.rating" max="5" min="1" required type="number" />
        </label>
        <label>
          评价内容
          <textarea v-model="form.content" required rows="5" placeholder="口味、分量、配送体验等"></textarea>
        </label>
        <button class="primary-button" type="submit">提交评价</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-title">
        <h2>近期反馈</h2>
        <span>{{ reviews.length }} 条</span>
      </div>
      <div class="review-list">
        <article v-for="review in reviews" :key="review.id" class="review-card">
          <div>
            <strong>{{ review.dish_detail.name }}</strong>
            <span>{{ '★'.repeat(review.rating) }}</span>
          </div>
          <p>{{ review.content }}</p>
          <small>{{ review.student_name }} · {{ formatDate(review.created_at) }}</small>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { createReview, fetchDishes, fetchReviews } from '../api/canteen'

const props = defineProps({
  reloadKey: {
    type: Number,
    default: 0,
  },
})

const dishes = ref([])
const reviews = ref([])
const form = reactive({
  dish: '',
  student_name: '',
  rating: 5,
  content: '',
})

async function loadData() {
  const [dishData, reviewData] = await Promise.all([fetchDishes(), fetchReviews()])
  dishes.value = dishData
  reviews.value = reviewData
}

async function submitReview() {
  await createReview({ ...form })
  form.content = ''
  form.rating = 5
  await loadData()
}

function formatDate(value) {
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

onMounted(loadData)
watch(() => props.reloadKey, loadData)
</script>

<template>
  <article class="dish-card">
    <div class="dish-media" :style="{ background: gradient }">
      <span>{{ dish.category_name }}</span>
    </div>
    <div class="dish-body">
      <div class="dish-heading">
        <div>
          <h3>{{ dish.name }}</h3>
          <p>{{ mealLabel }} · {{ dish.available_date }}</p>
        </div>
        <strong>￥{{ dish.price }}</strong>
      </div>
      <p class="dish-desc">{{ dish.description }}</p>
      <div class="nutrition-row">
        <span>{{ dish.calories }} kcal</span>
        <span>蛋白 {{ dish.protein }}g</span>
        <span>钠 {{ dish.sodium }}mg</span>
      </div>
      <div class="dish-footer">
        <span :class="['stock-pill', dish.stock < 10 ? 'warning' : '']">库存 {{ dish.stock }}</span>
        <button type="button" :disabled="dish.stock === 0" @click="$emit('add', dish)">加入餐盘</button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  dish: {
    type: Object,
    required: true,
  },
})

defineEmits(['add'])

const mealMap = {
  breakfast: '早餐',
  lunch: '午餐',
  dinner: '晚餐',
}

const mealLabel = computed(() => mealMap[props.dish.meal_period] || props.dish.meal_period)
const gradients = [
  'linear-gradient(135deg, #2f7d57, #9ad3bc)',
  'linear-gradient(135deg, #b45134, #f1bd8a)',
  'linear-gradient(135deg, #425c8c, #9eb7ef)',
  'linear-gradient(135deg, #78613b, #e0c276)',
]
const gradient = computed(() => gradients[props.dish.id % gradients.length])
</script>

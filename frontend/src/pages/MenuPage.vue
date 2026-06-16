<template>
  <div class="content-grid">
    <section class="menu-area">
      <div class="toolbar">
        <div class="filter-group">
          <button
            v-for="option in mealOptions"
            :key="option.value"
            :class="{ selected: filters.meal_period === option.value }"
            type="button"
            @click="filters.meal_period = option.value"
          >
            {{ option.label }}
          </button>
        </div>
        <select v-model="filters.category">
          <option value="">全部分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      <div v-if="loading" class="loading">菜品加载中...</div>
      <div v-else class="dish-grid">
        <DishCard v-for="dish in dishes" :key="dish.id" :dish="dish" @add="addToCart" />
      </div>
    </section>

    <aside class="side-stack">
      <OrderPanel
        :cart="cart"
        @created="handleOrderCreated"
        @increase="addToCart"
        @decrease="decreaseCart"
      />
      <NutritionPanel :dish-ids="cartDishIds" />
    </aside>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { fetchCategories, fetchDishes } from '../api/canteen'
import DishCard from '../components/DishCard.vue'
import NutritionPanel from '../components/NutritionPanel.vue'
import OrderPanel from '../components/OrderPanel.vue'

const props = defineProps({
  reloadKey: {
    type: Number,
    default: 0,
  },
})

const categories = ref([])
const dishes = ref([])
const cart = ref([])
const loading = ref(false)
const filters = reactive({
  meal_period: '',
  category: '',
})

const mealOptions = [
  { value: '', label: '全部' },
  { value: 'breakfast', label: '早餐' },
  { value: 'lunch', label: '午餐' },
  { value: 'dinner', label: '晚餐' },
]

const cartDishIds = computed(() => cart.value.map((item) => item.dish.id))

async function loadData() {
  loading.value = true
  try {
    const [categoryData, dishData] = await Promise.all([
      fetchCategories(),
      fetchDishes({ meal_period: filters.meal_period, category: filters.category }),
    ])
    categories.value = categoryData
    dishes.value = dishData
  } finally {
    loading.value = false
  }
}

function addToCart(dish) {
  const existing = cart.value.find((item) => item.dish.id === dish.id)
  if (existing) {
    if (existing.quantity < dish.stock) {
      existing.quantity += 1
    }
  } else {
    cart.value.push({ dish, quantity: 1 })
  }
}

function decreaseCart(dishId) {
  const existing = cart.value.find((item) => item.dish.id === dishId)
  if (!existing) return
  existing.quantity -= 1
  if (existing.quantity <= 0) {
    cart.value = cart.value.filter((item) => item.dish.id !== dishId)
  }
}

function handleOrderCreated() {
  cart.value = []
  loadData()
}

onMounted(loadData)
watch(() => [filters.meal_period, filters.category, props.reloadKey], loadData)
</script>

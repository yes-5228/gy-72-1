<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-mark">食</span>
        <div>
          <strong>校园订餐</strong>
          <small>School Canteen</small>
        </div>
      </div>
      <nav>
        <button
          v-for="item in navItems"
          :key="item.key"
          :class="{ active: currentPage === item.key }"
          type="button"
          @click="currentPage = item.key"
        >
          <span>{{ item.icon }}</span>
          {{ item.label }}
        </button>
      </nav>
    </aside>

    <main class="main-panel">
      <header class="topbar">
        <div>
          <p class="eyebrow">提前订餐 · 营养分析 · 配送闭环</p>
          <h1>{{ pageTitle }}</h1>
        </div>
        <button class="ghost-button" type="button" @click="reloadKey++">刷新数据</button>
      </header>

      <MenuPage v-if="currentPage === 'menu'" :reload-key="reloadKey" />
      <DeliveryPage v-else-if="currentPage === 'delivery'" :reload-key="reloadKey" />
      <ReviewsPage v-else :reload-key="reloadKey" />
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import DeliveryPage from './pages/DeliveryPage.vue'
import MenuPage from './pages/MenuPage.vue'
import ReviewsPage from './pages/ReviewsPage.vue'

const currentPage = ref('menu')
const reloadKey = ref(0)

const navItems = [
  { key: 'menu', label: '菜品订餐', icon: '🍱' },
  { key: 'delivery', label: '配送管理', icon: '🚚' },
  { key: 'reviews', label: '评价反馈', icon: '★' },
]

const pageTitle = computed(() => navItems.find((item) => item.key === currentPage.value)?.label)
</script>

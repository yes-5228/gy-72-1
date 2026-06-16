<template>
  <section class="panel">
    <div class="panel-title">
      <h2>营养成分分析</h2>
      <button class="ghost-button small" type="button" :disabled="dishIds.length === 0" @click="runAnalysis">
        重新分析
      </button>
    </div>

    <div v-if="!analysis" class="empty-state">餐盘中有菜品后可查看总热量、蛋白质、脂肪、碳水和钠含量。</div>
    <template v-else>
      <div class="macro-grid">
        <div v-for="item in macroItems" :key="item.label">
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
        </div>
      </div>
      <ul class="advice-list">
        <li v-for="advice in analysis.advice" :key="advice">{{ advice }}</li>
      </ul>
    </template>
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { analyzeNutrition } from '../api/canteen'

const props = defineProps({
  dishIds: {
    type: Array,
    required: true,
  },
})

const analysis = ref(null)

const macroItems = computed(() => {
  if (!analysis.value) return []
  const totals = analysis.value.totals
  return [
    { label: '热量', value: `${totals.calories} kcal` },
    { label: '蛋白质', value: `${totals.protein} g` },
    { label: '脂肪', value: `${totals.fat} g` },
    { label: '碳水', value: `${totals.carbohydrate} g` },
    { label: '钠', value: `${totals.sodium} mg` },
  ]
})

async function runAnalysis() {
  if (props.dishIds.length === 0) {
    analysis.value = null
    return
  }
  analysis.value = await analyzeNutrition(props.dishIds)
}

watch(() => props.dishIds.join(','), runAnalysis, { immediate: true })
</script>

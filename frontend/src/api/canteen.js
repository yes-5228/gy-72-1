import { api } from './client'

export function fetchCategories() {
  return api.get('/categories/')
}

export function fetchDishes(params = {}) {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      search.set(key, value)
    }
  })
  const suffix = search.toString() ? `?${search}` : ''
  return api.get(`/dishes/${suffix}`)
}

export function createOrder(payload) {
  return api.post('/orders/', payload)
}

export function analyzeNutrition(dishIds) {
  return api.post('/nutrition/analyze/', { dish_ids: dishIds })
}

export function fetchDeliveries() {
  return api.get('/deliveries/?ordering=estimated_arrival')
}

export function updateDelivery(id, payload) {
  return api.patch(`/deliveries/${id}/`, payload)
}

export function fetchReviews() {
  return api.get('/reviews/?ordering=-created_at')
}

export function createReview(payload) {
  return api.post('/reviews/', payload)
}

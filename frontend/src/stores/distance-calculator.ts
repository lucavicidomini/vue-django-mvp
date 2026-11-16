import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDistanceCalculatorStore = defineStore('distanceCalculator', () => {
  const distance = ref(1000)

  return { distance }
})
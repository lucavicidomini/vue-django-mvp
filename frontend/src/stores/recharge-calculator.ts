import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRechargeCalculatorStore = defineStore('rechargeCalculator', () => {
  const value = ref<[number, number]>([60, 80])

  return { value }
})
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export enum FuelType {
  EV = 0,
  Petrol = 1,
  Gasoline = 2,
  CNG = 3, // Compressed Natural Gas (Metano)
  LPG = 4 // Liquefied Petroleum Gas (GPL)
}

export interface Vehicle {
  id: number
  name: string
  usable_battery: number
  fuel_type: number,
  scenarios?: VehicleScenario[]
}

export interface VehicleScenario {
  id: number
  name: string
  consumption: number
}

export const useVehicleStore = defineStore('vehicles', () => {
  const all = ref<Vehicle[]>([
    { name: 'Vehicle 1', id: 1, usable_battery: 80, fuel_type: 0 }
  ])

  const evs = computed(() => all.value.filter(v => v.fuel_type === 0))

  const isEmpty = computed(() => all.value.length === 0)
  
  return { all, evs, isEmpty }
})

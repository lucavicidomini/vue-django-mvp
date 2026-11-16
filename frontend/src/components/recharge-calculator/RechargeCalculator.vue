<script setup lang="ts">
import { MCard, MFlex, MGrid } from '@m3ui-vue/m3ui-vue';
import RechargeInput from './RechargeInput.vue';
import { computed } from 'vue';
import type { Vehicle, VehicleRechargeSpeed, VehicleScenario } from '@/stores/vehicle';
import { FuelType, type Fuel } from '@/stores/fuel.ts';
import { useRechargeCalculatorStore } from '@/stores/recharge-calculator';
import type { CalculatorCard } from '@/models/calculator-card';

const props = defineProps({
  vehicles: {
    type: Array as () => Vehicle[],
    required: true
  },
  fuels: {
    type: Array as () => Fuel[],
    required: true
  },
});

const store = useRechargeCalculatorStore();

const evFuel = computed(() => props.fuels.find(fuel => fuel.id === FuelType.EV))

const evVehicles = computed(() => props.vehicles.filter(vehicle => vehicle.fuel_type === evFuel.value?.id))

const cards = computed(() => {
  if (!evFuel.value) {
    return [];
  }
  const cards: CalculatorCard[] = [];
  const evCost = evFuel.value;
  const [from, to] = store.value;
  const percentage = (to - from) / 100.0;
  for (const vehicle of evVehicles.value) {
    if (!vehicle.recharge_speeds?.length) {
      continue;
    }
    const amount = vehicle.usable_battery * percentage
    const card: CalculatorCard = {
      key: vehicle.id,
      title: vehicle.name,
      data: []
    };
    for (const rechargeSpeed of vehicle.recharge_speeds) {
      card.data.push({
        key: rechargeSpeed.id,
        subtitle: rechargeSpeed.name,
        value: getDurationFor(rechargeSpeed, amount)
      })
    }
    if (card.data.length) {
      cards.push(card);
    }
  }
  return cards;
})

const getDurationFor = (scenario: VehicleRechargeSpeed, amount: number): string => {
  const minutes = Math.ceil(amount / scenario.net_speed * 60);
  const hh = Math.trunc(minutes / 60);
  const mm = minutes % 60;
  return `${hh}h ${mm.toString().padStart(2, '0')}m`
}

</script>

<template>
  <MFlex direction="column" gap="md">
    <RechargeInput v-model="store.value" />
    <MCard v-for="card in cards" :key="card.key">
      <template #header>
        <div>{{ card.title }}</div>
      </template>
        <MGrid :cols="1" :sm="2" :lg="3" :xl="4" class="m-4" gap="md">
          <MCard
            v-for="item in card.data"
            :key="card.key + '-' + item.key"
            variant="outlined"
            
          >
            <MFlex justify="between" class="p-4">
              <div>{{ item.subtitle }}</div>
              <div>{{ item.value }}</div>
            </MFlex>
          </MCard>
        </MGrid>
    </MCard>
  </MFlex>
</template>

<style scoped></style>

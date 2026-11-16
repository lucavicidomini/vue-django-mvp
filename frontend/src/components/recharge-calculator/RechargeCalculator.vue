<script setup lang="ts">
import { MCard, MFlex, MGrid } from '@m3ui-vue/m3ui-vue';
import RechargeInput from './RechargeInput.vue';
import { computed } from 'vue';
import type { Vehicle, VehicleScenario } from '@/stores/vehicle';
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
  for (const vehicle of evVehicles.value) {
    if (!vehicle.scenarios?.length) {
      continue;
    }
    const card: CalculatorCard = {
      key: vehicle.id,
      title: vehicle.name,
      data: []
    };
    for (const scenario of vehicle.scenarios) {
      const fuel = getFuelFor(vehicle);
      if (fuel) {
        card.data.push({
          key: scenario.id,
          subtitle: scenario.name,
          value: getCostFor(scenario, fuel)
        });
      }
    }
    if (card.data.length) {
      cards.push(card);
    }
  }
  return cards;
})

const getFuelFor = (vehicle: Vehicle) => {
  return props.fuels.find(fuel => fuel.id === vehicle.fuel_type);
}

const getCostFor = (scenario: VehicleScenario, fuel: Fuel): string => {
  return "n/a" // (store.distance / consumption * fuel.price).toFixed(2);
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
              <div>{{ item.value }} €</div>
            </MFlex>
          </MCard>
        </MGrid>
    </MCard>
  </MFlex>
</template>

<style scoped></style>

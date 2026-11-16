<script setup lang="ts">
import { MCard, MFlex, MGrid, MIcon } from '@m3ui-vue/m3ui-vue';
import { computed, onMounted, ref } from 'vue';
import { useQuery } from '@tanstack/vue-query';
import type { CalculatorToggleKey, CalculatorToggleOption } from '@/models/calculator-toggle';
import type { Vehicle, VehicleScenario } from '@/stores/vehicle';
import DistanceInput from './DistanceInput.vue';
import type { Fuel } from '@/stores/fuel.ts';
import { useDistanceCalculatorStore } from '@/stores/distance-calculator.ts';

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

const store = useDistanceCalculatorStore();

interface CalculatorCard {
  key: number;
  title: string;
  data: {
    key: number;
    subtitle: string;
    value: string;
  }[]
}

const cards = computed(() => {
  const cards: CalculatorCard[] = [];
  for (const vehicle of props.vehicles) {
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
  const consumption = fuel.inverted ? 100 / scenario.consumption : scenario.consumption
  return (store.distance / consumption * fuel.price).toFixed(2);
}

</script>

<template>
  <MFlex direction="column" gap="md">
    <DistanceInput v-model="store.distance" />
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

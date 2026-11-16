<script setup lang="ts">
import { useVehiclesQuery } from '@/services/vehicles';
import { useFuelsQuery } from '@/services/fuels';
import { ref } from 'vue';
import type { CalculatorToggleKey } from '@/models/calculator-toggle';
import DistanceCalculator from '@/components/distance-calculator/DistanceCalculator.vue';
import CalculatorToggle from '@/components/dashboard/CalculatorToggle.vue';

const { data: vehicles} = useVehiclesQuery();
const { data: fuels } = useFuelsQuery();

const calculatorSelected = ref<CalculatorToggleKey | undefined>();

</script>

<template>
  <CalculatorToggle
    :modelValue="calculatorSelected"
    @select="calculatorSelected = $event"
    class="mb-3"
  />
  <DistanceCalculator
    v-if="calculatorSelected === 'distance'"
    :vehicles="vehicles ?? []"
    :fuels="fuels ?? []"
  />
  <div v-else-if="calculatorSelected === 'time'">
    <div>Charging time calculator content goes here</div>
  </div>
</template>

<style scoped></style>

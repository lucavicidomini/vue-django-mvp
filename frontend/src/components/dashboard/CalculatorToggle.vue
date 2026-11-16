<script setup lang="ts">
import { vehicleApis } from '@/services/vehicles';
import { MCard, MFlex, MGrid, MIcon } from '@m3ui-vue/m3ui-vue';
import { onMounted, ref } from 'vue';
import { useQuery } from '@tanstack/vue-query';
import type { CalculatorToggleKey, CalculatorToggleOption } from '@/models/calculator-toggle';

const props = defineProps({
  modelValue: {
    type: String as () => CalculatorToggleKey,
    required: false
  }
});

const emit = defineEmits(['select'])

const options: CalculatorToggleOption[] = [
    {
        title: 'Distance & Cost',
        subtitle: 'Calculate distance and cost',
        icon: 'route',
        key: 'distance'
    },
    {
        title: 'Charging time',
        subtitle: 'Calculate charging time',
        icon: 'timer',
        key: 'time'
    }
]

onMounted(() => {
  if (!props.modelValue) {
    emit('select', options[0]!.key);
  }
});

</script>

<template>
  <MGrid :cols="2">
    <MCard
      v-for="option in options"
      :key="option.key"
      :variant="props.modelValue === option.key ? 'filled' : 'elevated'"
      :clickable="props.modelValue !== option.key"
      @click="emit('select', option.key)"
    >
      <template #header>
        <MFlex class="gap-2 pb-2" align="center">
            <MIcon :name="option.icon" />
            <div>
                <h3 class="text-title-medium font-medium">{{ option.title }}</h3>
                <p class="text-body-small text-on-surface-variant">{{ option.subtitle }}</p>
            </div>
        </MFlex>
      </template>
    </MCard>
  </MGrid>
</template>

<style scoped></style>

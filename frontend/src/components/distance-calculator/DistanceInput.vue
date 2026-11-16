<script setup lang="ts">
import { MBox, MFlex, MSlider, MTextField } from '@m3ui-vue/m3ui-vue';
import { computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['update:modelValue'])

const sliderValue = computed(() => Math.min(Math.max(props.modelValue, 1), 1000))

</script>

<template>
  <MBox
    :border="true"
    rounded="lg"
    padding="sm"
  >
    <MFlex
      gap="md"
      align="center"
    >
      <MTextField
        label="Distance"
        type="number"
        :model-value="modelValue"
        @update:model-value="$emit('update:modelValue', $event)"
      >
        <template #trailing>km</template>
      </MTextField>
      <MSlider
        :min="1"
        :max="1000"
        :model-value="sliderValue"
        class="flex-grow"
        @update:model-value="$emit('update:modelValue', Array.isArray($event) ? $event[0] : $event)"
      />
    </MFlex>
  </MBox>
</template>

<style scoped></style>
